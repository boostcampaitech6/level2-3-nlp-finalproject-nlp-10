from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker 
from sqlalchemy import exc
from dotenv import load_dotenv
from sshtunnel import SSHTunnelForwarder
import pymysql
import os 

load_dotenv()  

# 서버 연결 정보
# server_user = os.getenv('SERVER_USER')
server_host = os.getenv('SERVER_HOST')
# server_port = int(os.getenv('SERVER_PORT'))
# server_private_key_path = os.getenv('SERVER_PRIVATE_KEY_PATH')

# DB 연결 정보
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_port = int(os.getenv('DB_PORT'))
db_name = os.getenv('DB_NAME')

# local
# DB_URL = f'mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'

# server
DB_URL = f"mysql+pymysql://{db_user}:{db_password}@{server_host}/{db_name}"

engine = create_engine(DB_URL, echo=True, pool_size=5, max_overflow=10)
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    session = session_local()
    try:
        yield session  
    finally:
        session.close()
