import glb
import datetime
import requests
import lxml
from bs4 import BeautifulSoup
import re
from bs4 import NavigableString

import math
import json
# 只有固定几个网址，硬编
bids=["456664753","222103174","20165629"]
keywords=["新冠","疫情","病毒"]

# 借用
def date_diff(cur_date):
    return (datetime.datetime.strptime(cur_date,"%Y-%m-%d").date()-glb.base_date).days

# 某搜索的所有结果
def video_bvids(bid,keyword):
    g=requests.get(
        url="https://api.bilibili.com/x/space/arc/search?mid=%s&ps=30&tid=0&pn=1&keyword=%s&order=pubdate&jsonp=jsonp"%(bid,keyword),
        headers=glb.ff_header
    )
    json1=json.loads(g.text)
    # 收集每一页
    bvids=[]
    print(json1['data']['page']['count'])
    for i in range(1,math.ceil(json1['data']['page']['count']/30)):
        g=requests.get(
            url="https://api.bilibili.com/x/space/arc/search?mid=%s&ps=30&tid=0&pn=%d&keyword=%s&order=pubdate&jsonp=jsonp"%(bid,i,keyword),
            headers=glb.ff_header
        )
        json1=json.loads(g.text)
        for tt in json1['data']['list']['vlist']:
            bvids.append(tt['bvid'])
            if tt['bvid']=="BV1U7411M7Qs":
                print("target bvid found! url:%s"%g.url)
    return bvids

# 处理结果页
def video_page_comment(bvid):
    g=requests.get(
        url="https://www.bilibili.com/video/%s"%bvid,
        headers=glb.ff_header
    )
    bs=BeautifulSoup(g.text,"lxml")

    if bs.find(string="追剧") is not None:
        return None

    username=""
    findname=bs.find(class_="username")
    if findname is None:
        username=" ".join([i.string for i in bs.find_all(class_="name-text is-vip")])
    else:
        username=findname.string

    if bs.find(class_="video-data") is None:
        print("video-data empty! url:%s bvid:%s"%(g.url,bvid))
    
    date=date_diff(
        bs.find(class_="video-data").find("span",title=False).string.split(" ")[0]
    )
    if date>182 or date<0:
        return None
    title=bs.find(class_="tit").string
    info=bs.find(class_="info open").string

    # 获取av号
    avid=bs.find(itemprop="url")['content'].split("v")[-1][:-1]
    # 请求第一页回复json
    g=requests.get(
        url="https://api.bilibili.com/x/v2/reply?jsonp=jsonp&pn=1&type=1&oid=%s&sort=2&_=1611517198902"%avid,
        headers=glb.ff_header
    )
    json1=json.loads(g.text)

    comments=[]
    if 'data' in json1 :
        if json1['data']['replies'] is not None:
            comments=[i['content']['message'] for i in json1['data']['replies']]
    # print(comments[0])

    return[date,username,"%s %s"%(title,info),comments]

import sys
# 整合
tot_bvid=set()
total_data=[]
cnt=0
for i in range(0,183):
    total_data.append({'date':i,'news':[],'comments':[]})

for bid in bids:
    for keyword in keywords:
        for one_bvid in video_bvids(bid,keyword):
            tot_bvid.add(one_bvid)

tot_len=len(tot_bvid)
for bvid in tot_bvid:
    cm=video_page_comment(bvid)
    if cm is not None:
        item=total_data[cm[0]]
        item['news'].append([cm[1],cm[2]])
        item['comments'].extend(cm[3])
    cnt+=1
    sys.stdout.write("\r%d / %d bvids loaded."%(cnt,tot_len))
    sys.stdout.flush

with open("bilibili_data.json","w",encoding='utf-8') as f:
    json.dump(total_data,f,ensure_ascii=False)
