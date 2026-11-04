import os
from dotenv import load_dotenv
from sqlalchemy import create_engine,String
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column

load_dotenv()
engine=create_engine(os.getenv('DATABASE_URL'))

class Base(DeclarativeBase):
    pass

class Movie(Base):
    __tablename__ = "movies"
    id:Mapped[int] = mapped_column( primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    year: Mapped[int]
    release: Mapped[str] = mapped_column(String(50))
    genre: Mapped[str] = mapped_column(String(100))
    duration: Mapped[str] = mapped_column(String(20))
    score: Mapped[int]
    language: Mapped[str] = mapped_column(String(50))

















