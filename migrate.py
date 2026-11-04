import sqlite3
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from db import engine, Base, Movie

Base.metadata.create_all(engine)  # 在 MySQL 里建 movies 表

conn = sqlite3.connect("movies.db")
conn.row_factory = sqlite3.Row
rows = conn.execute(
    "SELECT id, name, year, release, genre, duration, score, language FROM movies"
).fetchall()
conn.close()

with Session(engine) as session:
    count = session.scalar(select(func.count()).select_from(Movie))
    if count > 0:
        print(f"MySQL 里已有 {count} 条数据，已取消，避免重复导入")
    else:
        session.add_all([Movie(**dict(r)) for r in rows])
        session.commit()
        print(f"导入完成，共 {len(rows)} 条")