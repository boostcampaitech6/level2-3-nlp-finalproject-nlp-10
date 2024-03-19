from fastapi import APIRouter, Depends 
from schema.request import Topic_titles_request, Topic_id_request, News_cnt_request
from schema.response import Topic_titles_response
from schema.dto import Topic_title_dto, Topic_titles_dto
from service.service_jh import Service_jh
from repository.repository_jh import Repository_jh
from database.orm import Topic, Topic_summary, News_topic
from typing import List 
from collections import Counter

router = APIRouter(prefix='/jh')

@router.get("/hi")
def hello():
    return "hello" 

# 뉴스 요약 정보 불러오기 코드
@router.get("/get-titles")
def get_topic_titles_handler(
    request: Topic_titles_request,
    repo: Repository_jh = Depends()
) : 
    start_date = request.start_date
    end_date = request.end_date
    company_id = request.company_id
    
    # 요약 정보 불러오기
    topics : List[Topic_summary] = repo.get_topics_summary_by_date_and_company(start_date, end_date, company_id)
    
    # 토픽 당 뉴스 개수 세기
    news: List[News_topic] = repo.get_news_cnt_by_date_and_company(start_date, end_date, company_id)
    cnt = count_topic_occurrences(news)
    
    # 뉴스에서 가장 많이 등장한 sentiment_value 가져오기
    sentiments = repo.get_news_sentiment_by_date_and_company(start_date, end_date, company_id)
    sentiment = count_sentiment_occurrences(sentiments)
    
    # topic, topic_title_summary, topic_summary, cnt를 response
    result = []
    for topic, new in zip(topics, cnt):
        new_dict = {
            "topic_id": topic.topic_id,
            "topic_title_summary": topic.topic_title_summary,
            "topic_summary": topic.topic_summary,
            "cnt":  new
        }
        result.append(new_dict)
        
    return result

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
def count_topic_occurrences(news_topics):
        topic_counts = Counter(topic.topic_id for topic in news_topics)
        return list(topic_counts.values())

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
    request: Topic_titles_request,
    repo: Repository_jh = Depends()
):
    start_date = request.start_date
    end_date = request.end_date
    company_id = request.company_id
    sentiments = repo.get_news_sentiment_by_date_and_company(start_date, end_date, company_id)
    sentiment = count_sentiment_occurrences(sentiments)
    return sentiment

