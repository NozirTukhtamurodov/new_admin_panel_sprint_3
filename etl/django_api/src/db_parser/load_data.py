from configs import lite_connection, pg_connection, DictCursor, psycopg2, sqlite3, db_path, dsl
from db.schemas import Genre, Person, FilmWork, GenreFilmWork, PersonFilmWork
from db.parser import SQLiteExtractor, PostgresSaver


def is_postgres_empty(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM content.genre LIMIT 1;")
    data = cursor.fetchone()
    return data is None


def load_from_sqlite(connection: lite_connection, pg_conn: pg_connection):
    """Основной метод загрузки данных из SQLite в Postgres"""
    tables = [Genre, Person, FilmWork, GenreFilmWork, PersonFilmWork]
    pg_saver = PostgresSaver(connection=pg_conn)
    sqlite_extracter = SQLiteExtractor(connection=connection)
    for table in tables:
        sqlite_extracter.cur_execute(table=table)
        while True:
            extracted_data = sqlite_extracter.extract_data(100)
            if extracted_data:
                pg_saver.save_data(data=extracted_data, table=table)
            else:
                break
    sqlite_extracter.cursor.close()


if __name__ == '__main__':
    with sqlite3.connect(db_path) as sqlite_conn, psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:
        if is_postgres_empty(conn=pg_conn):
            load_from_sqlite(sqlite_conn, pg_conn)
    sqlite_conn.close()
    pg_conn.close()
