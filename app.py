import requests
import streamlit as st

API="http://127.0.0.1:8000"

st.title("电影列表")

#@st.cache_data
def get_movies(keyword,min_score):
    return requests.get(f"{API}/movies",params={"sj":keyword,"pf":min_score}).json()

#movies=get_movies()
#print(movies)
st.subheader("添加电影")
with st.form("add_form",clear_on_submit=True):
    name=st.text_input("电影名")
    year=st.number_input("年份",1900,2026,2000)
    release=st.text_input("上映时间(地区)")
    genre=st.text_input("类型")
    duration=st.text_input("时长")
    score=st.number_input("评分",0,100,80)
    language=st.text_input("语言")
    submitted=st.form_submit_button("添加")
if submitted:
    if not name:
        st.error("电影名不能为空")
    else:
        r=requests.post(
            f"{API}/movies",
            json={
                "name":name,
                "year":year,
                "release":release,
                "genre":genre,
                "duration":duration,
                "score":score,
                "language":language}
        )
        if r.status_code==200:
            st.success("添加成功")
        else:
            st.error(f"添加失败:{r.status_code}")


@st.dialog("确认删除")
def confirm_delete(movie_id):
    st.write(f"确定要删除{movie_id}吗?")
    col1,col2,_=st.columns([1,1,2])
    if col1.button("确定"):
        r = requests.delete(f"{API}/movies/{movie_id}")
        if r.status_code == 200:
            st.rerun()
        elif r.status_code == 404:
            st.error("没有该电影")
        else:
            st.error(f"失败:{r.status_code}")
    if col2.button("取消"):
        st.rerun()

sc=st.number_input("要删除的电影:",min_value=1,step=1)
if st.button("删除"):
    confirm_delete(sc)



keyword=st.text_input("搜索电影名:")
min_score=st.slider("最低评分:",0,100,80)

#调用接口,获取到数据
movies=get_movies(keyword,min_score)

if "detail" in movies:
    st.warning("没找到符合条件的电影")
else:
    st.write(f"共{len(movies)}部电影")
    st.dataframe(movies)
















