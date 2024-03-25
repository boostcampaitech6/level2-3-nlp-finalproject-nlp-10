from fastapi import APIRouter, Depends 
from schema.request import Topic_titles_request, Topic_id_request
from schema.response import Topic_titles_response
from schema.dto import Topic_title_dto, Topic_titles_dto
from service.service_jh import Service_jh
from repository.repository_jh import Repository_jh
from database.orm import Topic, Topic_summary, News_topic, News, Summary, Sentiment
from typing import List, Tuple
from collections import Counter
from starlette.middleware.cors import CORSMiddleware
from datetime import date
from datetime import datetime, timedelta

router = APIRouter(prefix='/jh')

@router.get("/hi")
def hello():
    return "hello" 

def make_set(data):
    unique_topic_ids = set()
    unique_data = []
    for item in data:
        if item.topic_id not in unique_topic_ids:
            unique_topic_ids.add(item.topic_id)
            unique_data.append(item.news_id)
    return unique_data

def count_topic_occurrences(news_topics):
        topic_counts = Counter(topic.topic_id for topic in news_topics)
        print(topic_counts)
        return list(topic_counts.values())
    
def count_sentiment_occurrences(sentiments):
    sentiment_counts = Counter(entry["sentiment_value"] for entry in sentiments)
    most_common_value = max(sentiment_counts, key=sentiment_counts.get)
    return most_common_value[0]

def filter_topic_code(topics: List[Topic]):
    filtered_topics = [topic for topic in topics if not topic.topic_code.endswith('-1')]
    return filtered_topics

# 뉴스 요약 정보 불러오기 코드
@router.get("/get-titles")
def get_topic_titles_handler(
    # request: Topic_titles_request,
    start_date: date,
    end_date: date,
    company_id: int,
    repo: Repository_jh = Depends()
) : 
    # start_date = request.start_date
    # end_date = request.end_date
    # company_id = request.company_id
    
    # 요약 정보 불러오기
    topics : List[Topic_summary] = repo.get_topics_summary_by_date_and_company(start_date, end_date, company_id)
    
    # 토픽 당 뉴스 개수 세기
    news: List[News_topic] = repo.get_news_cnt_by_date_and_company(start_date, end_date, company_id)
    cnt = count_topic_occurrences(news)
    
    # 토픽 당 대표 뉴스 가져오기
    news = repo.get_news_by_date_and_company(start_date, end_date, company_id)  
    news = make_set(news)    
    news = repo.get_news_by_news_id(news) 
    
    # 뉴스에서 가장 많이 등장한 sentiment_value 가져오기
    sentiments = repo.get_news_sentiment_by_date_and_company(start_date, end_date, company_id)
    sentiment = count_sentiment_occurrences(sentiments)
    
    # topic, topic_title_summary, topic_summary, cnt를 response
    result = []
    for topic, num, new in zip(topics, cnt, news):
        new_dict = {
            "topic_id": topic.topic_id,
            "topic_title_summary": topic.topic_title_summary,
            "topic_summary": topic.topic_summary,
            "cnt":  num,
            "title": new,
            "sentiment": sentiment[0]
        }
        result.append(new_dict)
        
    result = sorted(result, key=lambda x: x["cnt"], reverse=True)     
        
    return result

# 2페이지 기업별 최신 뉴스 불러오기 코드
@router.get("/get-titles-desc")
def get_news_by_news_id_ordered_desc_by_date(
    # request: Topic_titles_request,
    company_id: int,
    repo: Repository_jh = Depends()
) : 
    # 요약 정보 불러오기
    summarys : List[Topic_summary] = repo.get_news_summary_by_company(company_id)
        
    return 1

#################### 기업으로 최신 뉴스 불러오기

# 기업으로 최신 뉴스 불러오기
@router.get("/get-recent-news")
def get_recent_news_by_company(
    company_id: int,
    repo: Repository_jh = Depends()
) : 
    # 뉴스, 요약, 감성 정보 불러오기
    news : List[News] = repo.get_news_by_company(company_id)
    summarys : List[Summary] = repo.get_news_summary_by_company(company_id)
    sentiments : List[Sentiment] = repo.get_news_sentiment_by_company(company_id)
    
    result = []
    for one, summary, sentiment in zip(news, summarys, sentiments):
        cnt : int = repo.get_news_cnt_in_topic_by_news(one.news_id)
        new_dict = {
            "news_id": one.news_id,
            "news_title": one.title,
            "summary": summary.summary_text,
            "sentiment": sentiment.sentiment_value,
            "cnt": cnt
        }
        result.append(new_dict)
        
    return result

