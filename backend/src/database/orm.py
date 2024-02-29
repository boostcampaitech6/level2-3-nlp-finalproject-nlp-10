from sqlalchemy import Column, Integer, VARCHAR, DateTime, ForeignKey 
from datetime import datetime 
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class News(Base):
    __tablename__ = "news"
    
    # columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(VARCHAR(100), nullable=False)
    datetime = Column(DateTime, nullable=False, default=datetime.now)
    contents = Column(VARCHAR(3000), nullable=False)
    url = Column(VARCHAR(100), nullable=False)
    del_yn = Column(VARCHAR(1), nullable=False, default='N')
    
    # one to many
    news_company_list = relationship("News_company", back_populates="news")
    news_topic_list = relationship("News_topic", back_populates="news")
    
    # one to one
    summary = relationship("Summary", back_populates="news", uselist=False)
    sentiment = relationship("Sentiment", back_populates="news", uselist=False)


class Summary(Base):
    __tablename__ = "summary"
    
    # columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    summary_text = Column(VARCHAR(500), nullable=False)    
    del_yn = Column(VARCHAR(1), nullable=False, default='N')
    
    # foreign key
    news_id = Column(Integer, ForeignKey("news.id"))
    
    # one to one
    news = relationship("News", back_populates="summary")
    
    
class Sentiment(Base):
    __tablename__ = "sentiment"
    
    # columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    sentiment_value = Column(Integer, nullable=False)      
    del_yn = Column(VARCHAR(1), nullable=False, default='N')
    
    # foreign key
    news_id = Column(Integer, ForeignKey("news.id"))
    
    # one to one
    news = relationship("News", back_populates="sentiment")
    
    
class Company(Base):
    __tablename__ = "company"
    
    # columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(20), nullable=False)
    company_code = Column(VARCHAR(20), nullable=False)
    del_yn = Column(VARCHAR(1), nullable=False, default='N')
    
    # one to many
    company_news_list = relationship("News_company", back_populates="company")
    
    
class News_company(Base):
    __tablename__ = "news_company"
    
    # columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    del_yn = Column(VARCHAR(1), nullable=False, default='N')
    
    # foreign key
    news_id = Column(Integer, ForeignKey("news.id"))
    company_id = Column(Integer, ForeignKey("company.id"))
    
    # many to one
    news = relationship("News", back_populates="news_company_list")
    company = relationship("Company", back_populates="company_news_list")
    
    
class Topic(Base):
    __tablename__ = "topic"
    
    # columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    nouns = Column(VARCHAR(200), nullable=False)
    company_id = Column(VARCHAR(20), nullable=False) 
    topic_code = Column(VARCHAR(20), nullable=False)
    del_yn = Column(VARCHAR(1), nullable=False, default='N')
    
    # one to many
    topic_news_list = relationship("News_topic", back_populates="topic") 
    
    # one to one
    topic_summary = relationship("Topic_summary", back_populates="Topic", uselist=False)
    topic_image = relationship("Topic_image", back_populates="Topic", uselist=False)
    
class News_topic(Base):
    __tablename__ = "news_topic"
    
    # columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    del_yn = Column(VARCHAR(1), nullable=False, default='N')
    
    # foreign key
    news_id = Column(Integer, ForeignKey("news.id"))
    topic_id = Column(Integer, ForeignKey("topic.id"))
    
    # many to one
    news = relationship("News", back_populates="news_topic_list")
    topic = relationship("Topic", back_populates="topic_news_list")
    

class Topic_summary(Base):
    __tablename__ = "topic_summary"
    
    # columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    topic_title_sumary = Column(VARCHAR(200), nullable=False)
    topic_sumary = Column(VARCHAR(1000), nullable=False)
    del_yn = Column(VARCHAR(1), nullable=False, default='N')
    
    # foreign key
    topic_id = Column(Integer, ForeignKey("topic.id"))
    
    # one to one
    topic = relationship("Topic", back_populates="Topic_summary")
    
    
class Topic_image(Base):
    __tablename__ = "topic_image"
    
    # columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    image_url = Column(VARCHAR(100), nullable=False)
    
    # foreign key
    topic_id = Column(Integer, ForeignKey("topic.id"))
    
    # one to one
    topic = relationship("Topic", back_populates="Topic_image")
    
    
    
