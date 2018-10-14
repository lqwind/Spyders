# -*- coding: utf-8 -*-
"""
Created on Sun Aug 19 10:26:32 2018

@author: Luis.Lu
"""

import urllib3
from bs4 import BeautifulSoup

defurl = 'http://ng.letwx.com/supermarketshop/floorlist?letwxid=23&floor='

http = urllib3.PoolManager()

def defload(floor):
    
    req = http.request(
            'GET',
            defurl + floor,
            headers = {
                    'Host': 'ng.letwx.com',
                    'Connection': 'keep-alive',
                    'User-Agent': 'Mozilla/5.0 (Linux; Android 7.1.1; OS105 Build/NMF26X; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/044203 Mobile Safari/537.36 MicroMessenger/6.6.7.1321(0x26060739) NetType/WIFI Language/zh_CN',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,image/wxpic,image/sharpp,image/apng,*/*;q=0.8',
                    'Referer': 'http://ng.letwx.com/supermarketshop/index?letwxid=23&letwxauthid=oFwGKjlxMWfE',
                    'Accept-Encoding': 'gzip, deflate',
                    'Accept-Language': 'zh-CN,en-US;q=0.8'
                    
                    }
            
            )
    
    html = req.data.decode()
    soup = BeautifulSoup(html, "lxml")
    
    fetch_tag(floor, soup)
#<span class="font-9"><span class="bold">-1F</span>&nbsp;&nbsp;男士精品馆</span>

def fetch_tag(floor, data):    
    result_name = data.find_all('span', class_='font-9 hidden-e logo-p')
    #result_category = data.find_all('span', class_='font-9')
    

    for i in range(len(result_name)):
        shopName = result_name[i].text.strip()
        
        print(floor+'F', shopName)

        
if __name__ == '__main__':
    defload('9')
    defload('10')
    #defload('5')
    