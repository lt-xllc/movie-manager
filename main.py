import csv
from fastapi import FastAPI, HTTPException
import sqlite3
from pydantic import BaseModel



app=FastAPI(swagger_ui_parameters={
        "swagger_js_url": "https://cdn.bootcdn.net/ajax/libs/swagger-ui/5.17.14/swagger-ui-bundle.min.js",
        "swagger_css_url": "https://cdn.bootcdn.net/ajax/libs/swagger-ui/5.17.14/swagger-ui.min.css",
    })


def load_movies():
    with open("csv2.csv","r",encoding="utf-8") as f:
        rows=list(csv.DictReader(f))
    for i,row in enumerate(rows,start=1):
        row["id"]=i
    return rows




movies=load_movies()
#print(movies)
#@app.get("/")
#async def root():
#    return {"message": "Welcome to Movie Release API"}



class Movie(BaseModel):
    name: str
    year: int
    release: str = "无"
    genre: str = "无"
    duration: str= "无"
    score: int
    language: str = "无"

@app.post("/movies")
def list_movies(movie: Movie):
    conn=sqlite3.connect("movies.db")
    cur=conn.cursor()
    cur.execute("INSERT INTO movies (name,year,release,genre,duration,score,language)VALUES(?,?,?,?,?,?,?)",
                (movie.name,movie.year,movie.release,movie.genre,movie.duration,movie.score,movie.language))
    conn.commit()
    new_id=cur.lastrowid #添加了第几位id
    conn.close()
    return {"id": new_id,"message":"添加成功"}


@app.delete("/movies/{id}")
def delete_movie(id: int):
    conn=sqlite3.connect("movies.db")
    cur=conn.cursor()
    cur.execute("DELETE FROM movies WHERE id=?",(id,))
    conn.commit()
    delete=cur.rowcount #相较于之前的数据有多少改动
    conn.close()
    if delete == 0:
        raise HTTPException(status_code=404, detail="Movie not found")
    return {"message": "删除成功"}


@app.get("/movies")
def list_movies(sj: str="",pf: int=80):
    conn=sqlite3.connect("movies.db")

    conn.row_factory=sqlite3.Row
    cur=conn.cursor()
    cur.execute("""
                select id,name AS 电影名,year AS 年份,release AS "上映时间(地区)",genre AS 类型,duration AS 时长,score AS 评分,language AS 语言
                from movies 
                WHERE name LIKE ? AND score>=?                                                     
                                 """,(f"%{sj}%",pf))
    #rows=[dict(r)for r in cur.fetchall()]
    rows=[]
    for i in cur.fetchall():
        rows.append(dict(i))
        #print(i)
    conn.close()
    if rows:
        return rows
    raise HTTPException(status_code=404, detail="Movie not found")


    # a = []
    # for i in movies:
    #     if sj in i["电影名"] and pf<=int(i["评分"]):
    #         a.append(i)
    # if a:
    #     return a
    # raise HTTPException(status_code=404, detail="Movie not found")





# @app.get("/movies/{id}")
# def get_movie(id: str):
#     a=[]
#     for i in movies:
#         if id in i["电影名"]:
#             a.append(i)
#     if a:
#         return a
#
#     raise HTTPException(status_code=404, detail="Movie not found")





if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)






