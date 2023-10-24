from states.base_storage import BaseStorage
from redis import Redis
import os
from dotenv import load_dotenv


load_dotenv()
host = os.environ.get('REDIS_HOST')
port = os.environ.get('REDIS_PORT')
db = os.environ.get('REDIS_DB')


class RedisStorage(BaseStorage):
    def __init__(self):
        self.redis_client = Redis(host=host, port=port, db=db, encoding='utf-8')

    def save_state(self, state: dict) -> None:
        self.redis_client.hmset('state', state)

    def retrieve_state(self) -> dict:
        state = self.redis_client.hgetall('state')
        if state:
            # Convert bytes to strings in the state dictionary
            state = {key.decode('utf-8'): value.decode('utf-8') for key, value in state.items()}
            return state
        else:
            return {}
