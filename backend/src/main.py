from fastapi import FastAPI 
from api import company_api, news_api, topic_api, api_jh
import database.orm
from database.connection import engine
from starlette.middleware.cors import CORSMiddleware


import sys
import os

# 현재 스크립트의 경로를 가져옵니다.
current_dir = os.path.dirname(os.path.abspath(__file__))
# 'src' 디렉토리의 상위 디렉토리 경로를 구합니다.
base_dir = os.path.dirname(current_dir)
# sys.path에 추가합니다.
sys.path.append(base_dir)
# 이제 Python은 base_dir 경로 아래의 모든 디렉토리를 모듈 검색 경로에 포함시킬 것입니다.



app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.include_router(company_api.router)
# app.include_router(news_api.router)
# app.include_router(topic_api.router)
app.include_router(api_jh.router)

# table 자동 생성, 데이터 다 날아갈 수 있어서 처음에 생성할 때만 써야 함.
# database.orm.Base.metadata.create_all(bind=engine)

@app.get("/")
async def check_request_and_response():
    return {"message": "hello"}