from configs import lite_connection, pg_connection, dataclass, fields
from psycopg2.extras import execute_batch


class SQLiteExtractor:
    def __init__(self, connection: lite_connection) -> None:
        self.connection = connection
    
    @property
    def cursor(self):
        cur = getattr(self, 'cur', None)
        if not cur:
            cur = self.connection.cursor()
            setattr(self, 'cur', cur)
        return cur

    @property
    def query(self):
        return "SELECT * FROM {table_name}"

    def cur_execute(self, table):
        self.cursor.execute(self.query.format(table_name=table.__table_name__))

    def extract_data(self, number):
        return self.cursor.fetchmany(number)


class PostgresSaver:
    def __init__(self, connection: pg_connection) -> None:
        self.conn = connection
        self.batch = 5000

    def save_data(self, data, table: dataclass):
        column_names = [field.name for field in fields(table)]
        with self.conn.cursor() as cur:
            column_placeholders = ', '.join(['%s'] * len(column_names))
            query = (f"INSERT INTO content.{table.__table_name__} ({', '.join(column_names)}) VALUES ({column_placeholders})"
                    f" ON CONFLICT (id) DO NOTHING")
            execute_batch(cur, query, data, page_size=self.batch)
