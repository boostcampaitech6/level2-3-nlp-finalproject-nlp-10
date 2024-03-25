from sqlalchemy.orm import Session, aliased
from sqlalchemy import select, and_, func, not_ 
from schema.response import TopicImageURLResponse
from fastapi import Depends
from database.connection import get_db
from database.orm import News, Sentiment, Topic, Topic_summary, Company, News_topic, Topic_image, Summary, News_company, \
    Company_price_info, Economy_price_info, Company_Close_price
from typing import List 

class Repository_jh:
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session
        
    # 날짜와 기업으로 토픽에 맞는 topic_summary 불러오기     
    def get_topics_summary_by_company(self, company_id) -> List[Topic_summary]:
        return self.session.query(Topic_summary).join(Topic, Topic_summary.topic_id == Topic.topic_id).filter(and_(
                Topic.company_id == company_id
            )).all()    
        
    def get_news_cnt_by_company(self, company_id) -> List[News_topic]:
        return self.session.query(News_topic).join(Topic, News_topic.topic_id == Topic.topic_id).filter(and_(
                Topic.company_id == company_id
            )).all()    
        
    # 날짜와 기업으로 토픽의 뉴스들을 불러오기    
    def get_news_by_company_id(self, company_id):

        return self.session.query(News_topic).\
            join(Topic, News_topic.topic_id == Topic.topic_id).\
            filter(
                Topic.company_id == company_id,
            ).all()    
        
    #뉴스 아이디로 뉴스 내용 가져오기 + 날짜 내림차순으로 정렬    
    def get_news_ordered_desc_by_date(self, news_id):

        result = self.session.query(News.title).\
            filter(News.news_id.in_(news_id)).\
            order_by(News.date.desc()).all()
        
        return [row[0] for row in result]    
    
    # 기업으로 토픽의 뉴스들 sentiment들을 불러오기    
    def get_news_sentiment_by_company(self, company_id) -> List[any]:
    
        news_topic_alias = aliased(News_topic)
        news_alias = aliased(News)

        return self.session.query(Sentiment).\
            join(news_alias, Sentiment.news_id == news_alias.news_id).\
            join(news_topic_alias, news_alias.news_id == news_topic_alias.news_id).\
            join(Topic, news_topic_alias.topic_id == Topic.topic_id).\
            filter(
                Topic.company_id == company_id
            ).all()
        
    # 날짜와 기업으로 토픽에 맞는 topic_summary 불러오기     
    def get_topics_summary_by_date_and_company(self, start_date, end_date, company_id) -> List[Topic_summary]:
        return self.session.query(Topic_summary).join(Topic, Topic_summary.topic_id == Topic.topic_id).filter(and_(
                Topic.topic_date >= start_date,
                Topic.topic_date <= end_date,
                Topic.company_id == company_id,
                not_(Topic.topic_code.like('%-1'))
            )).all()
        
    # 날짜와 기업으로 토픽에 맞는 topic_summary 불러오기     
    def get_news_by_company(self, company_id) -> List[Topic_summary]:
        return self.session.query(Topic_summary).join(Topic, Topic_summary.topic_id == Topic.topic_id).filter(and_(
                Topic.company_id == company_id
            )).all()    
        
    # 날짜와 기업으로 토픽에 맞는 뉴스 불러오기    
    def get_news_cnt_by_date_and_company(self, start_date, end_date, company_id) -> List[News_topic]:
        return self.session.query(News_topic).join(Topic, News_topic.topic_id == Topic.topic_id).filter(and_(
                Topic.topic_date >= start_date,
                Topic.topic_date <= end_date,
                Topic.company_id == company_id,
                not_(Topic.topic_code.like('%-1'))
            )).all()
        
    # 날짜와 기업으로 토픽의 뉴스들 sentiment들을 불러오기    
    def get_news_sentiment_by_date_and_company(self, start_date, end_date, company_id) -> List[any]:

        news_topic_alias = aliased(News_topic)
        news_alias = aliased(News)

        return self.session.query(Sentiment).\
            join(news_alias, Sentiment.news_id == news_alias.news_id).\
            join(news_topic_alias, news_alias.news_id == news_topic_alias.news_id).\
            join(Topic, news_topic_alias.topic_id == Topic.topic_id).\
            filter(and_(
                Topic.topic_date >= start_date,
                Topic.topic_date <= end_date,
                Topic.company_id == company_id,
                not_(Topic.topic_code.like('%-1'))
            )).all()
            
        # 날짜와 기업으로 토픽에 맞는 뉴스 불러오기    
    def get_news_cnt_by_date_and_company(self, start_date, end_date, company_id) -> List[News_topic]:
        return self.session.query(News_topic).join(Topic, News_topic.topic_id == Topic.topic_id).filter(and_(
                Topic.topic_date >= start_date,
                Topic.topic_date <= end_date,
                Topic.company_id == company_id
            )).all()
       
    # 기업의 최신 종가(close) 가격 불러오기
    def get_company_stock_close_price_recent_90day(self, company_id):

        column_name = f'col_{company_id}'# getattr를 사용하여 모델에서 해당 컬럼 찾기
        target_column = getattr(Company_Close_price, column_name, None) # getattr를 사용하여 모델에서 해당 컬럼 찾기
        
        return self.session.query(Company_Close_price.date, target_column)\
            .order_by(Company_Close_price.date.desc()).limit(90).all() 

    
    # 기업으로 뉴스들 요약 불러오기    
    def get_news_summary_by_company(self, company_id) -> List[any]:
    
        news_alias = aliased(News)
        news_company_alias = aliased(News_company)

        return self.session.query(Summary).\
            join(news_alias, Summary.news_id == news_alias.news_id).\
            join(news_company_alias, news_alias.news_id == news_company_alias.news_id).\
            join(Company, news_company_alias.company_id == Company.company_id).\
            filter(
                Company.company_id == company_id
            ).\
            order_by(news_alias.date.desc()).\
            limit(30).all() 
            
    # 기업으로 뉴스들 불러오기    
    def get_news_by_company(self, company_id) -> List[any]:
    
        news_company_alias = aliased(News_company)


        return self.session.query(News).\
            join(news_company_alias, News.news_id == news_company_alias.news_id).\
            join(Company, news_company_alias.company_id == Company.company_id).\
            filter(
                Company.company_id == company_id
            ).\
            order_by(News.date.desc()).\
            limit(30).all() 
            
            
    # 기업으로 뉴스들 sentiment 불러오기    
    def get_news_sentiment_by_company(self, company_id) -> List[any]:
    
        news_topic_alias = aliased(News_topic)
        news_alias = aliased(News)

        return self.session.query(Sentiment).\
            join(news_alias, Sentiment.news_id == news_alias.news_id).\
            join(news_topic_alias, news_alias.news_id == news_topic_alias.news_id).\
            join(Topic, news_topic_alias.topic_id == Topic.topic_id).\
            filter(
                Topic.company_id == company_id
            ).\
            order_by(news_alias.date.desc()).\
            limit(30).all()         
    
    # 뉴스번호로, 해당 뉴스가 할당된 토픽 안에 총 뉴스의 개수가 몇 개인지 불러오는 코드    
    def get_news_cnt_in_topic_by_news(self, news_id) -> int:
    
        news_topic_alias = aliased(News_topic)
        news_alias = aliased(News)
        topic_alias = aliased(Topic)

        return self.session.query(func.count(news_topic_alias.news_topic_id)).\
            join(news_alias, news_topic_alias.news_id == news_alias.news_id).\
            join(topic_alias, news_topic_alias.topic_id == topic_alias.topic_id).\
            filter(
                news_alias.news_id == news_id
            ).scalar()            
            
            
