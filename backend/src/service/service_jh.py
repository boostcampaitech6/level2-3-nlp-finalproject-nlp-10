from repository.repository_jh import Repository_jh
from schema.request import Topic_titles_request
from schema.dto import Topic_title_dto, Topic_titles_dto
from fastapi import Depends 
from database.orm import Topic

class Service_jh:
    
    def get_topic_titles(request: Topic_titles_request, repo: Repository_jh = Depends()) -> Topic_titles_dto:
        print("request: =============", request)
        start_date = request.start_date
        end_date = request.end_date
        company_id = request.company_id
        topic_title_dto_list = []
        
        topics : Topic = repo.get_topics_by_date_and_company(start_date, end_date, company_id)
       
        for topic in topics:
            topic_title_summary = repo.get_topic_summary_by_topic(topic.id)
            news_in_topic = repo.get_news_cnt_id_by_topic(topic.id)
            topic_sentiment = repo.get_news_sentiment_by_topic(topic.id)
            
            topic_title_dto = Topic_title_dto(topic_title_summary, news_in_topic, topic_sentiment)
            
            topic_title_dto_list.append(topic_title_dto)
        
        topic_titles_dto = Topic_titles_dto(topic_title_dto_list)
              
        return topic_titles_dto