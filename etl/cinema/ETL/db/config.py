from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv


load_dotenv()
db_name = os.environ.get('DB_NAME')
db_user = os.environ.get('DB_USER')
db_password = os.environ.get('DB_PASSWORD')
host = os.environ.get('DB_HOST')
db_port = os.environ.get('DB_PORT')
URL = f"postgresql://{db_user}:{db_password}@{host}:{db_port}/{db_name}"

engine = create_engine(
    URL,
    pool_pre_ping=True, pool_size=20, pool_timeout=30)

Base = declarative_base()
