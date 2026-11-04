# 电影数据管理系统

一个前后端分离的小项目：爬取电影数据，存入数据库，通过 API 提供增删查功能，并用网页界面展示。

## 技术栈
- 爬虫：Python（requests + lxml/XPath），数据来自 TMDB 高分电影榜
- 数据库：MySQL 8（SQLAlchemy ORM），连接配置从 .env 读取
- 后端：FastAPI
- 前端：Streamlit

## 功能
- 按电影名搜索、按最低评分筛选
- 在页面上添加电影（表单）
- 在页面上删除电影（弹窗确认）

## 项目结构
```
c.py          爬虫（抓取 TMDB 榜单，输出 csv2.csv）
csv2.csv      爬取到的电影数据
to_db.py      把 CSV 导入 SQLite，生成 movies.db（已生成，无需再运行）
movies.db     SQLite 初始数据
db.py         SQLAlchemy 模型与数据库连接
migrate.py    把 SQLite 数据导入 MySQL（只需运行一次）
main.py       FastAPI 后端
app.py        Streamlit 前端
.env.example  数据库连接配置模板
```


## 运行方法
1. 安装依赖：`pip install -r requirements.txt`
2. 安装 MySQL 8，创建数据库：`CREATE DATABASE movies_db CHARACTER SET utf8mb4;`
3. 复制 `.env.example` 为 `.env`，把里面的"你的密码"改成自己的 root 密码
4. 导入初始数据（只需一次，不要重复运行）：`python migrate.py`
5. 启动后端：`python main.py`（地址 http://127.0.0.1:8000 ，接口文档见 /docs）
6. 另开一个终端启动前端：`streamlit run app.py`

## 接口
| 方法 | 路径 | 说明 |
|---|---|---|
| GET | /movies?sj=关键词&pf=最低评分 | 搜索和筛选 |
| POST | /movies | 添加电影 |
| DELETE | /movies/{id} | 删除电影 |

## 截图
![主界面](images/main.png)
![删除确认](images/delete.png)
