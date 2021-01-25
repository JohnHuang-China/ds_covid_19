import time
import json
import random
from sklearn import preprocessing
from sklearn.feature_extraction.text import CountVectorizer
import xgboost as xgb
import numpy as np
import collections

with open("all4_data_split.json","r",encoding="utf-8") as f:
    split_data_set=json.load(f)
with open("tot_split.json","r",encoding="utf-8") as f:
    tot_split=json.load(f)

stw=[l.strip() for l in open("hit_stpw.txt","r",encoding="utf-8").readlines()]
# 针对新闻和评论的两个vectorizer
news_cvt=CountVectorizer(
    min_df=10,
    max_df=0.2,
    ngram_range=(1,2),
    stop_words=stw,
)
comment_cvt=CountVectorizer(
    min_df=20,
    max_df=0.5,
    ngram_range=(1,1),
    stop_words=stw,
)

'''
news_vt.fit(tot_split['news'])
comment_vt.fit(tot_split['comments'])
print("news_vt has %d features"%len(news_vt.get_feature_names()))
print("comment_vt has %d features"%len(comment_vt.get_feature_names()))
# print(news_vt.transform(tot_split['news'][0:1]))
p0=time.perf_counter()
tot_split['news_vector']=news_vt.transform(tot_split['news'])
p1=time.perf_counter()
print("transform ended. cost: %f s"%(p1-p0))

p0=time.perf_counter()
clf = xgb.XGBClassifier(max_depth=7, n_estimators=200, colsample_bytree=0.8, 
                        subsample=0.8, nthread=10, learning_rate=0.1)
list1=[]
for i in range(0,len(tot_split['news'])):
    list1.append(random.randrange(10))
clf.fit(tot_split['news_vector'].tocsc(),list1)
p1=time.perf_counter()
print("training ended. cost: %f s"%(p1-p0))
'''
news_cvt.fit(tot_split['news'])
comment_cvt.fit(tot_split['comments'])

with open("news_rec.json","r",encoding="utf-8") as f:
    news_record=json.load(f)
with open("comment_rec.json","r",encoding="utf-8") as f:
    comment_record=json.load(f)

news_x=[]
news_y=[]
for item in news_record.items():
    news_x.append(split_data_set[int(item[0].split(",")[0])]['news'][int(item[0].split(",")[1])])
    news_y.append(item[1])
newsx_cvt=news_cvt.transform(news_x)
# print(news_x[0])

comment_x=[]
comment_y=[]
for item in comment_record.items():
    comment_x.append(split_data_set[int(item[0].split(",")[0])]['comments'][int(item[0].split(",")[1])])
    comment_y.append(item[1])
commentx_cvt=comment_cvt.transform(comment_x)

news_clf = xgb.XGBClassifier(max_depth=7, n_estimators=200, colsample_bytree=0.8, 
                        subsample=0.8, nthread=10, learning_rate=0.1)
comment_clf = xgb.XGBClassifier(max_depth=7, n_estimators=200, colsample_bytree=0.8, 
                        subsample=0.8, nthread=10, learning_rate=0.1)
news_clf.fit(newsx_cvt,news_y)
comment_clf.fit(commentx_cvt,comment_y)

for item in split_data_set:
    item['news_type']=news_clf.predict(news_cvt.transform(item['news']).tocsc())
    item['comment_type']=comment_clf.predict(comment_cvt.transform(item['comments']).tocsc())

print(split_data_set[0]['news_type'])
print(split_data_set[0]['comment_type'])

for item in split_data_set:
    # 处理新闻
    nt=item['news_type']
    cnt=[0,1,2,3,4,5,6]
    len1=len(nt)
    cl=collections.Counter(nt)
    #计数
    for i in range(0,7):
        cnt[i]=cl[i]/len1
    item['news_conc']=cnt
    # 处理评论
    nt=item['comment_type']
    cnt2=[0,1,2,3,4,5,6]
    len1=len(nt)
    cl=collections.Counter(nt)
    #计数
    for i in range(0,7):
        cnt2[i]=cl[i]/len1
    item['comment_conc']=cnt2

print(split_data_set[5]['news_conc'])
print(split_data_set[5]['comment_conc'])


#plt.plot(x_lab,y0)
#plt.plot(x_lab,y1,color='g')
#plt.plot(x_lab,y2,color='r')

import glb
import datetime
border_days=[
    datetime.date(2020,1,22),
    datetime.date(2020,2,9),
    datetime.date(2020,3,10)
    ]

import matplotlib.pyplot as plt
x_lab=np.arange(183)
y=[]
fig = plt.figure()
ax = fig.add_axes([0.1, 0.1, 0.6, 0.75])
for j in range(0,7):
    y.append([split_data_set[i]['news_conc'][j] for i in x_lab])
    ax.plot(x_lab,y[j],label="Type %d"%j)
ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
for dt in border_days:
    ax.vlines((dt-glb.base_date).days,0,1.0,colors='c',linestyles='dashed')
plt.title("News distribution by time")
plt.show()

y=[]
fig = plt.figure()
ax = fig.add_axes([0.1, 0.1, 0.6, 0.75])
for j in range(0,7):
    y.append([split_data_set[i]['comment_conc'][j] for i in x_lab])
    ax.plot(x_lab,y[j],label="Type %d"%j)
ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
for dt in border_days:
    ax.vlines((dt-glb.base_date).days,0,1.0,colors='c',linestyles='dashed')
plt.title("Comment distribution by time")
plt.show()