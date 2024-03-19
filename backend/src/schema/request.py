from pydantic import BaseModel
from datetime import datetime 

class Topic_titles_request(BaseModel):
    start_date: str 
    end_date: str 
    company_id: int
    
class Topic_id_request(BaseModel):
    topic_id: int
    