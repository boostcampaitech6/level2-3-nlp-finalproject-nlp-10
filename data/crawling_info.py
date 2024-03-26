from tqdm.notebook import tqdm
from bs4 import BeautifulSoup as bs
from urllib.request import Request, urlopen
import requests
import re
import pandas as pd
import numpy as np

companydf =  pd.read_csv("/content/drive/MyDrive/level2-boostcamp-team10/level3/뉴스데이터/병합/kospi47.csv", dtype = object)
company_list = companydf['종목명'].to_list()
company_code_list = companydf['종목코드'].to_list()

def clear_text(aa):
    aa = aa.replace("\n", "")
    aa = aa.replace("\t", "")
    return aa

def get_stock_information(company_code : str, main_df):

    # 가져올 url 문자열로 입력
    url = 'https://finance.naver.com/item/main.naver?code=' + company_code

    # requests의 get함수를 이용해 해당 url로 부터 html이 담긴 자료를 받아옴
    response = requests.get(url)

    # 우리가 얻고자 하는 html 문서가 여기에 담기게 됨
    html_text = response.text

    # html을 잘 정리된 형태로 변환
    html = bs(html_text, 'html.parser')

    # 전일종가, 시고저가, 거래량
    주식가격 = html.find('table', {'class' : 'no_info'})
    전일종가 = clear_text(주식가격.select('tr > td.first > em > span.blind')[0].text)
    시가 = clear_text(주식가격.select('tr > td.first > em > span.blind')[1].text)
    고가 = clear_text(주식가격.select('tr > td > em > span.blind')[1].text)
    저가 = clear_text(주식가격.select('tr > td > em > span.blind')[5].text)
    거래량 = clear_text(주식가격.select('tr > td > em > span.blind')[3].text)

    # 시가총액
    시가총액정보 = html.find('table', {'summary' : '시가총액 정보'})
    시가총액 = clear_text(시가총액정보.select('tr.strong > td > em')[0].text)
    시가총액순위 = clear_text(시가총액정보.select('tr > td > em')[1].text) + '위'
   # print(시가총액, 시가총액순위)

    # 외국인한도주식
    외국인한도주식정보 = html.find('table', {'summary' : '외국인한도주식수 정보'})
    외국인한도주식수A = clear_text(외국인한도주식정보.select('tr > td > em')[0].text)
    외국인한도주식수B = clear_text(외국인한도주식정보.select('tr > td > em')[1].text)
    외국인소진율 = clear_text(외국인한도주식정보.select('tr > td > em')[2].text)   # B/A
    #print(외국인소진율, 외국인한도주식수A, 외국인한도주식수B)

    #투자의견
    투자의견정보 = html.find('table', {'summary' : '투자의견 정보'})
    try :
        투자의견 = clear_text(투자의견정보.select('tr > td > span.f_up > em')[0].text)
    except :
        투자의견 = np.NaN
    목표주가 = clear_text(투자의견정보.select('tr > td > em')[0].text)
    try :
        _52주최고 = clear_text(투자의견정보.select('tr > td > em')[1].text)
    except :
        _52주최고 = np.NaN
    try :
        _52주최저 = clear_text(투자의견정보.select('tr > td > em')[2].text)
    except :
        _52주최저 = np.NaN
    #print(투자의견, 목표주가, _52주최고, _52주최저)

    #PER, EPS
    PEREPS = html.find('table', {'summary' : 'PER/EPS 정보'})
    try :
        PER = clear_text(PEREPS.select('tr > td > em#_per')[0].text) + '배'
    except :
        PER = np.NaN
    EPS = clear_text(PEREPS.select('tr > td > em#_eps')[0].text) + '원'
    try :
        추정PER = clear_text(PEREPS.select('tr > td > em#_cns_per')[0].text) + '배'
    except :
        추정PER = np.NaN
    try :
        추정EPS = clear_text(PEREPS.select('tr > td > em#_cns_eps')[0].text) + '원'
    except :
        추정EPS = np.NaN
    try :
        PBR = clear_text(PEREPS.select('tr > td > em#_pbr')[0].text) + '배'
    except :
        PBR = np.NaN
    try :
        BPS = clear_text(PEREPS.select('tr > td > em')[5].text) + '원'
    except :
        BPS = np.NaN
    try :
        배당수익률 = clear_text(PEREPS.select('tr > td > em#_dvr')[0].text) + '%'
    except :
        배당수익률 = np.NaN
    #print(PER, EPS, 추정PER, 추정EPS, PBR, BPS, 배당수익률)

    #동일업종
    동일업종 = html.find('table', {'summary' : '동일업종 PER 정보'})
    동일업종PER = clear_text(동일업종.select('tr.strong > td > em')[0].text) + '배'
    try :
        동일업종등락률 = clear_text(동일업종.select('td.f_up > em')[0].text)
    except :
        동일업종등락률 = np.NaN

    main_df.loc[main_df['종목코드']==company_code, '전일종가'] = 전일종가
    main_df.loc[main_df['종목코드']==company_code, '시가'] = 시가
    main_df.loc[main_df['종목코드']==company_code, '고가'] = 고가
    main_df.loc[main_df['종목코드']==company_code, '저가'] = 저가
    main_df.loc[main_df['종목코드']==company_code, '거래량'] = 거래량
    main_df.loc[main_df['종목코드']==company_code, '시가총액'] = 시가총액
    main_df.loc[main_df['종목코드']==company_code, '시가총액순위'] = 시가총액순위
    main_df.loc[main_df['종목코드']==company_code, '외국인한도주식수A'] = 외국인한도주식수A
    main_df.loc[main_df['종목코드']==company_code, '외국인한도주식수B'] = 외국인한도주식수B
    main_df.loc[main_df['종목코드']==company_code, '외국인소진율'] = 외국인소진율
    main_df.loc[main_df['종목코드']==company_code, '투자의견'] = 투자의견
    main_df.loc[main_df['종목코드']==company_code, '목표주가'] = 목표주가
    main_df.loc[main_df['종목코드']==company_code, '52주최고'] = _52주최고
    main_df.loc[main_df['종목코드']==company_code, '52주최저'] = _52주최저
    main_df.loc[main_df['종목코드']==company_code, 'PER'] = PER
    main_df.loc[main_df['종목코드']==company_code, 'EPS'] = EPS
    main_df.loc[main_df['종목코드']==company_code, '추정PER'] = 추정PER
    main_df.loc[main_df['종목코드']==company_code, '추정EPS'] = 추정EPS
    main_df.loc[main_df['종목코드']==company_code, 'PBR'] = PBR
    main_df.loc[main_df['종목코드']==company_code, 'BPS'] = BPS
    main_df.loc[main_df['종목코드']==company_code, '배당수익률'] = 배당수익률
    main_df.loc[main_df['종목코드']==company_code, '동일업종PER'] = 동일업종PER
    main_df.loc[main_df['종목코드']==company_code, '동일업종등락률'] = 동일업종등락률

    return main_df

main_df=pd.DataFrame(columns=['종목명','종목코드',
                              '전일종가', '시가', '고가', '저가', '거래량',
                              '시가총액', '시가총액순위',
                              '외국인한도주식수A', '외국인한도주식수B', '외국인소진율',
                              '투자의견', '목표주가', '52주최고', '52주최저',
                              'PER', 'EPS', '추정PER', '추정EPS', 'PBR', 'BPS', '배당수익률',
                              '동일업종PER', '동일업종등락률'])
main_df['종목명'] = company_list
main_df['종목코드'] = company_code_list

for comp_code in company_code_list:
    print(comp_code)
    main_df = get_stock_information(comp_code, main_df)

print(main_df.head())


main_df.to_csv("/content/drive/MyDrive/level2-boostcamp-team10/level3/뉴스데이터/stock_price_info.csv", index = False)










