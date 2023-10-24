from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.config import Base

from uuid import UUID, uuid4
from datetime import datetime, date
from sqlalchemy import ForeignKey
from typing import List


class BaseModel(Base):
    __abstract__ = True
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)


class Genre(BaseModel):
    __tablename__ = "genre"
    name: Mapped[str]
    description: Mapped[str]
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    filmworks: Mapped[List['GenreFilmwork']] = relationship(back_populates='genre')


class Person(BaseModel):
    __tablename__ = "person"
    full_name: Mapped[str]
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    filmworks: Mapped[List['PersonFilmWork']] = relationship(back_populates='person')


class FilmWork(BaseModel):
    __tablename__ = 'film_work'
    title: Mapped[str]
    description: Mapped[str]
    creation_date: Mapped[date]
    file_path: Mapped[str]
    rating: Mapped[float]
    type: Mapped[str]
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    filmwork_persons: Mapped[List['PersonFilmWork']] = relationship(back_populates='filmwork')
    filmwork_genres: Mapped[List['GenreFilmwork']] = relationship(back_populates='filmwork')


class PersonFilmWork(BaseModel):
    __tablename__ = 'person_film_work'
    role: Mapped[str]
    person_id: Mapped[UUID] = mapped_column(
        ForeignKey("person.id")
    )
    film_work_id: Mapped[UUID] = mapped_column(
        ForeignKey("film_work.id")
    )
    person: Mapped['Person'] = relationship(back_populates='filmworks')
    filmwork: Mapped['FilmWork'] = relationship(back_populates='filmwork_persons')


class GenreFilmwork(BaseModel):
    __tablename__ = "genre_film_work"
    film_work_id: Mapped[UUID] = mapped_column(
        ForeignKey("film_work.id")
    )
    genre_id: Mapped[UUID] = mapped_column(
        ForeignKey("genre.id")
    )
    filmwork: Mapped['FilmWork'] = relationship(back_populates='filmwork_genres')
    genre: Mapped['Genre'] = relationship(back_populates='filmworks')
