from pydantic import BaseModel
from typing import List, Dict
from typing import Optional

class TopicImageURLResponse(BaseModel):
    image_url: Optional[str] = None


class Topic_titles_response(BaseModel):
    titles: List[str]
    
    def __init__(self, titles):
        self.titles = titles
      
        
   
    
        
    