import urllib.request
import urllib
import re
import os

#from bs4 import BeautifulSoup
url0='https://www.stockio.com/free-icons/'
hea = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0'
def getHtml(url):
    req=urllib.request.Request(url)
    req.add_header('User-Agent',hea)
    req.add_header("GET",url0)
    resp=urllib.request.urlopen(req)
    html=resp.read().decode('utf-8')
    return html


def dl(url):
    r=urllib.request.Request(url)
    r.add_header('User-Agent',hea)
    rp=urllib.request.urlopen(r).read()
    with open(url.split("/")[-1],"wb") as f:
        f.write(rp)
        f.flush()
    
def getDownloadUrl(url):
    html=getHtml(url)
    reg=re.compile(r'"https://www.stockio.com/free-icon/\S+"')
    for u in reg.findall(html):
        u=u.strip('\"')
        #print(u)
        h=getHtml(u)
        pat=re.compile(r'download/[0-9]+')
        u1st=pat.findall(h)[0]
        dlurl='https://www.stockio.com/'+u1st
        #print(dlurl)
        dl(dlurl)

getHtml(url0)
print("opening successful")
print(r'^"https://www.stockio.com/free-icon/.+"$')

for i in range(1,76):
    url1=url0+'?page='+str(i)
    getDownloadUrl(url1)
