from fastapi import FastAPI, HTTPException,Depends
from pydantic import BaseModel
from db import engine,Movie
from sqlalchemy.orm import Session
from sqlalchemy import select


app=FastAPI(swagger_ui_parameters={
        "swagger_js_url": "https://cdn.bootcdn.net/ajax/libs/swagger-ui/5.17.14/swagger-ui-bundle.min.js",
        "swagger_css_url": "https://cdn.bootcdn.net/ajax/libs/swagger-ui/5.17.14/swagger-ui.min.css",
    })


class MovieIn(BaseModel):
    name: str
    year: int
    release: str = "无"
    genre: str = "无"
    duration: str= "无"
    score: int
    language: str = "无"


def get_db():
    with Session(engine) as session:
        yield session


#添加电影
@app.post("/movies")
def add_movies(movie: MovieIn,session: Session = Depends(get_db)):
    m=Movie(name=movie.name,year=movie.year,release=movie.release,genre=movie.genre,duration=movie.duration,score=movie.score,language=movie.language)
    session.add(m)
    session.commit()
    return {"id": m.id,"message":"添加成功"}
#删除电影
@app.delete("/movies/{id}")
def delete_movie(id: int,session: Session = Depends(get_db)):
    sel=select(Movie).where(Movie.id==id)
    delete=session.scalar(sel)
    if delete:
        session.delete(delete)
        session.commit()
        return {"message": "删除成功"}
    raise HTTPException(status_code=404, detail="Movie not found")
#查询电影
@app.get("/movies")
def get_movies(sj: str="",pf: int=80,session: Session = Depends(get_db)):
    sel=select(Movie).where(Movie.name.like(f"%{sj}%"),Movie.score>=pf)
    shuju=session.scalars(sel).all()
    rows = []
    for i in shuju:
        rows.append({"id":i.id,"电影名":i.name,"年份":i.year,"上映时间(地区)":i.release,"类型":i.genre,"时长":i.duration,"评分":i.score,"语言":i.language})
    if rows:
        return rows
    raise HTTPException(status_code=404, detail="Movie not found")




if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)






