import glb
import datetime
import requests
import lxml
from bs4 import BeautifulSoup

# custom:2020-01-30:2020-01-31
#某天的时间参数
def weibo_time_tag(days_from_base_date):
    new_date=glb.base_date+datetime.timedelta(days=days_from_base_date)
    new_date2=new_date+datetime.timedelta(days=1)
    return "custom:"+new_date.strftime('%Y-%m-%d-0')+":"+new_date2.strftime('%Y-%m-%d-0')

# 搜索GET
def weibo_s(q,day_offset):
    url="https://s.weibo.com/weibo"
    params={
        'q':q,
        'category':'4',
        'suball':'1',
        'timescope':weibo_time_tag(day_offset),
        'Refer':'g'
        }
    
    return requests.get(
        url=url,
        params=params,
        headers=glb.ff_header,
        cookies=glb.ff_wb_cookie,
        timeout=5
        )

#连接某一html块所有string
def conc(bs_tag):
    strs=["" if i.string is None else i.string for i in bs_tag.contents]
    return ''.join(strs)


import json

#某一页全部mid
def weibo_mid(weibo_get):
    bs=BeautifulSoup(weibo_get.text,'lxml')
    temp=[i['mid'] for i in bs.find_all(attrs={'action-type':'feed_list_item'})]
    return temp

# 评论GET
def weibo_c(mid):
    url="https://weibo.com/aj/v6/comment/big"
    params={
        'ajwvr':'6',
        'id':mid,
        'from':'singleWeiBo',
        '__rnd':'1611472127714'
    }
    return requests.get(
        url=url,
        params=params,
        headers=glb.ff_header,
        cookies=glb.ff_wb_cookie,
        timeout=5
        )

#某一页全部首次加载的一级评论
def weibo_page_all_comment(weibo_get):
    bs=BeautifulSoup(json.loads(weibo_get.text)['data']['html'],'lxml')
    comments=[]
    for i in bs.find_all(attrs={'node-type':'root_comment'}):
        tmp=conc_navi(i.find(class_="WB_text"))
        if tmp!="":
            comments.append(tmp)
    return comments


from bs4 import NavigableString
#提取某一tag下面所有NavigableString
def conc_navi(bs_tag):
    temp=''.join([str(i) for i in bs_tag.contents if isinstance(i,NavigableString)]).strip()[1:]# 第一个字符必定是"："
    repl=temp.find("//")  #通过"//"去掉回复的内容
    if(repl>=0):
        temp= temp[:repl]
    return temp.strip()

#某一搜索页全部首次加载的一级评论
def weibo_s_all_comment(weibo_get,checked_mid):
    all_comment=[]
    for mid in weibo_mid(weibo_get):
        if mid in checked_mid:
            continue
        else:
            checked_mid.add(mid)
        all_comment.extend(weibo_page_all_comment(weibo_c(mid)))
    return all_comment

# 特例化href
def href_id(wb_tag):
    return wb_tag.find(class_="from").find(href=True)["href"].split("?")[0].split("/")[-1]

import re
# 某一页全部content的发布者与内容
def weibo_page_all_content(weibo_get,checked_href):
    bs=BeautifulSoup(weibo_get.text,'lxml')
    if bs.find(string=re.compile("抱歉，未找到")) is not None:
        return []
    contents=bs.find_all("div",class_="content")
    texts=[]
    for k in contents:
        hid=href_id(k)
        if hid in checked_href:  #  判断hid
            continue
        else:
            checked_href.add(hid)
        text=k.find("p",attrs={"node-type":"feed_list_content_full"})
        if text is None:
            text=k.find("p",attrs={"node-type":"feed_list_content"})
        texts.append(text)
    pairs=[[i['nick-name'],conc(i).strip()] for i in texts]
    for p in pairs:
        if p[0]=="新浪电影":
            print("XLDY found. url:"+weibo_get.url)
    return pairs

# 收集某天以前的所有搜索
# 关键字新冠、疫情、病毒
def weibo_crawl(keys,ddl):
    max_day=(ddl-glb.base_date).days
    data=[]
    for i in range(0,max_day+1):
        #保存新闻
        checked_href=set()  # href查重
        checked_mid=set()
        news=[]
        comments=[]
        for k in keys:
            try:
                ge=weibo_s(k,i)
                news.extend(weibo_page_all_content(ge,checked_href))
                comments.extend(weibo_s_all_comment(ge,checked_mid))
            except:
                print("---connection error---")
        data.append({
            'date':i,
            'news':news,
            'comments':comments
        })
        print("Day %d completed."%i)
    with open("weibo_data.json","w",encoding="utf-8") as f:
        json.dump(data,f,ensure_ascii=False)

requests.adapters.DEFAULT_RETRIES=5
requests.session().keep_alive=False
weibo_crawl(['新冠','疫情','病毒'],datetime.date(2020,6,30))
        
            




print(weibo_s("疫情",5).url)
#for k in weibo_page_all_content(weibo_s("疫情",5)):
#    print("%s\n%s"%(k[0],k[1]))
#requests.session().keep_alive=False
#for k in weibo_s_all_comment(weibo_s("病毒",6)):
#   print(k)

t='''<div class="WB_text">
            <a target="_blank" href="//weibo.com/lixiaofen026081" usercard="id=1785489115">哒哒爱点木</a>：为什么越来越多呀？        </div>'''

# print(BeautifulSoup(weibo_s("疫情",5).text,'lxml').find("a"))
# print(weibo_time_tag(1))