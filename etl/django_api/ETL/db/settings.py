import os
from dotenv import load_dotenv


load_dotenv()


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Build paths inside the project like this: BASE_DIR / 'subdir'.


db_name = os.environ.get('DB_NAME')
db_user = os.environ.get('DB_USER')
db_password = os.environ.get('DB_PASSWORD')
host = os.environ.get('DB_HOST')
db_port = os.environ.get('DB_PORT')

DB_URL = f"postgresql://{db_user}:{db_password}@{host}:{db_port}/{db_name}"
