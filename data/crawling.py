import os
import time
import itertools
import asyncio
import aiohttp
import orjson
from loguru import logger
from tqdm import tqdm

from collections import defaultdict
import datetime
import numpy as np
import pandas as pd


from typing import List, Union
from fake_useragent import UserAgent
from enum import Enum

from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from urllib.parse import urlparse, parse_qs

from selenium import webdriver
from selenium.webdriver.common.by import By
import tenacity

from preprocessing import Denoiser



class RestClient:
    def __init__(self, loop) -> None:
        self.ip_address : List[str] = ['0.0.0.0']
        user_agent = UserAgent()

        self.sessions = itertools.cycle([aiohttp.ClientSession(loop=loop,
                                                               headers={"User-Agent":user_agent.random},
                                                               json_serialize=orjson.dumps,
                                                               connector=aiohttp.TCPConnector(local_addr=(ip, 0))) for ip in self.ip_address]
                                        )
        
    async def get(self,
                  url,
                  params=None,
                  timeout=1,
                  headers=None) -> dict:
        async with next(self.sessions).get(url=url, params=params, timeout=timeout, headers=headers) as response:
            return await response.text()
        


class NewsCrawler:
    def __init__(self, client, kospi47_path:str='./utils/company.csv', krx_list_path='./utils/krxlist.csv') -> None:
        self.client = client
        self.denoiser = Denoiser()
        self.kospi47 = pd.read_csv(kospi47_path)['name'].tolist()
        krx_list = pd.read_csv(krx_list_path)['Name'].tolist()
        self.dupli_stock_info = self.get_dupli_stocks_info(self.kospi47, krx_list)



    def get_dupli_stocks_info(self, kospi47, krx_list) :
        """kodex100 종목 중 단어가 겹치는 종목 정보 저장 뒤에 관련 종목을 선별할 때 사용"""
        dupli_stock_info = defaultdict(list)
        for stock_query in kospi47:
            for stock_check in krx_list:
                if (stock_query != stock_check) and (stock_query in stock_check):
                    dupli_stock_info[stock_query].append(stock_check)
        
        dupli_stock_info['SK'].extend(['SK해운', 'SK에코플랜트'])
        dupli_stock_info['KT'].extend(['KTC', 'KT클라우드'])
        dupli_stock_info['하이브'].extend(['하이브리드'])


        return dupli_stock_info


    def generate_date_list(self, start_date, end_date)-> List[str]:
        "url에 넣어줄 날짜 정보 생성"
        date_list = []
        current_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')

        while current_date <= end_date:
            date_list.append(current_date.strftime('%Y-%m-%d'))
            current_date += timedelta(days=1)
        return date_list
    
    
    def save_crawling_data(self, crawling_info:List[dict], save_dir:str)->None:
        df_crawling = pd.DataFrame(crawling_info)
        df_crawling.to_csv(save_dir, index=False)


    def find_relate_stock(self, text:str)-> List:
        """text 안에 kospi47 종목들이 포함되어 있는지 확인하고 있다면 list로 반환"""
        relate_stock = []
        for stock_query in self.kospi47:
            idx = text.find(stock_query)

            # stock이 text(제목, 내용)에 여러번 등장 할 수 있으므로 모두 체크.
            while idx >= 0:
                dupli_flag = False
                # 종목의 중복을 검토해야하는지 확인. "카카오"가 "카카오뱅크"에서 "카카오"를 추출한건지 확인
                if stock_query in self.dupli_stock_info:
                    for stock_check in self.dupli_stock_info[stock_query]:
                        if stock_check == text[idx:idx+len(stock_check)]:
                            dupli_flag = True
                            break
                
                if not dupli_flag:
                    relate_stock.append(stock_query)
                
                idx = text.find(stock_query, idx+1)
        
        return relate_stock



    @tenacity.retry(wait=tenacity.wait_fixed(1), stop=tenacity.stop_after_attempt(5))
    async def crawling_mainnews(self, section, date, page, date_urls, crawling_info):
        "date와 page가 주어졌을 때 네이버 금융 주요뉴스 제목, url 크롤링하는 함수"
        new_page = False
        try:
            # 주요 뉴스 목차 URL 생성
            url = f'https://finance.naver.com/news/mainnews.naver?date={date}&page={page}'
            
            response = await self.client.get(url = url)
            news_html = BeautifulSoup(response, "html.parser")
            
            # ul tag에 뉴스 리스트 존재
            ul_tag = news_html.select_one("#contentarea_left > div.mainNewsList._replaceNewsLink > ul")
            
            # 각 뉴스는 li tag안에 있음
            li_tags = ul_tag.find_all('li')
            
            for i in range(len(li_tags)):
                li_tag = li_tags[i]
                dl_tag = li_tag.find('dl')
                dd_tag = dl_tag.find('dd', class_='articleSubject')
                
                if dd_tag == None:
                    dd_tag = dl_tag.find('dt', class_='articleSubject')
        
                a_tag = dd_tag.find('a')
                a_tag_url = a_tag['href']
                title = dd_tag.get_text().strip()
                
                # URL 파싱
                parsed_url = urlparse(a_tag_url)
                query_params = parse_qs(parsed_url.query)
                
                # article_id와 office_id 값 출력
                article_id = query_params.get('article_id', [])[0]
                office_id = query_params.get('office_id', [])[0]
                
                # URL 형식에 맞게 변형
                url = f"https://n.news.naver.com/mnews/article/{office_id}/{article_id}"
                
                if url not in date_urls:
                    date_urls.add(url)
                    crawling_info.append({'section' : section, 'title' : title, 'date' : date, 'page' : page, 'url' : url})
                    
                    # 현재 페이지에 새로운 뉴스가 하나라도 있다면 new page로 인식
                    new_page = True
                    
        except Exception as e:
            logger.error(f"DATE : {date}, PAGE : {page}, URL : {url}, EXCEPTION : {e}")
            raise ValueError('CRAwLING NOT WORK')

        return date_urls, new_page, crawling_info



    @tenacity.retry(wait=tenacity.wait_fixed(1), stop=tenacity.stop_after_attempt(5))
    async def crawling_financenews(self, section, date, page, date_urls, crawling_info):
        "date와 page가 주어졌을 때 네이버 금융 기업/종목분석, 공시/메모 뉴스 제목, url 크롤링하는 함수"
        try:
            # url에 들어가는 날짜형식에 맞게 변환
            date, date_save_format = date.replace('-', ''), date
            new_page = False
            
            # 주요 뉴스 목차 URL 생성
            if section == '기업/종목분석':
                url = f'https://finance.naver.com/news/news_list.naver?mode=LSS3D&section_id=101&section_id2=258&section_id3=402&date={date}&page={page}'
            elif section == '공시/메모':
                url = f'https://finance.naver.com/news/news_list.naver?mode=LSS3D&section_id=101&section_id2=258&section_id3=406&date={date}&page={page}'
            
            response = await self.client.get(url = url)
            news_html = BeautifulSoup(response, "html.parser")
            
            # ul tag에 뉴스 리스트 존재
            ul_tag = news_html.select_one("#contentarea_left > ul")
            # 각 뉴스는 li tag안에 있음
            li_tags = ul_tag.find_all('li')
            
            for li_tag in li_tags:
                dl_tag = li_tag.find('dl')
                
                # 뉴스 기사가 dd tag 또는 dt tag에 존재해있음.
                dd_tags = dl_tag.find_all('dd', class_='articleSubject')
                dt_tags = dl_tag.find_all('dt', class_='articleSubject')
                dd_dt_tags = dd_tags + dt_tags
                
                for dd_tag in dd_dt_tags:
                    a_tag = dd_tag.find('a')
                    a_tag_url = a_tag['href']
                    title = dd_tag.get_text().strip()
                    
                    # URL 파싱
                    parsed_url = urlparse(a_tag_url)
                    query_params = parse_qs(parsed_url.query)
                    
                    # article_id와 office_id 값 출력
                    article_id = query_params.get('article_id', [])[0]
                    office_id = query_params.get('office_id', [])[0]
                    
                    # URL 형식에 맞게 변형
                    url = f"https://n.news.naver.com/mnews/article/{office_id}/{article_id}"
                    
                    if url not in date_urls:
                        date_urls.add(url)
                        crawling_info.append({'section' : section, 'title' : title, 'date' : date_save_format, 'page' : page, 'url' : url})
                        
                        # 현재 페이지에 새로운 뉴스가 하나라도 있다면 new page로 인식
                        new_page = True

        except Exception as e:
            logger.error(f"DATE : {date}, PAGE : {page}, URL : {url}, EXCEPTION : {e}")
            raise ValueError('CRAwLING NOT WORK')

        return date_urls, new_page, crawling_info


    @tenacity.retry(wait=tenacity.wait_fixed(1), stop=tenacity.stop_after_attempt(5))
    async def crawling_contents_from_url(self, url):
        """url에 접근해서 제목, 내용, 일자를 크롤링하는 함수"""
        try:
            response = await self.client.get(url=url)
            news_html = BeautifulSoup(response, "html.parser")
            
            # 뉴스 제목 가져오기
            title = news_html.select_one("#ct > div.media_end_head.go_trans > div.media_end_head_title > h2")
            if title == None:
                title = news_html.select_one("#content > div.end_ct > div > h2")

            title = title.get_text()

            date = news_html.select_one("#ct > div.media_end_head.go_trans > div.media_end_head_info.nv_notrans > div.media_end_head_info_datestamp > div:nth-child(1) > span")
            date = date.get_text()

            # 뉴스 본문 가져오기
            contents = news_html.select("article#dic_area")
            if contents == []:
                contents = news_html.select("#articeBody")
                
            contents = contents[0].get_text()
        
        except Exception as e:
            raise ValueError("CRAwLING NOT WORK")
        
        return title, date, contents



    async def crawling_news_url(self, start_date:str, end_date:str, section:str='기업/종목분석', save_dir:str='./data/crawling_url/companynews.csv')->None:
        """기업/종목분석, 공시/메모 뉴스 url 크롤러"""
        logger.info(f"{section} NEWS CRAwLING START!!")

        crawling_info, total_cnt = [], 0
        date_list = self.generate_date_list(start_date, end_date)

        for date in tqdm(date_list) :
            date_urls, page = set(), 1
            
            while True:
                if section == '주요뉴스':
                    # date, page에 해당하는 정보 크롤링
                    date_urls, new_page, crawling_info = await self.crawling_mainnews(section, date, page, date_urls, crawling_info)
                else:
                    # date, page에 해당하는 정보 크롤링
                    date_urls, new_page, crawling_info = await self.crawling_financenews(section, date, page, date_urls, crawling_info)

                if new_page:
                    page += 1
                else:
                    # logger.info(f"DATE : {date}, LAST PAGES : {page-1}, NEWS CNT : {len(date_urls)}")
                    total_cnt += len(date_urls)
                    break


        logger.info(f"MAIN NEWS CRAwLING END!! - TOTAL URL : {total_cnt}")

        # save crawling data
        self.save_crawling_data(crawling_info, save_dir)
        logger.info(f"MAIN NEWS CRAWLING DATA SAVED!! DIR : {save_dir}")


    def dynamic_crawling_news_url(self, start_date:str, end_date:str, save_dir:str='./data/crawling_url/stock_relate_news.csv') -> None:
        """네이버 경제 뉴스 url 크롤러"""
        logger.info(f"ECONOMY NEWS CRAWLING START!!")
        
        driver = webdriver.Chrome()
        crawling_info, total_cnt = [], 0
        date_list = self.generate_date_list(start_date, end_date)
        # (1) 일자별로 접근하고
        for date in tqdm(date_list):
            try:
                driver.get(f"https://news.naver.com/breakingnews/section/101/261?date={date.replace('-', '')}")
                
                news_list_div = None
                # (2) 각 일자에 '기사 더보기' 계속 클릭하고 모든 기사를 UI에 띄우기.
                while True:
                    try:
                        before_news_list_div = news_list_div if news_list_div else None
                        driver.find_element(By.XPATH, '//*[@id="newsct"]/div[2]/div/div[2]/a').click()
                        news_list_div = driver.find_elements(By.XPATH, '//*[@id="newsct"]/div[2]/div/div[1]')

                        time.sleep(0.3)
                    except Exception as e:
                        if "Message: element not interactable" in str(e):
                            pass
                        else: 
                            logger.error(e)
                        break

                # (3) 모든 기사를 다 띄웠으면 각 기사에 접근하기.
                try:
                    news_group_list_div = news_list_div[0].find_elements(By.CSS_SELECTOR, 'div.section_article._TEMPLATE')
                # 마지막에 페이지가 이상하게 넘어가는 경우가 있음.
                except:
                    news_group_list_div = before_news_list_div[0].find_elements(By.CSS_SELECTOR, 'div.section_article._TEMPLATE')
                    logger.info(f"LAST PAGE ERROR : Replace to Before page, DATE : {date}")

                for news_group in news_group_list_div:
                    for news in news_group.find_elements(By.CSS_SELECTOR, 'div.sa_text'):
                        title = news.text.split('\n')[0]

                        a_tag = news.find_element(By.TAG_NAME, 'a')
                        # # a 태그의 href 속성 가져오기
                        url = a_tag.get_attribute('href')
                        crawling_info.append({'title' : title, 'url' :url})
            
            except Exception as e:
                logger.error(f'DATE : {date}, {e}')
        
        logger.info(f"ECONOMY NEWS CRAWLING END!! - TOTAL URL : {total_cnt}")

        # save crawling data
        self.save_crawling_data(crawling_info, save_dir)
        logger.info(f"ECONOMY NEWS CRAWLING DATA SAVED!! DIR : {save_dir}")



    async def crawling_news_contents(self, url_data_path:str, merge_data_path:str)->None:
        """url 정보를 받아서 뉴스를 제목, 내용, 날짜를 가져오는 함수"""
        crawling_info = []
        df_url = pd.read_csv(url_data_path)

        for url in tqdm(df_url['url']):
            try:
                title, date, contents = await self.crawling_contents_from_url(url)
                # 여기에 전처리 함수 추가하기.
                contents = self.denoiser.remove_space(contents)
                date = f"{date.split(' ')[0][0:4]}-{date.split(' ')[0][5:7]}-{date.split(' ')[0][8:10]} {int(date.split(' ')[2][:-3]) + (0 if date.split(' ')[1] == '오전' else 12)}:{date.split(' ')[2][-2:]}"
                
                # 뉴스 제목, 내용 안에 kospi47 종목이 포함되는지 확인
                relate_stock_from_title = self.find_relate_stock(title)
                relate_stock_from_contents = self.find_relate_stock(contents)
                relate_stock = relate_stock_from_title + relate_stock_from_contents
                
                # 관련 종목이 있는 경우에만 저장
                if relate_stock:
                    crawling_info.append({'url' : url, 'relate_stock' : relate_stock, 'real_title' : title, 'contents' : contents, 'datetime' :date})
            except:
                continue

        df_contents = pd.DataFrame(crawling_info)
        df_merge = pd.merge(left=df_url, right=df_contents, on='url').dropna()
        df_merge = df_merge.drop_duplicates(subset=['url'])
        df_merge.to_csv(merge_data_path, index=False)



