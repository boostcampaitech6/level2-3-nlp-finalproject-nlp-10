from typing import List
from schema import response 

class Topic_title_dto:
    def __init__(self, topic_title_summary: str, cnt: int, sentiment: int):
        self.topic_title_summary = topic_title_summary
        self.cnt = cnt 
        self.sentiment = sentiment

class Topic_titles_dto:
    titles:List[str]
    def __init__(self, title: Topic_title_dto):
        self.titles: List[Topic_title_dto] = List[title]
    
    def topic_titles_dto_to_response(self):
        return response.Topic_titles_response(self.titles)
    