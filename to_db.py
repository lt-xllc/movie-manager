import csv
import sqlite3

conn=sqlite3.connect("movies.db")
cur=conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS movies(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    year INTEGER,
    release TEXT,
    genre TEXT,
    duration TEXT,
    score INTEGER,
    language TEXT
)
""")

cur.execute("DELETE FROM movies")

with open("csv2.csv","r",encoding="utf-8") as f:
    reader = csv.reader(f)
    #print(list(reader))
    next(reader)
    rows = [(r[0],int(r[1]),r[2],r[3],r[4],int(r[5]),r[6]) for r in reader]


cur.executemany("INSERT INTO movies (name,year,release,genre,duration,score,language)VALUES(?,?,?,?,?,?,?)",rows)
conn.commit()

cur.execute("SELECT name,score FROM movies WHERE score>=? ORDER BY score DESC",(88,))
print(cur.fetchall())
conn.close()














