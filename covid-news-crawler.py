from bs4 import BeautifulSoup

html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""

soup=BeautifulSoup(html_doc,'html.parser')

import requests
import lxml

ff_header={
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0',
    }
ff_wb_cookie={
	"_s_tentry": "login.sina.com.cn",
	"ALF": "1642928459",
	"Apache": "8175450816258.878.1611392463737",
	"SCF": "Aht7HwEKaZ1k0RUq1iQj4c9kDaJPz3rafhVsgpvPK50yUVgKF8-ygTnREwpcnenmZG-LwNNmWlzxvkgY6K6DcWw.",
	"SINAGLOBAL": "1554178379884.7576.1586852533034",
	"SSOLoginState": "1611392460",
	"SUB": "_2A25ND5WcDeRhGeRP71MX9CbIyzyIHXVufIBUrDV8PUNbmtANLWrTkW9NTgX4tynMn-bjFgbn3pEbHqopRJpUTP8L",
	"SUBP": "0033WrSXqPxfM725Ws9jqgMF55529P9D9W5X-m-swu9eX0w8nPEixiWy5JpX5KMhUgL.FozpSh2cShnXeh52dJLoIpRLxK-LBo5L12qLxKnL1K.LB-zLxKBLBonLBoqEe0et",
	"ULV": "1611392463745:34:3:3:8175450816258.878.1611392463737:1611312692145",
	"UOR": ",,www.baidu.com",
	"WBStorage": "8daec78e6a891122|undefined",
	"webim_unReadCount": "{\"time\":1611416315003,\"dm_pub_total\":0,\"chat_group_client\":999,\"chat_group_notice\":0,\"allcountNum\":1042,\"msgbox\":0}",
	"wvr": "6"
}

test_url="https://s.weibo.com/weibo"

test_params={
    'q':'123',
    'category':'4',
    'suball':'1',
    'timescope':'custom:2020-01-30:2020-01-31',
    'Refer':'g'
    }

r=requests.get(url=test_url,params=test_params,headers=ff_header)

print(r.url)

import re

soup2=BeautifulSoup(r.text,'lxml')
print(soup2.title)
test_detail_url=soup2.find_all("a",string=re.compile("[0-9]+年[0-9]+月[0-9]+日 [0-9]{2}:[0-9]{2}"))[0].get("href").split("?")[-2]

r2=requests.get(url='https://weibo.com/6004281123/Is50X3Y2W?type=comment',headers=ff_header,cookies=ff_wb_cookie)
print(r2.url)

soup3=BeautifulSoup(r2.text,'lxml')
print(soup3.find_all("div"))

f=open("D://abc.html","w",encoding="utf-8")
for i in r2.text:
    f.write(i)
f.close()

test_html='''
<div class="WB_text">
            <a target="_blank" href="//weibo.com/6870015860" usercard="id=6870015860">废话一盆盆</a><a action-type="ignore_list" title="微博会员" target="_blank" href="https://vip.weibo.com/personal?from=main"><em class="W_icon icon_member5"></em></a>：我就想买点口罩，医用外科就行<img class="W_img_face" render="ext" src="//img.t.sinajs.cn/t4/appstyle/expression/ext/normal/e3/2018new_weixioa02_org.png" title="[微笑]" alt="[微笑]" type="face">        </div>
'''

soup4=BeautifulSoup(test_html,'lxml')
print(soup4.div.contents)