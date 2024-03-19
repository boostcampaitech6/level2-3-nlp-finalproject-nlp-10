from pydantic import BaseModel
from typing import List

class Topic_titles_response(BaseModel):
    titles: List[str]
    
    def __init__(self, titles):
        self.titles = titles
        
   
    
        
    