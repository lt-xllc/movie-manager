import requests
from lxml import html
import csv

url_1="https://www.themoviedb.org/movie/top-rated"
url_2="https://www.themoviedb.org/"
#print(requests.get(url_1).text)
url_3="https://www.themoviedb.org/discover/movie/items"
#获取网页源码
a=requests.get(url_1).text
#b=requests.post(url_3,"air_date.gte=&air_date.lte=&certification=&certification_country=CN&debug=&first_air_date.gte=&first_air_date.lte=&include_adult=false&include_softcore=false&latest_ceremony.gte=&latest_ceremony.lte=&page={page1}&primary_release_date.gte=&primary_release_date.lte=&region=&release_date.gte=&release_date.lte=2027-04-28&show_me=everything&sort_by=vote_average.desc&vote_average.gte=0&vote_average.lte=10&vote_count.gte=300&vote_count.lte=&watch_region=CN&with_genres=&with_keywords=&with_networks=&with_origin_country=&with_original_language=&with_watch_monetization_types=&with_watch_providers=&with_release_type=&with_runtime.gte=0&with_runtime.lte=400&view=&discover_preset=top-rated").text

#定义表头
biaotou=["电影名","年份","上映时间(地区)","类型","时长","评分","语言"]

#创建html对象
m=html.fromstring(a)


#n1=m.xpath('//div[@id]/div/div/a/@href')
#print(url_2+n1[0])

wangzhi=[]
#获取到所有网址并加进wangzhi列表中
for j in range(1,6):
    b = requests.post(url_3,
                      f"air_date.gte=&air_date.lte=&certification=&certification_country=CN&debug=&first_air_date.gte=&first_air_date.lte=&include_adult=false&include_softcore=false&latest_ceremony.gte=&latest_ceremony.lte=&page={j}&primary_release_date.gte=&primary_release_date.lte=&region=&release_date.gte=&release_date.lte=2027-04-28&show_me=everything&sort_by=vote_average.desc&vote_average.gte=0&vote_average.lte=10&vote_count.gte=300&vote_count.lte=&watch_region=CN&with_genres=&with_keywords=&with_networks=&with_origin_country=&with_original_language=&with_watch_monetization_types=&with_watch_providers=&with_release_type=&with_runtime.gte=0&with_runtime.lte=400&view=&discover_preset=top-rated").text
    if j==1:
        m=html.fromstring(a)
    else:
        m=html.fromstring(b)
    for i in m.xpath('//div[@id]/div/div'):
        if i.xpath('./a/@href')!=[]:
            wangzhi.append(url_2+i.xpath('./a/@href')[0])




#获取网址里的数据并返回
def f1(wangzhi1):
    sj=[]
    dijige=1
    for i in wangzhi1:
        a1=requests.get(i).text
        m1=html.fromstring(a1)
        n1=m1.xpath('//*[@id="original_header"]/div[2]/section/div[1]/h2/a/text()')
        n2=m1.xpath('//*[@id="original_header"]/div[2]/section/div[1]/h2/span/text()')
        n2=[n2[0][1:-1]]
        n3=m1.xpath('//*[@id="original_header"]/div[2]/section/div[1]/div/span[@class="release"]/text()')

        if n3!=[]:
            n3=n3[0].strip()
            n3=[n3]
        else:
            n3=["无"]
        n4=m1.xpath('//*[@id="original_header"]/div[2]/section/div[1]/div/span[@class="genres"]/a/text()')
        if n4!=[]:
            n4=[",".join(n4)]
        else:
            n4=["无"]
        n5=m1.xpath('//*[@id="original_header"]/div[2]/section/div[1]/div/span[@class="runtime"]/text()')
        if n5!=[]:
            n5=n5[0].strip()
            n5=[n5]
        else:
            n5=["无"]
        n6=m1.xpath('//*[@id="consensus_pill"]/div/div[1]/div/div/@data-percent')
        n7=m1.xpath('//*[@id="media_v4"]/div/div/div[2]/div/section/div[1]/div/section[1]/p/strong[contains(.,"默认语言")]/following-sibling::text()')

        sj.append(n1+n2+n3+n4+n5+n6+n7)
        print("获取成功!",dijige)
        dijige=dijige+1
    return sj
    #for i in sj:
        #print(i)



with open("csv2.csv",'w',newline='',encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=biaotou)
    w.writeheader()  # 写入表头
    shuju=f1(wangzhi)
    for i in shuju:
        #按行写入数据
        w.writerow(dict(zip(biaotou,i)))








