from sqlalchemy import Column, Integer, VARCHAR, DateTime, ForeignKey, Date 
from datetime import datetime 
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class News(Base):
    __tablename__ = "NEWS"
    
    # columns
    news_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(VARCHAR(100), nullable=False)
    date = Column(DateTime, nullable=False)
    contents = Column(VARCHAR(3000), nullable=False)
    url = Column(VARCHAR(100), nullable=False)
    # del_yn = Column(VARCHAR(1), nullable=False, default='N')
    
    # one to many
    news_company_list = relationship("News_company", back_populates="news")
    news_topic_list = relationship("News_topic", back_populates="news")
    
    # one to one
    summary = relationship("Summary", back_populates="news", uselist=False)
    sentiment = relationship("Sentiment", back_populates="news", uselist=False)


class Summary(Base):
    __tablename__ = "SUMMARY"
    
    # columns
    summary_id = Column(Integer, primary_key=True, autoincrement=True)
    summary_text = Column(VARCHAR(500), nullable=False)    
    # del_yn = Column(VARCHAR(1), nullable=False, default='N')
    
    # foreign key
    news_id = Column(Integer, ForeignKey("NEWS.news_id"))
    
    # one to one
    news = relationship("News", back_populates="summary")
    
    
class Sentiment(Base):
    __tablename__ = "SENTIMENT"
    
    # columns
    sentiment_id = Column(Integer, primary_key=True, autoincrement=True)
    sentiment_value = Column(Integer, nullable=False)      
    # del_yn = Column(VARCHAR(1), nullable=False, default='N')
    
    # foreign key
    news_id = Column(Integer, ForeignKey("NEWS.news_id"))
    
    # one to one
    news = relationship("News", back_populates="sentiment")
    
    
class Company(Base):
    __tablename__ = "COMPANY"
    
    # columns
    company_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(20), nullable=False)
    company_code = Column(VARCHAR(20), nullable=False)
    # del_yn = Column(VARCHAR(1), nullable=False, default='N')
    
    # one to many
    company_news_list = relationship("News_company", back_populates="company")
    
    
class News_company(Base):
    __tablename__ = "NEWS_COMPANY"
    
    # columns
    news_company_id = Column(Integer, primary_key=True, autoincrement=True)
    # del_yn = Column(VARCHAR(1), nullable=False, default='N')
    
    # foreign key
    news_id = Column(Integer, ForeignKey("NEWS.news_id"))
    company_id = Column(Integer, ForeignKey("COMPANY.company_id"))
    
    
    # many to one
    news = relationship("News", back_populates="news_company_list")
    company = relationship("Company", back_populates="company_news_list")
    
    
class Topic(Base):
    __tablename__ = "TOPIC_AT"
    
    # columns
    topic_id = Column(Integer, primary_key=True, autoincrement=True)
    news_id_list = Column(VARCHAR(2000), nullable=False)
    company_id = Column(VARCHAR(20), nullable=False) 
    topic_date = Column(Date, nullable=False)
    topic_code = Column(VARCHAR(20), nullable=False)
    # sentiment = Column(Integer, nullable=False)
    # del_yn = Column(VARCHAR(1), nullable=False, default='N')
    
    # one to many
    topic_news_list = relationship("News_topic", back_populates="topic") 
    
    # one to one
    topic_summary = relationship("Topic_summary", back_populates="topic", uselist=False)
    topic_image = relationship("Topic_image", back_populates="topic", uselist=False)
    
class News_topic(Base):
    __tablename__ = "NEWS_TOPIC_AT"
    
    # columns
    news_topic_id = Column(Integer, primary_key=True, autoincrement=True)
    # del_yn = Column(VARCHAR(1), nullable=False, default='N')
    
    # foreign key
    news_id = Column(Integer, ForeignKey("NEWS.news_id"))
    topic_id = Column(Integer, ForeignKey("TOPIC_AT.topic_id"))
    
    # many to one
    news = relationship("News", back_populates="news_topic_list")
    topic = relationship("Topic", back_populates="topic_news_list")
    

class Topic_summary(Base):
    __tablename__ = "TOPIC_SUMMARY"
    
    # columns
    topic_summary_id = Column(Integer, primary_key=True, autoincrement=True)
    topic_title_summary = Column(VARCHAR(200), nullable=False)
    topic_summary = Column(VARCHAR(1000), nullable=False)
    # del_yn = Column(VARCHAR(1), nullable=False, default='N')
    
    # foreign key
    topic_id = Column(Integer, ForeignKey("TOPIC_AT.topic_id"))
    
    # one to one
    topic = relationship("Topic", back_populates="topic_summary")
    
    
class Topic_image(Base):
    __tablename__ = "TOPIC_IMAGE"
    
    # columns
    topic_image_id = Column(Integer, primary_key=True, autoincrement=True)
    image_url = Column(VARCHAR(100), nullable=False)
    
    # foreign key
    topic_id = Column(Integer, ForeignKey("TOPIC_AT.topic_id"))
    
    # one to one
    topic = relationship("Topic", back_populates="topic_image")
    
    
    
