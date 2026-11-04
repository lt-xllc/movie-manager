from sqlalchemy import select
from sqlalchemy.orm import Session
from db import engine, Movie

with Session(engine) as session:
    stmt = select(Movie).where(Movie.name.like("%教父%"), Movie.score >= 80)
    for m in session.scalars(stmt):
        print(m.name, m.score)