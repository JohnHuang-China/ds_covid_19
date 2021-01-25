import glb
import datetime
import requests
import lxml
from bs4 import BeautifulSoup
import re
from bs4 import NavigableString
import json

base_second=1577721600

# gpc生成
def get_gpc(days):
    cur_second=base_second+days*86400
    return "stf=%d,%d|stftype=2"%(cur_second,cur_second+86400-1)

# 搜索页
def baidu_s(keyword,days):
    return requests.get(
        url="https://www.baidu.com/s?ie=utf-8&medium=2&rtt=1&bsst=1&rsv_dl=news_t_sk&cl=2&wd=%s&tn=news&rsv_bp=1&tfflag=0&gpc=%s"%(keyword,get_gpc(days)),
        headers=glb.ff_header
    )

# 详情页
def baidu_baijiahao(url):
    g=requests.get(
        url=url,
        headers=glb.ff_header
    )
    bs=BeautifulSoup(g.text,'lxml')
    if bs.find(class_="author-name") is None:
        print("no author-name-----url:%s"%url)
        return None

    name=bs.find(class_="author-name").find('a').string
    title=bs.find(class_="article-title").find('h2').string
    content="".join([i.string if i.string is not None else "" for i in bs.find_all(class_="bjh-p")])

    if re.search(r'"tid":"[0-9]+"',g.text) is None:
        print("no tid found! url:%s"%g.url)
    tid=re.search(r'"tid":"[0-9]+"',g.text).group().split("\"")[-2]
    g=requests.get(
        url="https://ext.baidu.com/api/comment/v2/comment/list?thread_id=%s&reply_id=&start=0&num=20&appid=22862035&order=12&inner_order=9&use_list=1&use_uk=1"%tid,
        headers=glb.ff_header
    )
    json1=json.loads(g.text)
    repl_list=json1['ret']['list']

    comments=[]
    if repl_list:
        comments=[i['content'] for i in repl_list]    
    
    return [name,"%s %s"%(title,content),comments]

print(baidu_baijiahao("https://baijiahao.baidu.com/s?id=1689748168304280609&wfr=spider&for=pc"))

import sys
keywords=["新冠","疫情","病毒"]
total_data=[]
# 整合
for d in range(0,183):
    total_data.append({'date':d,'news':[],'comments':[]})
    checked_url=set()
    for keyword in keywords:
        g=baidu_s(keyword,d)
        bs=BeautifulSoup(g.text,'lxml')
        news_title=bs.find_all(class_="news-title-font_1xS-F")
        if news_title is not None:
            for i in news_title:
                checked_url.add(i['href'])
    for url in checked_url:
        pg=baidu_baijiahao(url)
        if pg is not None:
            item=total_data[d]
            item['news'].append([pg[0],pg[1]])
            item['comments'].extend(pg[2])
    sys.stdout.write("\r%d days loaded."%d)
    sys.stdout.flush

with open("baijiahao_data.json","w",encoding='utf-8') as f:
    json.dump(total_data,f,ensure_ascii=False)
    

 