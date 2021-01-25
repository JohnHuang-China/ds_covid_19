
from bs4 import BeautifulSoup
test_html='''<div class="WB_text">
            <a target="_blank" href="//weibo.com/6870015860" usercard="id=6870015860">废话一盆盆</a><a action-type="ignore_list" title="微博会员" target="_blank" href="https://vip.weibo.com/personal?from=main"><em class="W_icon icon_member5"></em></a>：我就想买点口罩，医用外科就行<img class="W_img_face" render="ext" src="//img.t.sinajs.cn/t4/appstyle/expression/ext/normal/e3/2018new_weixioa02_org.png" title="[微笑]" alt="[微笑]" type="face">        </div>'''

soup4=BeautifulSoup(test_html,'lxml')
for k in soup4.div.contents:
    print((k))