# 기업으로 뉴스 요약 불러오기
@router.get("/get-news-summary")
def get_news_summary_by_company(
    company_id: int,
    repo: Repository_jh = Depends()
) : 
    # 요약 정보 불러오기
    summarys : List[Summary] = repo.get_news_summary_by_company(company_id)
        
    return summarys

# 기업으로 뉴스 불러오기
@router.get("/get-news-s")
def get_news_s_by_company(
    company_id: int,
    repo: Repository_jh = Depends()
) : 
    # 요약 정보 불러오기
    news : List[Summary] = repo.get_news_by_company(company_id)
        
    return news

# 기업으로 뉴스 감성 불러오기
@router.get("/get-news-sentiment")
def get_news_sentiment_by_company(
    company_id: int,
    repo: Repository_jh = Depends()
) : 
    # 요약 정보 불러오기
    sentiment : List[Summary] = repo.get_news_sentiment_by_company(company_id)
        
    return sentiment

# 뉴스로, 해당 뉴스가 속한 토픽에 할당된 뉴스 개수 불러오기
@router.get("/get-news-cnt-int-topic")
def get_news_cnt_in_topic_by_news(
    news_id: int,
    repo: Repository_jh = Depends()
) : 
    # 요약 정보 불러오기
    news_cnt : int = repo.get_news_cnt_in_topic_by_news(news_id)
        
    return news_cnt


# 기업과 날짜로 가장 핫한 토픽의 topic_summary 불러오기
@router.get("/get-last")
def get_topic_summary_by_date_and_company_last(
    repo: Repository_jh = Depends()
) : 
    
    # 현재 날짜
    today = datetime.now().date()

    # 어제 날짜 계산
    yesterday = today - timedelta(days=1)
    
    aDay = datetime.strptime('2023-11-01', '%Y-%m-%d').date()
    
    result = []
    for company in range(48, 95):
        # 요약 정보 불러오기
        topics : List[Topic_summary] = repo.get_topics_summary_by_date_and_company_last(company)
        
        # 토픽 당 뉴스 개수 세기
        news: List[News_topic] = repo.get_news_cnt_by_date_and_company_last(company)
        cnt = count_topic_occurrences(news)
        
        if cnt:  # 리스트가 비어 있는지 확인
            max_index = cnt.index(max(cnt))
        
        else:
            max_index = -1
        
        if(max_index != -1):
            new_dict = {
                "company_id": company,
                "topic_summary": topics[max_index].topic_summary
            }
        else:
            new_dict = {
                "company_id": company,
                "topic_summary": "데이터 없음"
            }    
        
        result.append(new_dict)  
        
    return result


# 기업으로 company_info 가져오기
@router.get("/get-company-info")
def get_company_info_by_company(
    company_id: int,
    repo: Repository_jh = Depends()
) : 
    # 요약 정보 불러오기
    company_info : int = repo.get_company_info_by_company(company_id)
        
    return company_info


# 가장 최근 경제 지표 값들 (economy_price_info) 가져오기
@router.get("/get-economy-info")
def get_economy_info_recent(   
    repo: Repository_jh = Depends()
) : 
    # 요약 정보 불러오기
    economy_info = repo.get_economy_price_info_recent()
        
    return economy_info 

# 가장 최근 경제 지표 값들 (economy_price_info)의 등략률 계산해서 반환하기
@router.get("/get-economy-info-updown-rate")
def get_economy_info_updown_rate(   
    repo: Repository_jh = Depends()
)  -> dict:
    # 요약 정보 불러오기
    economy_info_1day_before = repo.get_economy_price_info_recent()
    economy_info_2day_before = repo.get_second_economy_price_info()

    economy_index_list = ['코스피', '코스닥', '코스피200', '금', '비트코인', '다우존스', '나스닥', 'SnP500', 
                    '환율_원화', 'WTI', '한국채권_5년물', '한국채권_10년물', '미국채권_5년물', '미국채권_10년물']
    
    updown_rate_dict = {}
    for index_name in economy_index_list:
        value_1 = getattr(economy_info_1day_before , index_name, None)
        value_2 = getattr(economy_info_2day_before , index_name, None)
        updown_rate = (value_1 - value_2)/value_2*100
        updown_rate_dict[index_name + '_등락률'] = float(f"{updown_rate:.3f}") 
    return updown_rate_dict


