from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column

engine=create_engine('sqlite:///movies.db')

class Base(DeclarativeBase):
    pass

class Movie(Base):
    __tablename__ = "movies"
    id:Mapped[int] = mapped_column( primary_key=True)
    name:Mapped[str]
    year:Mapped[int]
    release:Mapped[str]
    genre:Mapped[str]
    duration:Mapped[str]
    score:Mapped[int]
    language:Mapped[str]

















