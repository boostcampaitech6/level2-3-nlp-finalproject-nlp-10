from sqlalchemy.orm import Session, aliased
from sqlalchemy import select, and_, func 
from fastapi import Depends
from database.connection import get_db
from database.orm import News, Sentiment, Topic, Topic_summary, Company, News_topic
from typing import List 

class Repository_jh:
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session
        
    # 날짜와 기업으로 토픽에 맞는 topic_summary 불러오기     
    def get_topics_summary_by_date_and_company(self, start_date, end_date, company_id) -> List[Topic_summary]:
        return self.session.query(Topic_summary).join(Topic, Topic_summary.topic_id == Topic.id).filter(and_(
                Topic.topic_date >= start_date,
                Topic.topic_date <= end_date,
                Topic.company_id == company_id
            )).all()
        
    # 날짜와 기업으로 토픽에 맞는 뉴스 불러오기    
    def get_news_cnt_by_date_and_company(self, start_date, end_date, company_id) -> List[News_topic]:
        return self.session.query(News_topic).join(Topic, News_topic.topic_id == Topic.id).filter(and_(
                Topic.topic_date >= start_date,
                Topic.topic_date <= end_date,
                Topic.company_id == company_id
            )).all()
        
    # 날짜와 기업으로 토픽의 뉴스들 sentiment들을 불러오기    
    def get_news_sentiment_by_date_and_company(self, start_date, end_date, company_id) -> List[any]:
        # return self.session.query(News_topic).join(Topic, News_topic.topic_id == Topic.id).filter(and_(
        #         Topic.topic_date >= start_date,
        #         Topic.topic_date <= end_date,
        #         Topic.company_id == company_id
        #     )).all()
    
        news_topic_alias = aliased(News_topic)
        news_alias = aliased(News)

        return self.session.query(Sentiment).\
            join(news_alias, Sentiment.news_id == news_alias.id).\
            join(news_topic_alias, news_alias.id == news_topic_alias.news_id).\
            join(Topic, news_topic_alias.topic_id == Topic.id).\
            filter(and_(
                Topic.topic_date >= start_date,
                Topic.topic_date <= end_date,
                Topic.company_id == company_id
            )).all()
        
    # 테스트 코드
    def get_topics_by_date_and_company(self, start_date, end_date, company_id) -> List[Topic]:
        return self.session.query(Topic).filter(
            and_(
                Topic.topic_date >= start_date,
                Topic.topic_date <= end_date,
                Topic.company_id == company_id
            )
        ).all()
        
    # 테스트 코드
    def get_topic_summary_by_topic(self, topic_id) -> Topic_summary:
        return self.session.query(Topic_summary).filter(Topic_summary.topic_id == topic_id).first() 
        
    # 테스트 코드
    def get_news_cnt_id_by_topic(self, topic_id) -> int:
        return self.session.query(func.count(News_topic.id)).filter(News_topic.topic_id == topic_id).scalar()
        
    # 테스트 코드
    def get_news_sentiment_by_topic(self, topic_id) -> int:
        news_topics = self.session.query(News_topic).filter(News_topic.topic_id == topic_id).all()
        news_topics_len = len(news_topics)
                    
        positives_len = (
            self.session.query(func.count(Sentiment.id))
            .join(News_topic, Sentiment.news_id == News_topic.news_id)
            .filter(News_topic.topic_id == topic_id, Sentiment.sentiment_value == 1)
            .scalar()
        )
                
        if positives_len > (news_topics_len / 2):
            return 1
                
        return 0
    
        
        
        
                
    
