import uuid
from dataclasses import dataclass, field
from datetime import datetime, date

@dataclass
class Genre:
    __table_name__ = 'genre'
    id: uuid.UUID = field(default_factory=uuid.uuid4())
    name: str = field(default_factory='')
    description: str = field(default_factory='')
    created_at: datetime = field(default_factory=datetime.now())
    updated_at: datetime = field(default_factory=datetime.now())


@dataclass
class Person:
    __table_name__ = 'person'
    id: uuid.UUID = field(default_factory=uuid.uuid4())
    full_name: str = field(default_factory='')
    created_at: datetime = field(default_factory=datetime.now())
    updated_at: datetime = field(default_factory=datetime.now())


@dataclass
class FilmWork:
    __table_name__ = 'film_work'
    id: uuid.UUID = field(default_factory=uuid.uuid4())
    title: str = field(default_factory='')
    description: str = field(default_factory='')
    creation_date: date = field(default_factory=datetime.now())
    file_path: str = field(default_factory='')
    rating: float = field(default_factory=1)
    type: str = field(default_factory='')
    created_at: datetime = field(default_factory=datetime.now())
    updated_at: datetime = field(default_factory=datetime.now())

@dataclass
class GenreFilmWork:
    __table_name__ = 'genre_film_work'
    id: uuid.UUID = field(default_factory=uuid.uuid4())
    film_work_id: uuid.UUID = field(default_factory=uuid.uuid4())
    genre_id: uuid.UUID = field(default_factory=uuid.uuid4())
    created_at: datetime = field(default_factory=datetime.now())


@dataclass
class PersonFilmWork:
    __table_name__ = 'person_film_work'
    id: uuid.UUID = field(default_factory=uuid.uuid4())
    film_work_id: uuid.UUID = field(default_factory=uuid.uuid4())
    person_id: uuid.UUID = field(default_factory=uuid.uuid4())
    role: str = field(default_factory="")
    created_at: datetime = field(default_factory=datetime.now())
