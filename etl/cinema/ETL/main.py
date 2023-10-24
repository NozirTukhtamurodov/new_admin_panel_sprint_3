from decorators import create_session, coroutine, backoff
from time import sleep
import logging as logger
from repository import FilmWorkRepository
from elastic.indexes import MoviesIndex
from typing import Generator
from datetime import datetime
from states.state import State
from states.redis_storage import RedisStorage


STATE_KEY = 'last_movies_updated'


@coroutine
@create_session
@backoff(start_sleep_time=0.1, factor=2, border_sleep_time=100)
def fetch_changed_movies(next_node: Generator, session) -> Generator[None, datetime, None]:
    ''' 
    checks if there any updated movies
    '''
    while last_updated := (yield):
        with session:
            records_per_page = 100
            offset = 0
            while True:
                query = FilmWorkRepository.last_updateds(limit=records_per_page, offset=offset, updated_at=last_updated)
                result = session.execute(query)
                objects = result.mappings().all()
                ## break the loop if there is no data
                if not result or not objects:
                    break
                offset += records_per_page
                next_node.send(objects)


@coroutine
@backoff(start_sleep_time=0.1, factor=2, border_sleep_time=100)
def save_movies(next_node: Generator) -> Generator[None, list, None]:
    '''
    saves the updated movies to ES
    
    '''
    while movies := (yield):
        MoviesIndex.put_data(data=movies)
        logger.info(f'Received for saving {len(movies)} movies')
        next_node.send(str(movies[-1]['updated_at']))


@coroutine
@backoff(start_sleep_time=0.1, factor=2, border_sleep_time=100)
def save_state(state: State) -> Generator[None, list, None]:
    '''
    saves the updated_at field into state
    '''
    while update_at := (yield):
        logger.info(f'Recived for saving last updated at: {update_at} to state')
        state.set_state(STATE_KEY, update_at)


@backoff(start_sleep_time=0.1, factor=2, border_sleep_time=100)
def main():
    state = State(RedisStorage())
    state_saver_coro: Generator = save_state(state)
    movies_saver_coro: Generator = save_movies(next_node=state_saver_coro)
    fetcher_coro: Generator = fetch_changed_movies(next_node=movies_saver_coro)

    while True:
        logger.info('Starting ETL process for updates ...')
        fetcher_coro.send(state.get_state(STATE_KEY) or str(datetime.min))
        sleep(15)

if __name__ == "__main__":
    main()
