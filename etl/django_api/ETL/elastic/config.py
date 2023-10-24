import os
from dotenv import load_dotenv


load_dotenv()

HOST = os.environ.get('NGINX_HOST')
PORT = os.environ.get('ELASTIC_PORT')
URL = f"http://{HOST}:{PORT}"
