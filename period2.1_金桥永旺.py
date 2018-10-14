# -*- coding: utf-8 -*-
"""
Created on Tue Aug  7 14:44:39 2018

@author: Luis.Lu
"""

import urllib3
from bs4 import BeautifulSoup


defurl = 'http://jinqiao.aeonmall-china.com/shop/lists/'
pageurl = 'http://jinqiao.aeonmall-china.com/shop/lists//page:'

http = urllib3.PoolManager()

def defload():
    
    req = http.request(
            'GET',
            defurl,
            headers = {
                    'Host': 'jinqiao.aeonmall-china.com',
                    'Connection': 'keep-alive',
                    'User-Agent': 'Mozilla/5.0 (Linux; Android 7.1.1; OS105 Build/NMF26X; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/044203 Mobile Safari/537.36 MicroMessenger/6.6.7.1321(0x26060739) NetType/WIFI Language/zh_CN',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,image/wxpic,image/sharpp,image/apng,*/*;q=0.8',
                    'Referer': 'http://jinqiao.aeonmall-china.com/',
                    'Accept-Encoding': 'gzip, deflate',
                    'Accept-Language': 'zh-CN,en-US;q=0.8'
                    
                    }
            
            )
    
    html = req.data.decode()
    soup = BeautifulSoup(html, "lxml")
    
    fetch_tag(soup)


def load(pageNo):
    req = http.request(
            'GET',
            pageurl + pageNo,
            headers = {
                    'Host': 'jinqiao.aeonmall-china.com',
                    'Connection': 'keep-alive',
                    'Accept': 'text/html, */*; q=0.01',
                    'User-Agent': 'Mozilla/5.0 (Linux; Android 7.1.1; OS105 Build/NGI77B; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/044204 Mobile Safari/537.36 MicroMessenger/6.6.7.1321(0x26060739) NetType/WIFI Language/zh_CN',
                    'Referer': 'http://jinqiao.aeonmall-china.com/shop/lists/',
                    'Accept-Encoding': 'gzip, deflate',
                    'Accept-Language': 'zh-CN,en-US;q=0.8'
                    }
            )
    
    html = req.data.decode()
    soup = BeautifulSoup(html, "lxml")
    
    fetch_tag(soup)

def fetch_tag(data):    
    result_name = data.find_all('h3', class_='shopName')
    result_other = data.find_all('p', class_='area')
    
    for i in range(len(result_name)):
        #print(result_name[i].text.strip())
        #print(result_other[i].text.strip().replace('\n',''))
        shopName = result_name[i].text.strip()
        shopOther = ''.join(result_other[i].text.split())#.split('／')
        
        print(shopName, shopOther)
'''
        for j in range(len(shopOther)):
            print(shopName, shopOther[j])
'''
def get_url():
    urls = []
    
    for i in range(1,10):
        if i != 1:
            url = 'http://jinqiao.aeonmall-china.com/shop/lists//page:%d' % i
        else:
            url = 'http://jinqiao.aeonmall-china.com/shop/lists/'

    return urls
    
    
if __name__ == '__main__':
    #defload()
    load('7')
    load('8')
    load('9')





