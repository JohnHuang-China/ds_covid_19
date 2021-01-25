import requests
import datetime
from bs4 import BeautifulSoup

base_date=datetime.date(2019,12,31)
ff_header={
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0',
    }
ff_wb_cookie={
	"_s_tentry": "login.sina.com.cn",
	"ALF": "1643016908",
	"Apache": "8175450816258.878.1611392463737",
	"SCF": "Aht7HwEKaZ1k0RUq1iQj4c9kDaJPz3rafhVsgpvPK50yIp36mKV4yD1GxHise3NUFmkg72lkO-uG2XsJuFMXGTc.",
	"SINAGLOBAL": "1554178379884.7576.1586852533034",
	"SSOLoginState": "1611392460",
	"SUB": "_2A25NCU8eDeRhGeRP71MX9CbIyzyIHXVufyfWrDV8PUNbmtANLXfckW9NTgX4twIUDqUu9Q6ZUk2KmkqiY_DIqcTK",
	"SUBP": "0033WrSXqPxfM725Ws9jqgMF55529P9D9W5X-m-swu9eX0w8nPEixiWy5JpX5KMhUgL.FozpSh2cShnXeh52dJLoIpRLxK-LBo5L12qLxKnL1K.LB-zLxKBLBonLBoqEe0et",
	"ULV": "1611392463745:34:3:3:8175450816258.878.1611392463737:1611312692145",
	"UOR": ",,www.baidu.com",
	"WBStorage": "8daec78e6a891122|undefined",
	"webim_unReadCount": "{\"time\":1611477455908,\"dm_pub_total\":0,\"chat_group_client\":999,\"chat_group_notice\":0,\"allcountNum\":1039,\"msgbox\":0}",
	"wvr": "6"
}
