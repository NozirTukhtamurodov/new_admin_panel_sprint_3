import psycopg2
import sqlite3
import pytest
from sqlite_to_postgres.configs import DictCursor, db_path, dsl
from sqlite_to_postgres.db.schemas import Genre, Person, FilmWork, PersonFilmWork, GenreFilmWork
from datetime import datetime, timezone
import sys  # Import the sys module
sys.path.append(('..'))


def format_timestamp(timestamp):
    # Format the datetime object as a string in the PostgreSQL format
    pg_formatted_timestamp = timestamp.strftime('%Y-%m-%dT%H:%M:%S.%f%z')

    return pg_formatted_timestamp


@pytest.fixture(scope="module")
def sqlite_conn():
    # Connect to SQLite and return the connection
    conn = sqlite3.connect(db_path)
    yield conn
    conn.close()

@pytest.fixture(scope="module")
def pg_conn():
    # Connect to PostgreSQL and return the connection
    conn = psycopg2.connect(**dsl, cursor_factory=DictCursor)
    yield conn
    conn.close()

def test_genre_data_transfer(sqlite_conn, pg_conn):
    # Verify structure and data integrity for the Genre table
    tables = [Genre, Person, FilmWork, GenreFilmWork, PersonFilmWork]
    pg_cursor = pg_conn.cursor()
    sqlite_cursor = sqlite_conn.cursor()
    for table in tables:
        table_name = table.__table_name__
        # Verify table structure (column names and data types)
        pg_cursor.execute(f"SELECT * FROM {table_name} WHERE 1=0")
        pg_columns = [desc[0] for desc in pg_cursor.description]
        pg_columns.sort()

        sqlite_cursor.execute(f"PRAGMA table_info({table_name})")
        sqlite_columns = [row[1] for row in sqlite_cursor.fetchall()]
        sqlite_columns.sort()
        assert pg_columns == sqlite_columns, f"Column structure mismatch for {table_name}"
        # Verify data integrity (compare row counts and individual rows)
        pg_cursor.execute(f"SELECT {', '.join(pg_columns)} FROM {table_name}")
        pg_data = pg_cursor.fetchall()

        sqlite_cursor.execute(f"SELECT {', '.join(sqlite_columns)} FROM {table_name}")
        sqlite_data = sqlite_cursor.fetchall()
        
        assert len(pg_data) == len(sqlite_data), f"Row count mismatch for {table_name}"
        for pg_row, sqlite_row in zip(pg_data, sqlite_data):
            # Format timestamps consistently before comparing
            for i in range(len(pg_row)):
                pg_row_data = pg_row[i]
                sqlite_row_data = sqlite_row[i]
                if isinstance(pg_row_data, datetime):
                    pg_row_data = pg_row_data.astimezone(timezone.utc)
                    pg_row_data = pg_row_data.strftime('%Y-%m-%d %H:%M:%S.%f').rstrip('0')
                    sqlite_row_data = sqlite_row_data.split('+')[0]
                assert pg_row_data == sqlite_row_data, "Data mismatch for genre"
