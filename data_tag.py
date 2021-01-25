import json
import random

'''
心情：疑问、希望（关心）、赞扬、批评（嘲笑）、害怕、
新闻标签定义：
0-其它
1-国内+
2-国外/湾湾+
3-外交+
4-国内-
5-国外/湾湾-
6-外交-

评论标签定义
0-其它
1-希望、同情、祝福、哀悼、加油、关心
2-疑问、悬疑、担心、惊讶、惊叹
3-难受、失望、抱怨、不赞同、批评
4-嘲讽、狗头、辩证、观点
5-赞美、赞同、感谢、感叹、致敬
6-开心、满足、有信心、有底气、乐观
'''

with open("all4_data.json","r",encoding="utf-8") as f:
    data_set=json.load(f)

news_manual_rec={}
comment_manual_rec={}

print("judging news now...")
news_cnt=0
while True:
    news_cnt+=1
    pos=(0,0)
    # 找到一个未取过的位置
    while True:
        cnt=0
        while cnt<=0:
            rand_date=random.randrange(183)
            cnt=len(data_set[rand_date]['news'])
        pos=(rand_date,random.randrange(cnt))
        if "%d,%d"%pos not in news_manual_rec:
            break
    cont=data_set[pos[0]]['news'][pos[1]][1]
    print("%d. %s"%(news_cnt,cont[:(80 if len(cont)>80 else len(cont))]))
    inp=''
    while True:
        print("enter the type: ",end="")
        inp=input()
        if inp!="":
            break
    i=int(inp)
    if i>10:
        break
    news_manual_rec["%d,%d"%pos]=i

print("judging comments now...")
comment_cnt=0
while True:
    comment_cnt+=1
    pos=(0,0)
    # 找到一个未取过的位置
    while True:
        cnt=0
        while cnt<=0:
            rand_date=random.randrange(183)
            cnt=len(data_set[rand_date]['comments'])
        pos=(rand_date,random.randrange(cnt))
        if "%d,%d"%pos not in comment_manual_rec:
            break
    cont=data_set[pos[0]]['comments'][pos[1]]
    if cont=="":
        continue
    print("%d. %s"%(comment_cnt,cont[:(80 if len(cont)>80 else len(cont))]))
    inp=''
    while True:
        print("enter the type: ",end="")
        inp=input()
        if inp!="":
            break
    i=int(inp)
    if i>10:
        break
    comment_manual_rec["%d,%d"%pos]=i


# 用于恢复
'''
import re
for i in range(0,len(f)-1):
    bg=5 if i==1 else 7
    tar_str=re.compile(f[i][bg:(bg+20)])
    for d in range(0,183):
        for subs in range(0,len(data_set[d]['news'])):
            if tar_str.match(data_set[d]['news'][subs][1]):
                news_manual_rec["%d,%d"%(d,subs)]=int(f[i+1][0])
'''

with open("news_rec.json","w",encoding="utf-8") as f:
    json.dump(news_manual_rec,f)
with open("comment_rec.json","w",encoding="utf-8") as f:
    json.dump(comment_manual_rec,f)