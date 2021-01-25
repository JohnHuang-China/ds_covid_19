import glb
import datetime
import requests
import lxml
from bs4 import BeautifulSoup
import re
from bs4 import NavigableString

#失败检测
def s_fail(tianya_get):
    bs=BeautifulSoup(tianya_get.text,'lxml')
    return bs.find(string=re.compile("没有找到含有")) is not None

# 集成了失败检测
def tianya_s(key,page):
    url="https://search.tianya.cn/bbs"
    params={
        'q':key,
        'pn':str(page),
        's':'10',
        'f':'3',
    }
    g=0
    while True:
        g=requests.get(
            url=url,
            params=params,
            headers=glb.ff_header,
        )
        if not s_fail(g):
            break
    return g
    
# 每个帖子保留标题、日期、回复量
def list_all(tianya_get,checked_href):
    bs=BeautifulSoup(tianya_get.text,'lxml')
    li_rec=[]
    for li in bs.find_all("li",class_=False,id=False):
        # 筛选
        if li.find(string=re.compile("区块链")) is not None:
            continue
        href=li.find("a")["href"]
        if href in checked_href:
            continue
        else:
            checked_href.add(href)
        # 数据
        ti=li.find("h3")
        title="".join([i for i in ti.stripped_strings])
        dat=li.find(string=re.compile("^[0-9]+-[0-9]+-[0-9]+ [0-9]+:[0-9]+:[0-9]+$")).string.split(" ")[0]
        repl=li.find(string=re.compile("^[0-9]+$")).string
        if dat[0]!='2':
            with open("wrong_page.html","w",encoding="utf-8") as f:
                f.write(tianya_get.text)
            print("wrong date:%s url:%s"%(dat,tianya_get.url))
        li_rec.append({
            'title':title,
            'href':href,
            'date':dat,
            'reply':repl
        })
    return li_rec

import json
all_rec=[]
checked_href=set()
for keyw in ['新冠','疫情']:
    for k in range(0,76):
        all_rec.extend(list_all(tianya_s(keyw,k),checked_href))
        # print("Page %d finished"%k)
    print("%s finished."%keyw)
with open("tianya_result.json","w",encoding='utf-8') as f:  # 保存
    json.dump(all_rec,f,ensure_ascii=False)

# 日期处理
def date_diff(cur_date):
    return (datetime.datetime.strptime(cur_date,"%Y-%m-%d").date()-glb.base_date).days

# 详情页处理
# 返回一个pair，news与comments
def tianya_comment(comment_url):
    g=requests.get(comment_url)
    bs=BeautifulSoup(g.text,'lxml')
    find_title=bs.find(class_="s_title")
    if find_title is None:
        return None
    if bs.find(class_="bbs-content clearfix") is None:
        print("first floor error! url: %s"%comment_url)
    title="".join([i for i in find_title.stripped_strings])
    first_floor="".join([i for i in bs.find(class_=re.compile("^bbs-content.*clearfix$")).stripped_strings])
    if title is None or first_floor is None:
        print("%s: %s + %s"%(comment_url,title,first_floor))
    comments=["".join(i.find(class_="bbs-content").stripped_strings) for i in bs.find_all(class_="atl-item",replyid=True)]
    return [title+" "+first_floor,comments]

all_rec=[]
with open("tianya_result.json","r",encoding='utf-8') as f:  # 加载
    all_rec=json.load(f)

# 数据汇总
total_data=[]
for i in range(0,183):
    total_data.append({'date':i,'news':[],'comments':[]})
for i in all_rec:
    if int(i['date'][0:4])==2020 and int(i['date'][5:7])<=6:
        diff=date_diff(i['date'])
        cm=tianya_comment(i['href'])
        if cm is not None:
            target_date=total_data[diff]
            target_date['news'].append(["",cm[0]])
            target_date['comments'].extend(cm[1])
        


with open("tianya_data.json","w",encoding='utf-8') as f:
    json.dump(total_data,f,ensure_ascii=False)