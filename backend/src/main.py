from fastapi import FastAPI 
from api import company_api, news_api, topic_api, api_jh
import database.orm
from database.connection import engine
from starlette.middleware.cors import CORSMiddleware

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