# 기업과 날짜로 가장 핫한 토픽의 topic_summary 불러오기

    def get_topics_summary_by_date_and_company_last(self, company_id) -> List[Topic_summary]:
        
        return self.session.query(Topic_summary).join(Topic, Topic_summary.topic_id == Topic.topic_id).filter(and_(
                Topic.company_id == company_id,
                not_(Topic.topic_code.like('%-1'))
            )).order_by(Topic.topic_date.desc()).\
            limit(30).all()
    
    def get_news_cnt_by_date_and_company_last(self, company_id) -> List[News_topic]:
        return self.session.query(News_topic).join(Topic, News_topic.topic_id == Topic.topic_id).filter(and_(
                Topic.company_id == company_id,
                not_(Topic.topic_code.like('%-1'))
            )).order_by(Topic.topic_date.desc()).\
            limit(30).all()    
 
 
    # 기업으로 가장 최근 company_info 불러오기        
    def get_company_info_by_company(self, company_id) -> Company_price_info:
        return self.session.query(Company_price_info).filter(and_(
                Company_price_info.company_id == company_id
            )).order_by(Company_price_info.date.desc()).first()      
            
            
    # 날짜와 기업으로 토픽의 뉴스들을 불러오기    
    def get_news_by_date_and_company(self, start_date, end_date, company_id):

        return self.session.query(News_topic).\
            join(Topic, News_topic.topic_id == Topic.topic_id).\
            filter(and_(
                Topic.topic_date >= start_date,
                Topic.topic_date <= end_date,
                Topic.company_id == company_id,
                not_(Topic.topic_code.like('%-1'))
            )).all()
   
    
    #뉴스 아이디로 뉴스 내용 가져오기    
    def get_news_by_news_id(self, news_id):

        result = self.session.query(News.title).\
            filter(News.news_id.in_(news_id)).all()
        
        return [row[0] for row in result]
    
    #뉴스 아이디로 뉴스 내용 가져오기 + 날짜 내림차순으로 정렬    
    def get_news_by_news_id_ordered_desc_by_date(self, news_id):

        result = self.session.query(News.title).\
            filter(News.news_id.in_(news_id)).\
            order_by(News.date.desc()).all()
        
        return [row[0] for row in result]
    
    #뉴스 토픽 기준 첫 번째 뉴스의 이미지 1개 url 골라오기
    def get_topic_image_url_by_date_and_company(self, topic_id):
        topic_image = self.session.query(Topic_image).\
            filter(Topic_image.topic_id == topic_id).first()
        
        if topic_image:
            return TopicImageURLResponse(image_url=topic_image.image_url)
        else:
            return TopicImageURLResponse()


    # 가장 최근 economy_price_info 불러오기  (경제지표)     
    def get_economy_price_info_recent(self) -> Economy_price_info:
        return self.session.query(Economy_price_info)\
                        .order_by(Economy_price_info.date.desc()).first() 
    
    # 가장 최근의 경제지표 정보에서 두 번째로 최신인 데이터를 불러오기 (경제지표 등락률 계산용)
    def get_second_economy_price_info(self) -> Economy_price_info:
        return self.session.query(Economy_price_info)\
                        .order_by(Economy_price_info.date.desc())\
                        .offset(1).first()


        
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
    


    
