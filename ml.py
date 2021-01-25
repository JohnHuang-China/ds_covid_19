import jieba
import json
import time
from sklearn import preprocessing
from sklearn.feature_extraction.text import CountVectorizer

data_files=["bilibili_data.json","weibo_data.json","baijiahao_data.json","tianya_data.json"]
data_set=[]
for i in range(0,183):
    data_set.append({'date':i,'news':[],'comments':[]})
for i in range(0,4):
    with open(data_files[i],"r",encoding='utf-8') as f:
        jsons_cur=json.load(f)
    for j in range(0,183):
        for news in jsons_cur[j]['news']:
            if news[0]!="健康中国":
                data_set[j]['news'].append(news)
        data_set[j]['comments'].extend(jsons_cur[j]['comments'])
with open("all4_data.json","w",encoding="utf-8") as f:
    json.dump(data_set,f,ensure_ascii=False)

# 先做好分词，调用vectorize时下标对应即可
import sys
split_data_set=[]
tot_split={'news':[],'comments':[]}
for i in range(0,183):
    split_data_set.append({'date':i,'news':[],'comments':[]})
    dd=data_set[i]
    for news in dd['news']:
        sp=" ".join(jieba.cut(news[1]))
        split_data_set[i]['news'].append(sp)
        tot_split['news'].append(sp)
    for cmm in dd['comments']:
        sp=" ".join(jieba.cut(cmm))
        split_data_set[i]['comments'].append(sp)
        tot_split['comments'].append(sp)
    sys.stdout.write("\r%d days split."%i)
    sys.stdout.flush
with open("all4_data_split.json","w",encoding="utf-8") as f:
    json.dump(split_data_set,f,ensure_ascii=False)
with open("tot_split.json","w",encoding="utf-8") as f:
    json.dump(tot_split,f,ensure_ascii=False)