async def main(startdate, enddate):

    loop = asyncio.get_event_loop()
    client = RestClient(loop)
    crwaler = NewsCrawler(client)

    path_back = f'{startdate.replace("-", "")}_{enddate.replace("-", "")}.csv'
    await asyncio.gather(
        crwaler.crawling_news_url(start_date=startdate, end_date=enddate, section='주요뉴스', save_dir=f'./data/crawling_url/mainnews_{path_back}'),
        crwaler.crawling_news_url(start_date=startdate, end_date=enddate, section='기업/종목분석', save_dir=f'./data/crawling_url/companynews_{path_back}'),
        crwaler.crawling_news_url(start_date=startdate, end_date=enddate, section='공시/메모', save_dir=f'./data/crawling_url/disclosurenews_{path_back}')
    )

    crwaler.dynamic_crawling_news_url(start_date=startdate, end_date=enddate, save_dir=f'./data/crawling_url/economynews_{path_back}')

    await asyncio.gather(
        crwaler.crawling_news_contents(url_data_path=f'./data/crawling_url/mainnews_{path_back}', merge_data_path=f'./data/crawling_all/mainnews_{path_back}'),
        crwaler.crawling_news_contents(url_data_path=f'./data/crawling_url/companynews_{path_back}', merge_data_path=f'./data/crawling_all/companynews_{path_back}'),
        crwaler.crawling_news_contents(url_data_path=f'./data/crawling_url/disclosurenews_{path_back}', merge_data_path=f'./data/crawling_all/disclosurenews_{path_back}'),
        crwaler.crawling_news_contents(url_data_path=f'./data/crawling_url/economynews_{path_back}', merge_data_path=f'./data/crawling_all/economynews_{path_back}')

    )
    

if __name__ == "__main__":
    startdate = '2024-02-13'
    enddate = '2024-02-23'


    asyncio.run(main(startdate, enddate))