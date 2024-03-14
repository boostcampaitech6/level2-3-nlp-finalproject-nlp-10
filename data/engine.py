import asyncio
from crawling import RestClient, NewsCrawler
from datetime import datetime

from collections import Counter
from functools import reduce

import random
import numpy as np
import pandas as pd
import pymysql
from datetime import datetime, timedelta

from dotenv import load_dotenv
import os
from loguru import logger
import tenacity
from tqdm import tqdm, trange

load_dotenv()
tqdm.pandas()

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification, BartForConditionalGeneration
from sentence_transformers import SentenceTransformer
import hdbscan

def fix_seed(seed = 42):
    random.seed(seed) # python random seed 고정
    np.random.seed(seed) # numpy random seed 고정
    torch.manual_seed(seed) # torch random seed 고정
    torch.cuda.manual_seed_all(seed)


class Engine:
    def __init__(self, db_user, db_password, db_host, topic_n, db_database='AUTOMATION', db_port=3306, period=24, day_diff = 0):
        # MySQL 서버 정보 설정
        self.db_config = {
            'user': db_user,
            'password': db_password,
            'host': db_host,
            'database': db_database,
            'port': int(db_port)  # MySQL 기본 포트
        }
        
        # topic_code에 사용되는 변수. 삼성전자_{topic_n}_0, 삼성전자_{topic_n}_1, 삼성전자_{topic_n}_2, ...   
        self.topic_n = topic_n
        
        # 수집하는 시간 업데이트
        if period == 24:
            self.today = (datetime.now() - timedelta(days=day_diff)).strftime('%Y-%m-%d')
            self.start_time = (datetime.now() - timedelta(days=day_diff)).replace(hour=0, minute=0, second=0, microsecond=0)
            self.end_time = (datetime.now() - timedelta(days=day_diff)).replace(hour=23, minute=59, second=59, microsecond=0)

        else:
            self.today = datetime.now().strftime('%Y-%m-%d')
            self.start_time = (datetime.now() - timedelta(hours=period)).replace(minute=0, second=0, microsecond=0)
            self.end_time = datetime.now().replace(minute=0, second=0, microsecond=0)
        
        logger.info(f"Automation Process Start : {self.start_time.strftime('%Y-%m-%d %H:%M:%S')} ~ {self.end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    
    def db_connection(self):
        # MySQL 연결 설정
        connection = pymysql.connect(
            user=self.db_config['user'],
            password=self.db_config['password'],
            host=self.db_config['host'],
            database=self.db_config['database'],
            port=self.db_config['port'],
            cursorclass=pymysql.cursors.DictCursor  # 결과를 딕셔너리로 받기 위한 설정
        )
        
        return connection
    
    @tenacity.retry(wait=tenacity.wait_fixed(3), stop=tenacity.stop_after_attempt(5))
    def insert_data_to_db(self, query, data, description=''):
        try:
            connection = self.db_connection()
            with connection.cursor() as cursor:
                # 데이터 입력 및 커밋
                result = cursor.executemany(query, data)
                connection.commit()
        
        except Exception as e:
            logger.error(f"{description} | ERROR : {e}")
            raise ValueError(f'ERROR : {description}')    

        finally:
            connection.close()
    
    @tenacity.retry(wait=tenacity.wait_fixed(3), stop=tenacity.stop_after_attempt(5))
    def select_data_from_db(self, query, description=''):
        try:
            connection = self.db_connection()
            with connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                
        except Exception as e:
            logger.error(f"{description} | ERROR : {e}")
            raise ValueError(f'ERROR : {description}')    

        finally:
            connection.close()
        
        return result
    
    
    def fill_company(self, path='./utils/company.csv') -> None:
        table_name = 'COMPANY'
        logger.info(f"INSERT {table_name} TABLE START")
        
        df = pd.read_csv(path)
        company_info = df.to_dict(orient='index')
        # to_dict 과정에서 정수로 구성된 문자열이 정수로 변함.
        company_info = [{'company_code' : '0'*(6-len(str(company_info[idx]['company_code']))) + str(company_info[idx]['company_code']), 
                            'name' : company_info[idx]['name'] } for idx in company_info]        
        
        self.insert_data_to_db(query = f"INSERT INTO {self.db_config['database']}.{table_name} (company_code, name) VALUES (%(company_code)s, %(name)s)",
                               data = company_info, 
                               description = f'INSERT {table_name} TABLE')
        
        logger.info(f"INSERT {table_name} TABLE DONE")
        
        
        
    async def fill_news(self):
        table_name = 'NEWS'
        start_time, end_time = self.start_time.strftime('%Y-%m-%d %H:%M:%S'), self.end_time.strftime('%Y-%m-%d %H:%M:%S')
        logger.info(f"INSERT {table_name} TABLE START : {start_time} ~ {end_time}")
        # 뉴스 데이터 크롤링.
        await self.crawling_news()
        logger.info(f"NEWS Crawling Done")
        
        # 수집한 데이터 로드 및 전처리
        news_info = self.preprocess_news()
        logger.info(f"NEWS Preprocessing Done")
        
        self.insert_data_to_db(query = f"INSERT INTO {self.db_config['database']}.{table_name} (date, url, title, contents, relate_stock) \
                                                            VALUES (%(date)s, %(url)s, %(title)s, %(contents)s, %(relate_stock)s)",
                               data = news_info, 
                               description = f'INSERT {table_name} TABLE')
        logger.info(f"INSERT {table_name} TABLE DONE : {start_time} ~ {end_time}")
    
    
    
    
    def fill_news_company(self):
        table_name = 'NEWS_COMPANY'
        start_time, end_time = self.start_time.strftime('%Y-%m-%d %H:%M:%S'), self.end_time.strftime('%Y-%m-%d %H:%M:%S')
        logger.info(f"INSERT {table_name} TABLE START : {start_time} ~ {end_time}")        
        # NEWS, COMPANY 데이터 조회, 
        news_data = self.select_data_from_db(query = f"SELECT * FROM {self.db_config['database']}.NEWS WHERE date BETWEEN '{start_time}' AND '{end_time}';", 
                                             description='SELECT NEWS TABLE')
        company_data = self.select_data_from_db(query = f"SELECT * FROM {self.db_config['database']}.COMPANY;",
                                                description='SELECT COMPANY TABLE')
        logger.info(f"NEWS, COMPANY SELECT Done")
        
        # NEWS_COMPANY 테이블에 맞게 전처리
        news_company_info = self.preprocess_news_company(news_data, company_data)
        logger.info(f"{table_name} Preprocessing Done")
        
        # NEWS_COMPANY 테이블에 입력
        self.insert_data_to_db(query=f"INSERT INTO {self.db_config['database']}.{table_name} (news_id, company_id) VALUES (%(news_id)s, %(company_id)s)",
                               data=news_company_info,
                               description=f'INSERT {table_name} TABLES')
        logger.info(f"INSERT {table_name} TABLE DONE : {start_time} ~ {end_time}")
    
    
    def fill_summary(self):
        table_name = 'SUMMARY'
        start_time, end_time = self.start_time.strftime('%Y-%m-%d %H:%M:%S'), self.end_time.strftime('%Y-%m-%d %H:%M:%S')
        logger.info(f"INSERT {table_name} TABLE START : {start_time} ~ {end_time}")
        # NEWS, COMPANY 데이터 조회, 
        news_data = self.select_data_from_db(query = f"SELECT * FROM {self.db_config['database']}.NEWS WHERE date BETWEEN '{start_time}' AND '{end_time}';", 
                                             description='SELECT NEWS TABLE')
        logger.info(f"NEWS SELECT Done")
        
        # NEWS 요약 데이터 생성
        summary_info = self.preprocess_summary(news_data=news_data, 
                                               model_path= './model/summary/summary_model.pt',
                                               pretrained_model_name_or_path="EbanLee/kobart-summary-v2")
        logger.info(f"NEWS {table_name} Done")
        
        # SUMMARY TABLE에 데이터 입력
        self.insert_data_to_db(query=f"INSERT INTO {self.db_config['database']}.{table_name} (news_id, summary_text) VALUES (%(news_id)s, %(summary_text)s)",
                               data = summary_info,
                               description=f'INSERT {table_name} TABLES')
        logger.info(f"INSERT {table_name} TABLE END : {start_time} ~ {end_time}")

        
    
    def fill_sentiment(self):
        table_name = 'SENTIMENT'
        start_time, end_time = self.start_time.strftime('%Y-%m-%d %H:%M:%S'), self.end_time.strftime('%Y-%m-%d %H:%M:%S')
        logger.info(f"INSERT SENTIMENT TABLE START : {start_time} ~ {end_time}")
        
        # NEWS, COMPANY 데이터 조회, 
        news_data = self.select_data_from_db(query = f"SELECT * FROM {self.db_config['database']}.NEWS WHERE date BETWEEN '{start_time}' AND '{end_time}';", 
                                             description='SELECT NEWS TABLE')
        logger.info(f"NEWS SELECT Done")
        
        # NEWS SENTIMENT 데이터 생성
        sentiment_info = self.preprocess_sentiemnt(news_data = news_data,
                                                   model_path='model/sentiment',
                                                   pretrained_model_name_or_path='model/sentiment')
        logger.info(f"NEWS {table_name} Done")
        
        # SENTIMENT TABLE에 데이터 입력
        self.insert_data_to_db(query=f"INSERT INTO {self.db_config['database']}.{table_name} (news_id, sentiment_value) VALUES (%(news_id)s, %(sentiment_value)s)",
                               data = sentiment_info,
                               description=f'INSERT {table_name} TABLES')
        logger.info(f"INSERT SENTIMENT TABLE END : {start_time} ~ {end_time}")
        
    
    
    def fill_topic(self):
        table_name = 'TOPIC'
        start_time, end_time = self.start_time.strftime('%Y-%m-%d %H:%M:%S'), self.end_time.strftime('%Y-%m-%d %H:%M:%S')
        logger.info(f"INSERT {table_name} TABLE START : {start_time} ~ {end_time}")
        # NEWS, SUMMARY, COMPANY, NEWS_COMPANY 테이블병합 데이터 조회, 
        merge_data = self.select_data_from_db(query = f"""
                                                                SELECT 
                                                                    {self.db_config['database']}.NEWS.news_id,
                                                                    {self.db_config['database']}.SUMMARY.summary_text,
                                                                    {self.db_config['database']}.NEWS_COMPANY.company_id,
                                                                    {self.db_config['database']}.COMPANY.company_code,
                                                                    {self.db_config['database']}.COMPANY.name
                                                                FROM 
                                                                    {self.db_config['database']}.NEWS_COMPANY
                                                                JOIN 
                                                                    {self.db_config['database']}.NEWS ON {self.db_config['database']}.NEWS_COMPANY.news_id = {self.db_config['database']}.NEWS.news_id
                                                                JOIN 
                                                                    {self.db_config['database']}.SUMMARY ON {self.db_config['database']}.NEWS_COMPANY.news_id = {self.db_config['database']}.SUMMARY.news_id
                                                                JOIN 
                                                                    {self.db_config['database']}.COMPANY ON {self.db_config['database']}.NEWS_COMPANY.company_id = {self.db_config['database']}.COMPANY.company_id
                                                                WHERE 
                                                                    {self.db_config['database']}.NEWS.date BETWEEN '{self.start_time}' AND '{self.end_time}';
                                            """, 
                                            
                                            description='SELECT NEWS, SUMMARY MERGE TABLE')
        logger.info(f"NEWS, SUMMARY MERGE SELECT Done")
        
        # EMBEDDING 생성
        topic_info = self.preprocess_topic(merge_data)
        logger.info(f"MAKE EMBEDDING DONE")
         
        # TOPIC 테이블에 입력
        self.insert_data_to_db(query=f"INSERT INTO {self.db_config['database']}.{table_name} (topic_code, company_id, news_id_list, topic_date, startdate) \
                                                    VALUES (%(topic_code)s, %(company_id)s, %(news_id_list)s, %(topic_date)s, %(start_date)s)",
                               data=topic_info,
                               description=f'INSERT {table_name} TABLES')
        
        logger.info(f"INSERT {table_name} TABLE END : {start_time} ~ {end_time}")


    def fill_news_topic(self):
        table_name = 'NEWS_TOPIC'
        start_time, end_time = self.start_time.strftime('%Y-%m-%d %H:%M:%S'), self.end_time.strftime('%Y-%m-%d %H:%M:%S')
        logger.info(f"INSERT {table_name} TABLE START : {start_time} ~ {end_time}")
        
        topic_data = self.select_data_from_db(query = f"SELECT * FROM {self.db_config['database']}.TOPIC WHERE startdate BETWEEN '{self.start_time}' AND '{self.end_time}';", 
                                                    description='SELECT TOPIC TABLE')
        logger.info(f"{table_name} SELECT Done")

        news_topic_info = self.preprocess_news_topic(topic_data)
        logger.info(f"{table_name} PREPROCESS Done")
        
        # TOPIC_NEWS 테이블 입력
        self.insert_data_to_db(query=f"INSERT INTO {self.db_config['database']}.{table_name} (news_id, topic_id) VALUES (%(news_id)s, %(topic_id)s)",
                               data=news_topic_info,
                               description=f'INSERT {table_name} TABLES')
        
        logger.info(f"INSERT {table_name} TABLE END : {start_time} ~ {end_time}")
        
        
    def fill_topic_summary(self):
        table_name = 'TOPIC_SUMMARY'
        start_time, end_time = self.start_time.strftime('%Y-%m-%d %H:%M:%S'), self.end_time.strftime('%Y-%m-%d %H:%M:%S')
        logger.info(f"INSERT {table_name} TABLE START : {start_time} ~ {end_time}")
        merge_data = self.select_data_from_db(query = f"""
                                                            SELECT T.topic_id,
                                                                T.startdate,
                                                                T.max_news_id,
                                                                {self.db_config['database']}.NEWS.title,
                                                                {self.db_config['database']}.SUMMARY.summary_text
                                                            FROM (
                                                                SELECT {self.db_config['database']}.NEWS_TOPIC.topic_id, 
                                                                       {self.db_config['database']}.TOPIC.startdate, 
                                                                       MAX({self.db_config['database']}.NEWS_TOPIC.news_id) AS max_news_id
                                                                FROM {self.db_config['database']}.NEWS_TOPIC
                                                                JOIN {self.db_config['database']}.TOPIC ON {self.db_config['database']}.NEWS_TOPIC.topic_id = {self.db_config['database']}.TOPIC.topic_id
                                                                WHERE {self.db_config['database']}.TOPIC.startdate BETWEEN '{self.start_time}' AND '{self.end_time}'
                                                                GROUP BY {self.db_config['database']}.NEWS_TOPIC.topic_id
                                                            ) AS T
                                                            JOIN {self.db_config['database']}.NEWS ON T.max_news_id = {self.db_config['database']}.NEWS.news_id
                                                            JOIN {self.db_config['database']}.SUMMARY ON T.max_news_id = {self.db_config['database']}.SUMMARY.news_id;
                                                        """, 
                                                description='SELECT NEWS, SUMMARY, TOPIC, NEWS_TOPIC MERGE TABLE')
        logger.info(f"{table_name} SELECT DONE")
        
        topic_summary_info = self.preprocess_topic_summary(merge_data)
        logger.info(f"{table_name} PREPROCESS DONE")
        
        # TOPIC_SUMMARY 테이블 입력
        self.insert_data_to_db(query=f"INSERT INTO {self.db_config['database']}.{table_name} (topic_id, topic_title_summary, topic_summary) \
                                                VALUES (%(topic_id)s, %(topic_title_summary)s, %(topic_summary)s)",
                               data=topic_summary_info,
                               description=f'INSERT {table_name} TABLES')
    
        logger.info(f"INSERT {table_name} TABLE END : {start_time} ~ {end_time}")
        
    
    def fill_topic_image(self):
        table_name = 'TOPIC_IMAGE'
        start_time, end_time = self.start_time.strftime('%Y-%m-%d %H:%M:%S'), self.end_time.strftime('%Y-%m-%d %H:%M:%S')
        logger.info(f"INSERT {table_name} TABLE START : {start_time} ~ {end_time}")
        
        topic_data = self.select_data_from_db(query = f"SELECT * FROM {self.db_config['database']}.TOPIC WHERE startdate BETWEEN '{self.start_time}' AND '{self.end_time}';", 
                                                    description='SELECT TOPIC TABLE')
        logger.info(f"{table_name} SELECT DONE")
        
        topic_image_info = self.preprocess_topic_image(topic_data)
        logger.info(f"{table_name} PREPROCESS DONE")
        
        # TOPIC_IMAGE 테이블에 입력
        self.insert_data_to_db(query=f"INSERT INTO {self.db_config['database']}.{table_name} (topic_id, image_url) VALUES (%(topic_id)s, %(image_url)s)",
                               data=topic_image_info,
                               description=f'INSERT {table_name} TABLES')
        logger.info(f"INSERT {table_name} TABLE END : {start_time} ~ {end_time}")
        
        
    def preprocess_news(self):
        df_main = pd.read_csv('./data/mainnews_all.csv')
        df_company = pd.read_csv('./data/companynews_all.csv')
        df_disclosure = pd.read_csv('./data/disclosurenews_all.csv')
        df_economy = pd.read_csv('./data/economynews_all.csv')

        # 데이터 전처리
        df_news = pd.concat([df_main, df_company, df_disclosure, df_economy])
        df_news = df_news[['datetime', 'url', 'real_title', 'contents', 'relate_stock']].rename({'real_title' : 'title', 'datetime' : 'date'}, axis=1)

        # 수집하는 기간에 해당하는 뉴스 확인, datetime 형식 변경 : 오후 12시 : 24시 --> 12시
        df_news['date'] = pd.to_datetime(df_news['date'].apply(lambda x : x.replace("24:", "12:")))
        df_news = df_news[(df_news['date'] >= self.start_time) & (df_news['date'] < self.end_time)]
        df_news = df_news.sort_values(by='date')

        # url 기준으로 중복 뉴스 제거
        df_news.drop_duplicates(subset=['url'], inplace=True)
        df_news.reset_index(drop=True, inplace=True)

        # relate_stock 전처리 : SK, LG, KT는 5번 이상 나와야 인정하고 나머지는 1번만 나와도 인정하자./ ,으로 연결
        df_news['relate_stock'] = df_news['relate_stock'].apply(lambda x : self.new_relate_news(eval(x)))
        df_news = df_news[df_news['relate_stock'].apply(lambda x : len(x) > 0)]
        df_news['relate_stock'] = df_news['relate_stock'].apply(lambda lst : reduce(lambda acc, cur : acc+','+cur, lst))

        # contents가 NaN이고, title에 [속보]가 포함되면 contents에 title을 넣음.
        mask = (df_news['title'].str.contains('속보')) & (df_news['contents'].isna())
        df_news.loc[mask, 'contents'] = df_news.loc[mask, 'title']

        # contents 길이가 5000이하인 뉴스들만 선별
        df_news = df_news[df_news['contents'].apply(lambda x : len(x) < 5000)]
        df_news.reset_index(drop=True, inplace=True)
        
        news_info = df_news.to_dict(orient='index')
        news_info = [news_info[idx] for idx in news_info]
    
        return news_info
    
            
    # NEWS_COMPANY 전처리
    def preprocess_news_company(self, news_data, company_data):
        """news_table과 company_table에서 조회한 데이터를 활용하여, news_company 데이터의 입력 데이터를 생성"""
        company_info, news_company_info = {}, []
        for info in company_data:
            company_info[info['name']] = info['company_id']

        for info in news_data:
            news_id, relate_stocks = info['news_id'], info['relate_stock'].split(',')
            for stock in relate_stocks:
                news_company_info.append({'news_id': news_id, 'company_id' : company_info[stock]})
        
        return news_company_info
    
    
    def preprocess_summary(self, news_data, model_path='./model/summary/summary_model.pt', pretrained_model_name_or_path="EbanLee/kobart-summary-v2"):
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        # tokenizer 및 모델 로드
        tokenizer = AutoTokenizer.from_pretrained(pretrained_model_name_or_path)
        model = BartForConditionalGeneration.from_pretrained(pretrained_model_name_or_path)
        model.to(device)
        model.eval()
        summary_info = [] 
        with torch.no_grad():
            for i in tqdm(range((len(news_data) // 30) + 1), desc='SUMMARY WORKING'):
                s_i, e_i = i*30, min((i+1)*30, len(news_data)+1)
                news_id_list = [data['news_id'] for data in news_data[s_i:e_i]]
                contents_list = [data['contents'] for data in news_data[s_i:e_i]]

                # input data encoding
                inputs = tokenizer.batch_encode_plus(contents_list, 
                                                    return_tensors="pt", 
                                                    padding=True, 
                                                    truncation=True, 
                                                    max_length=1026).to(device)

                outputs = model.generate(inputs['input_ids'], 
                                            bos_token_id=tokenizer.bos_token_id,
                                            eos_token_id=tokenizer.eos_token_id,
                                            length_penalty=2.0,
                                            max_length=300,
                                            min_length=50,
                                            num_beams=6,).to("cpu")
                
                decoded_output = tokenizer.batch_decode(outputs, skip_special_tokens=True)
                
                for news_id, summary_text in zip(news_id_list, decoded_output):
                    summary_info.append({'news_id' : news_id, 'summary_text':summary_text})

        # GPU 메모리 정리
        torch.cuda.empty_cache()
        return summary_info
    
    
    def preprocess_sentiemnt(self, news_data, model_path='./model/sentiment', pretrained_model_name_or_path='./model/sentiment'):
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        tokenizer = AutoTokenizer.from_pretrained(pretrained_model_name_or_path)
        model = AutoModelForSequenceClassification.from_pretrained(pretrained_model_name_or_path, 
                                                                num_labels=3)
        model.to(device)
        model.eval()
        
        sentiment_info = []
        with torch.no_grad():
            for i in tqdm(range((len(news_data) // 30) + 1), desc='SUMMARY WORKING'):
                s_i, e_i = i*30, min((i+1)*30, len(news_data)+1)
                news_id_list = [data['news_id'] for data in news_data[s_i:e_i]]
                title_list = [data['title'] for data in news_data[s_i:e_i]]
                
                # Tokenizing Inputs and Predict
                input = tokenizer(title_list, truncation=True, padding=True, return_tensors='pt').to(device)
                outputs = model(**input)
                predicted_class = torch.argmax(outputs.logits, dim=-1).to('cpu')
                
                for news_id, sentiment in zip(news_id_list, predicted_class.numpy()):
                    sentiment_info.append({'news_id' : news_id, 'sentiment_value' : sentiment})

        torch.cuda.empty_cache()
        return sentiment_info
     

    def preprocess_topic(self, merge_data):
        df_merge = self.get_embedding_vector(merge_data, model_name = 'leewaay/kpf-bert-base-klueNLI-klueSTS-MSL512')
        
        topic_info = []
        for stock in ['전체'] + df_merge['name'].unique().tolist():
            
            # 전체 종목 클러스터링
            if stock == '전체':
                df_stock = df_merge.copy()
                # news_id 마다 여러 company_id에 매핑되어있다. news_id를 기준으로 중복 제거처리.
                df_stock = df_stock.drop_duplicates(subset=['news_id']).reset_index(drop=True)
                stock_name, company_id, topic_date = '전체', '0', datetime.strptime(self.today, '%Y-%m-%d')
                
            else:
                df_stock = df_merge[df_merge['name'] == stock].copy()
                stock_name, company_id, topic_date = df_stock['name'].unique()[0], df_stock['company_id'].unique()[0], datetime.strptime(self.today, '%Y-%m-%d')
                
            # logger.info(f"Stock : {stock} Clustering Start, Count : {len(df_stock)} ")
            if len(df_stock) == 1:
                topic_code = f"{stock_name}_{self.topic_n}_0"
                news_id_list = str(df_stock['news_id'].unique()[0])
                topic_info.append({
                                        'topic_code' : topic_code,
                                        'company_id' : company_id,
                                        'news_id_list': news_id_list,
                                        'topic_date' : topic_date,
                                        'start_date' : self.start_time,
                })
                
            else:
                embedding = df_stock['embedding'].tolist()
                df_clustering, topic_counter = self.clustering(df_stock, embedding, min_cluster_size=2, min_samples=1, method='leaf')
                
                # topic 별로 내용 추출 
                for topic in topic_counter:
                    df_topic = df_clustering[df_clustering['Topic'] == topic].copy()
                    topic_code = f"{stock_name}_{self.topic_n}_{topic}"
                    news_id_list = ','.join(map(lambda x : str(x), df_topic['news_id'].tolist()))
                    
                    # NEWS, Topic 별 내용 저장
                    topic_info.append({
                                            'topic_code' : topic_code,
                                            'company_id' : company_id,
                                            'news_id_list': news_id_list,
                                            'topic_date' : topic_date,
                                            'start_date' : self.start_time,
                                            })
                    
        return topic_info
    
    def preprocess_news_topic(self, topic_data):
        news_topic_lst = []

        for info in topic_data:
            topic_id, news_id_lst = info['topic_id'], info['news_id_list'].split(',')
            news_topic_lst.extend([{'news_id' : news_id, 'topic_id' : topic_id} for news_id in news_id_lst])
        return news_topic_lst
    
    
    # [TODO] topic_title, topci_summary는 추후 수정 가능
    def preprocess_topic_summary(self, merge_data):
        topic_summary_info = [{'topic_id' : ts_data['topic_id'], 
                                'topic_title_summary' : ts_data['title'],
                                'topic_summary' : ts_data['summary_text']} for ts_data in merge_data]
        return topic_summary_info

    
    
    # [TODO] topic url은 추후 crawling을 통해서 수집
    def preprocess_topic_image(self, topic_data):
        image_url = 'https://imgnews.pstatic.net/image/016/2024/03/05/20240305050255_0_20240305103801168.jpg?type=w647'
        topic_image_info = [{'topic_id' :data['topic_id'], 'image_url' : image_url} for data in topic_data] 
        return topic_image_info


    def get_embedding_vector(self, summary_data, model_name = 'leewaay/kpf-bert-base-klueNLI-klueSTS-MSL512'):
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        model = SentenceTransformer(model_name).to(device)
        
        df_merge = pd.DataFrame(summary_data)
        df_merge['embedding'] = df_merge['summary_text'].progress_apply(model.encode)
        
        # GPU 메모리 정리
        torch.cuda.empty_cache()
        return df_merge

    # HDBSCAN 실행
    def clustering(self, corpus, corpus_embeddings, min_cluster_size=2, min_samples=1, method='leaf'):
        cluster = hdbscan.HDBSCAN(min_cluster_size=min_cluster_size,
                                min_samples=min_samples,
                                metric='euclidean',
                                allow_single_cluster=True,
                                cluster_selection_method=method,
                                ).fit(corpus_embeddings) #eom leaf

        docs_df = corpus.copy()
        docs_df['Topic'] = cluster.labels_    
        return docs_df, Counter(cluster.labels_)


    async def crawling_news(self):
        # 데이터 수집
        loop = asyncio.get_event_loop()
        client = RestClient(loop)
        crwaler = NewsCrawler(client)
        
        await asyncio.gather(
                crwaler.crawling_news_url(start_date=self.today, end_date=self.today, section='주요뉴스', save_dir=f'./data/mainnews_url.csv'),
                crwaler.crawling_news_url(start_date=self.today, end_date=self.today, section='기업/종목분석', save_dir=f'./data/companynews_url.csv'),
                crwaler.crawling_news_url(start_date=self.today, end_date=self.today, section='공시/메모', save_dir=f'./data/disclosurenews_url.csv')
            )
        crwaler.dynamic_crawling_news_url(start_date=self.today, end_date=self.today, save_dir=f'./data/economynews_url.csv')


        await asyncio.gather(
                crwaler.crawling_news_contents(url_data_path=f'./data/mainnews_url.csv', merge_data_path=f'./data/mainnews_all.csv'),
                crwaler.crawling_news_contents(url_data_path=f'./data/companynews_url.csv', merge_data_path=f'./data/companynews_all.csv'),
                crwaler.crawling_news_contents(url_data_path=f'./data/disclosurenews_url.csv', merge_data_path=f'./data/disclosurenews_all.csv'),
                crwaler.crawling_news_contents(url_data_path=f'./data/economynews_url.csv', merge_data_path=f'./data/economynews_all.csv')
            )
    
    
    def new_relate_news(self, lst):
        """수집한 new 데이터에서 관련 종목을 재선별"""
        relate_news = []
        counter = Counter(lst)

        for stock in counter:
            if stock in ['SK', 'LG', 'KT'] :
                if counter[stock] >= 5:
                    relate_news.append(stock)
            else:
                relate_news.append(stock)
        return relate_news



if __name__ == "__main__":    
    fix_seed()
    db_user, db_password, db_host, db_database, db_port = os.getenv('DB_USER'), os.getenv('DB_PASSWORD'), os.getenv('DB_HOST'), os.getenv('DB_DATABASE'), os.getenv('DB_PORT')
    engine = Engine(db_user=db_user, 
                        db_password=db_password, 
                        db_host=db_host, 
                        topic_n=0, 
                        db_database= db_database, 
                        db_port=db_port, 
                        period=24, 
                        day_diff=1)
    
    engine.fill_news()
    # engine.fill_summary()
    # engine.fill_sentiment()
    # engine.fill_topic()
    # engine.fill_news_topic()
    # engine.fill_topic_summary()
    # engine.fill_topic_image()
    