# 기업의 최신 종가(close) 가격 불러오기 최근 90개
@router.get("/get-company-close-price-90", response_model=Tuple[List[str], List[int]])
def get_company_close_recent_90(
    company_id: int,     
    repo: Repository_jh = Depends()
) -> Tuple[List[str], List[int]]: 
    # 요약 정보 불러오기
    company_close_90 = repo.get_company_stock_close_price_recent_90day(company_id)
    
    # 날짜와 종가(close price)를 각각 분리하여 리스트 생성
    dates = [item[0].isoformat() for item in company_close_90]  
    close_prices = [item[1] for item in company_close_90]
    
    # 날짜 리스트와 종가 리스트를 튜플로 묶어 반환
    return dates, close_prices


@router.get("/get-topic-image-url")
def some_path_function(
    topic_id : int,
    repo: Repository_jh = Depends()
    ):

    return repo.get_topic_image_url_by_date_and_company(topic_id)


#############################################################################################################
# 테스트 코드
# 뉴스 요약 정보 불러오기 코드
@router.get("/get-news")
def get_news_handler(
    # request: Topic_titles_request,
    start_date: date,
    end_date: date,
    company_id: int,
    repo: Repository_jh = Depends()
) : 
    
    # 뉴스 불러오기
    news = repo.get_news_by_date_and_company(start_date, end_date, company_id)  
    news = make_set(news)    
    news = repo.get_news_by_news_id(news)
    return news 

# 테스트 코드
@router.get('/get-topics')
def get_topics_handler(
    request: Topic_titles_request,
    repo: Repository_jh = Depends()
):
    start_date = request.start_date
    end_date = request.end_date
    company_id = request.company_id
    topics : List[Topic] = repo.get_topics_by_date_and_company(start_date, end_date, company_id)
    return topics

# 테스트 코드
@router.get('/get-cnt')
def get_cnt_handler(
    request: Topic_id_request,
    repo: Repository_jh = Depends()
):
    topic_id = request.topic_id
    cnt: int = repo.get_news_cnt_id_by_topic(topic_id)
    return cnt

# 테스트 코드
@router.get('/get-cnt2')
def get_cnt_handler(
    request: Topic_titles_request,
    repo: Repository_jh = Depends()
):
    start_date = request.start_date
    end_date = request.end_date
    company_id = request.company_id
    cnt: List[News_topic] = repo.get_news_cnt_by_date_and_company(start_date, end_date, company_id)
    return count_topic_occurrences(cnt)

# 테스트 코드
@router.get('/get-summary')
def get_summarys_handler(
    request: Topic_id_request,
    repo: Repository_jh = Depends()
):
    topic_id = request.topic_id
    topic_title_summary = repo.get_topic_summary_by_topic(topic_id)
    return topic_title_summary

# 테스트 코드
@router.get('/get-summary2')
def get_summarys_handler(
    request: Topic_titles_request,
    repo: Repository_jh = Depends()
):
    start_date = request.start_date
    end_date = request.end_date
    company_id = request.company_id
    topics : List[Topic_summary] = repo.get_topics_summary_by_date_and_company(start_date, end_date, company_id)
    return topics

# 테스트 코드
@router.get('/get-sentiment')
def get_sentiment_handler(
    request: Topic_id_request,
    repo: Repository_jh = Depends()
):
    topic_id = request.topic_id
    sentiment = repo.get_news_sentiment_by_topic(topic_id)
    return sentiment

# 테스트 코드
def count_sentiment_occurrences(sentiments):
        sentiment_counts = Counter(sentiment.sentiment_value for sentiment in sentiments)
        most_common_sentiments = sentiment_counts.most_common()
        most_common_sentiment = most_common_sentiments[0]
        return most_common_sentiment

# 테스트 코드
@router.get('/get-sentiment2')
def get_sentiment_handler(
    # request: Topic_titles_request,
    start_date: date,
    end_date: date,
    company_id: int,
    repo: Repository_jh = Depends()
):
    
    sentiments = repo.get_news_sentiment_by_date_and_company(start_date, end_date, company_id)
    # sentiment = count_sentiment_occurrences(sentiments)
    return sentiments

