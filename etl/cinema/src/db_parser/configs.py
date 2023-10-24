from dataclasses import dataclass, fields
from psycopg2.extensions import connection as pg_connection
from sqlite3 import Connection as lite_connection
import sqlite3
import psycopg2
from psycopg2.extras import DictCursor
import os
from dotenv import load_dotenv


load_dotenv()


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Build paths inside the project like this: BASE_DIR / 'subdir'.


db_name = os.environ.get('DB_NAME')
db_user = os.environ.get('DB_USER')
db_password = os.environ.get('DB_PASSWORD')
host = os.environ.get('DB_HOST', '127.0.0.1')
db_port = os.environ.get('DB_PORT', 5432)
db_path = f'{BASE_DIR}/db.sqlite'

dsl = {'dbname': db_name, 'user': db_user, 'password': db_password, 'host': host, 'port': db_port}
