# pip install pykrx  # pykrx 설치
# pip install finance_datareader

import FinanceDataReader as fdr
import pandas as pd
from pykrx import bond
from time import sleep
from datetime import datetime
import os
import time

"""
# 경제지표 = 수집 항목 정리
1. 코스피
2. 코스닥
3. 코스피200
4. 금 -> 금 선물 (국제 금값)
5. 비트코인
6. 다우존스 지수
7. 나스닥 종합지수
8. S&P500 지수
9. 환율(달러) - 달러(원화, 유로화)
10. WTI - 원유 oil 가격
9. 한국 채권 (5, 10 년 물)
10.  미국 채권 (5, 10 년 물)
"""


# 날짜를 꼭 "yyyy-mm-dd" 형식으로 넣어야함
# 날짜 하루에 대한 지수 값을 가져다 주는 function 임
# 하루 수집에 1분도 안 걸림

def crawling_economy_close_price_by_day(date_str : str):
    KOSPI_INDEX = fdr.DataReader('KS11', date_str)['Close'].values[0]  # 코스피지수
    KOSPI_200_INDEX = fdr.DataReader('KS200', date_str)['Close'].values[0]   # 코스피 200 지수
    KOSDAQ_INDEX = fdr.DataReader('KQ11', date_str)['Close'].values[0]   # 코스닥 지수
    #print(KOSPI_INDEX, KOSPI_200_INDEX, KOSDAQ_INDEX)

    Gold = fdr.DataReader('GC=F', date_str)['Close'].values[0]  # 금 선물 (COMEX)
    Dollar_kr = fdr.DataReader('USD/KRW', date_str)['Close'].values[0]# 달러 원화
    Dollar_euro = fdr.DataReader('USD/EUR', date_str)['Close'].values[0] # 달러 유로화
    #print(Gold, Dollar_kr, Dollar_euro)

    DJ = fdr.DataReader('DJI', date_str)['Close'].values[0] # 다우존스 지수 (DJI - Dow Jones Industrial Average)
    NASDAQ = fdr.DataReader('IXIC', date_str)['Close'].values[0] # 나스닥 종합지수 (IXIC - NASDAQ Composite)
    SNP = fdr.DataReader('S&P500', date_str)['Close'].values[0] # S&P500 지수 (NYSE)
    #print(DJ, NASDAQ, SNP)

    WTI = fdr.DataReader('CL=F', date_str)['Close'].values[0] # WTI유 선물 Crude Oil (NYMEX)
    Bitcoin = fdr.DataReader('BTC-KRW', date_str)['Close'].values[0] # 비트코인
    #print(WTI, Bitcoin)

    date_str_nodash = date_str.replace('-', '')
    bond5_kr = bond.get_otc_treasury_yields(date_str_nodash).loc['국고채 5년', '수익률'] # 5년 만기 한국 국채 수익률
    bond10_kr = bond.get_otc_treasury_yields(date_str_nodash).loc['국고채 10년', '수익률'] # 10년 만기 한국 국채 수익률
    bond5_usa = fdr.DataReader('US5YT',  date_str)['Close'].values[0]  # 5년 만기 미국국채 수익률
    bond10_usa = fdr.DataReader('US10YT',  date_str)['Close'].values[0] # 10년 만기 미국국채 수익률
    #print(bond5_kr, bond10_kr, bond5_usa, bond10_usa)

    economy_table = pd.DataFrame({
        '코스피':[KOSPI_INDEX],
        '코스피200':[KOSPI_200_INDEX],
        '코스닥':[KOSDAQ_INDEX],
        '금_국제_선물':[Gold],
        '달러_원화':[Dollar_kr],
        '달러_유로':[Dollar_euro],
        '다우존스지수':[DJ],
        '나스닥':[NASDAQ],
        'S&P500':[SNP],
        'WTI_원유':[WTI],
        '비트코인':[Bitcoin],
        '국고채5년':[bond5_kr],
        '국고채10년':[bond10_kr],
        '미국채5년':[bond5_usa],
        '미국채10년':[bond10_usa]},
        index = [date_str])

    return economy_table

# 필요하시다면,,,
# 오늘의 날짜를 가져다주는 함수
def get_date_str():
    now = datetime.now()
    today_date = now.strftime('%Y-%m-%d')
    print('오늘 날짜 :', today_date)
    print('======='*5)
    return today_date

date = get_date_str()
crawling_economy_close_price_by_day(date)

