import FinanceDataReader as fdr
from collections import Counter
from functools import reduce
from pykrx import stock, bond

import time
import random
import numpy as np
import pandas as pd
import pymysql


from dotenv import load_dotenv
from datetime import datetime, timedelta

import os
from loguru import logger
import tenacity
from tqdm import tqdm
import argparse

load_dotenv()


class MacroEngine:
    def __init__(self, db_user, db_password, db_host, db_database='AUTOMATION', db_port=3306, day_diff = 0):
        # MySQL 서버 정보 설정
        self.db_config = {
            'user': db_user,
            'password': db_password,
            'host': db_host,
            'database': db_database,
            'port': int(db_port)  # MySQL 기본 포트
        }

        # 수집하는 시간 업데이트
        self.today = (datetime.now() - timedelta(days=day_diff)).strftime('%Y-%m-%d')
        logger.info(f"""Macro Automation Process Start {self.today}""")
    
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
    
    def fill_company_close(self):
        table_name = 'COMPANY_CLOSE'        
        logger.info(f"INSERT {table_name} TABLE START : {self.today}")        
        # COMPANY 데이터 조회 
        company_data = self.select_data_from_db(query = f"SELECT * FROM {self.db_config['database']}.COMPANY;", description='SELECT COMPANY TABLE')
        logger.info(f"COMPANY SELECT Done")
        
        # COMPANY 종가 데이터 수집
        company_close_info = self.preprocess_company_close(company_data)
        logger.info(f"{table_name} Preprocessing Done")
        
        # COMPANY_CLOSE 테이블 입력
        self.insert_data_to_db(query=f"INSERT INTO {self.db_config['database']}.{table_name} (date{reduce(lambda acc, cur: acc + f', `{cur}`', range(48, 94 + 1), '')}) VALUES (%(date)s{reduce(lambda acc, cur: str(acc) + f', %({cur})s', range(48, 94 + 1), '')})",
                               data=company_close_info,
                               description=f'INSERT {table_name} TABLES')
        logger.info(f"INSERT {table_name} TABLE DONE : {self.today}")
    
    
    def fill_company_price_info(self):
        table_name = 'COMPANY_PRICE_INFO'        
        logger.info(f"INSERT {table_name} TABLE START : {self.today}")        
        
        # COMPANY 데이터 조회 
        company_price_info_data = self.select_data_from_db(query = f"SELECT * FROM {self.db_config['database']}.COMPANY;", description='SELECT COMPANY TABLE')
        logger.info(f"COMPANY SELECT Done")
        
        # COMPANY 가격 정보 데이터 수집
        columns = ['date',  'company_id', 'company_code', 'name', '시가', '고가', '저가', '종가', '거래량', '등락률', '시가총액', '거래대금', 'BPS', 'PER', 'PBR', 'EPS', 'DIV', 'DPS', '상장주식수', '외국인보유수량', '외국인지분율', '외국인한도수량', '외국인한도소진률']

        company_price_info_info = self.preprocess_company_price_info(company_price_info_data, columns)
        logger.info(f"{table_name} Preprocessing Done")
        
        
        # COMPANY_PRICE_INFO 테이블 입력
        self.insert_data_to_db(query=f"INSERT INTO {self.db_config['database']}.{table_name} ({reduce(lambda acc, cur: acc + f', `{cur}`', columns)}) VALUES (%(date)s{reduce(lambda acc, cur: str(acc) + f', %({cur})s', columns[1:], '')})",
                               data=company_price_info_info,
                               description=f'INSERT {table_name} TABLES')
        logger.info(f"INSERT {table_name} TABLE DONE : {self.today}")
        
    
    def fill_economy_price_info(self):
        table_name = 'ECONOMY_PRICE_INFO'
        logger.info(f"INSERT {table_name} TABLE START : {self.today}")
        
        economy_price_info_info = self.preprocess_economy_price_info()
        logger.info(f"{table_name} Preprocessing Done")
        
        columns = ['date' ,'코스피' ,'코스피200' ,'코스닥' ,'금' ,'환율_원화' ,'환율_유로화' ,'다우존스' ,'나스닥' ,'SnP500' ,'WTI' ,'비트코인' ,'한국채권_5년물' ,'한국채권_10년물' ,'미국채권_5년물' ,'미국채권_10년물']        # ECONOMY_PRICE_INFO 테이블 입력
        self.insert_data_to_db(query=f"INSERT INTO {self.db_config['database']}.{table_name} ({reduce(lambda acc, cur: acc + f', `{cur}`', columns)}) VALUES (%(date)s{reduce(lambda acc, cur: str(acc) + f', %({cur})s', columns[1:], '')})",
                               data=economy_price_info_info,
                               description=f'INSERT {table_name} TABLES')
        logger.info(f"INSERT {table_name} TABLE DONE : {self.today}")
        
    
    
    def preprocess_company_price_info(self, company_price_info_data, columns):
        company_price_info_info = []
        day_diff7 = (datetime.strptime(self.today, '%Y-%m-%d') - timedelta(days=7)).strftime('%Y-%m-%d')

        for data in company_price_info_data:
            ticker = data['company_code']
            try:
                df_price = stock.get_market_ohlcv(day_diff7, self.today, ticker).reset_index()
                df_cap = stock.get_market_cap(day_diff7, self.today, ticker).drop(columns=['거래량', '상장주식수'], axis=1).reset_index()
                df_fundamental = stock.get_market_fundamental(day_diff7, self.today, ticker).reset_index()
                df_foreign = stock.get_exhaustion_rates_of_foreign_investment(day_diff7, self.today, ticker).reset_index()

                merge_df = pd.merge(left=df_price, right=df_cap, on='날짜', how='left')
                merge_df = pd.merge(left=merge_df, right=df_fundamental, on='날짜', how='left')
                merge_df = pd.merge(left=merge_df, right=df_foreign, on='날짜', how='left')
                merge_df.rename({'날짜' : 'date', '보유수량' : '외국인보유수량', '지분율':'외국인지분율', '한도수량':'외국인한도수량', '한도소진률' : '외국인한도소진률'}, axis=1, inplace=True)
                
                info = merge_df.fillna(0).iloc[-1, :].to_dict()
                info['company_id'], info['company_code'], info['name'] = data['company_id'], data['company_code'], data['name']
            except Exception as e:
                info = data
                for column in columns[4:]:
                    info[column] = 0                
                logger.error(f"{data} | ERROR : {e}")
            
            time.sleep(0.5)
            
            info['date'] = datetime.strptime(self.today, '%Y-%m-%d')
            company_price_info_info.append(info)
        
        return company_price_info_info
        
    
    def preprocess_company_close(self, company_data):
        company_close_info = {'date' : datetime.strptime(self.today, '%Y-%m-%d')}
        for data in company_data:
            try:
                day_diff2 = (datetime.strptime(self.today, '%Y-%m-%d') - timedelta(days=7)).strftime('%Y-%m-%d')
                close = fdr.DataReader(data['company_code'],  day_diff2, self.today).iloc[-1, 3]
                
            except Exception as e:
                close = 0
                print('ERROR', data, e)
            company_close_info[str(data['company_id'])] = close
        
        return [company_close_info]
    
    
    def preprocess_economy_price_info(self):
        day_diff6 = (datetime.strptime(self.today, '%Y-%m-%d') - timedelta(days=6)).strftime('%Y-%m-%d')
        economy_price_info_info = {'date' : self.today}
        
        column_ticker = [('코스피', 'KS11'), ('코스피200', 'KS200'), ('코스닥', 'KQ11'), ('금', 'GC=F'), ('환율_원화', 'USD/KRW'), 
                         ('환율_유로화', 'USD/EUR'), ('다우존스', 'DJI'), ('나스닥', 'IXIC'), ('SnP500', 'S&P500'), ('WTI', 'CL=F'), ('비트코인', 'BTC-KRW'),
                         ('미국채권_5년물', 'US5YT'), ('미국채권_10년물', 'US10YT')]
        for key, ticker in column_ticker:
            try:
                value = fdr.DataReader(ticker, day_diff6, self.today)['Close'].fillna(-100).values[-1]
            except:
                value = -100
            economy_price_info_info[key] = value
        
        date_str_nodash = self.today.replace('-', '')
        for key, ticker in [('한국채권_5년물', '국고채 5년'), ('한국채권_10년물', '국고채 10년')]:
            try:
                value = bond.get_otc_treasury_yields(date_str_nodash).loc[ticker, '수익률'] # 5년 만기 한국 국채 수익률
            except:
                value = -100
            economy_price_info_info[key] = value
        return [economy_price_info_info]
    
    def fill(self):
        self.fill_company_close()
        self.fill_company_price_info()
        self.fill_economy_price_info()
    
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--day_diff', type=int, default=0, help='day diff from now')
    args = parser.parse_args()
    
    db_user, db_password, db_host, db_database, db_port = os.getenv('DB_USER'), os.getenv('DB_PASSWORD'), os.getenv('DB_HOST'), os.getenv('DB_DATABASE'), os.getenv('DB_PORT')
    macro_engine = MacroEngine(db_user, db_password, db_host, db_database, db_port, day_diff = i)
    macro_engine.fill_economy_price_info()
    
    macro_engine.fill()
