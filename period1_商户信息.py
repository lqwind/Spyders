# -*- coding: utf-8 -*-
"""
Created on Tue Jul 31 16:02:18 2018

@author: Luis.Lu

特点：爬取Json格式的数据


"""

#https://m.dianping.com/shopping/node/brand/brandwall.html?shopid=6789187&cityid=16&floor=3%E5%B1%82&latitude=30.61131&longitude=114.30465&dpid=-6564837699093534559&product=dpapp

import urllib3
import requests
import json


requests.packages.urllib3.disable_warnings()

http = urllib3.PoolManager()

defUrl = 'https://m.dianping.com/shopping/node/brand/brandwall.html'

cid_wuhan = '16'
sid_hj = '6789187'       #荟聚中心
sid_gg = '56781791'      #武汉国际广场
sid_wg = '50486936'      #武商广场
sid_sm = '60398451'      #世贸广场
sid_ljhwd = '58241615'   #菱角湖万达
sid_xpm = '1935490'      #销品茂
sid_jqyw = '96357495'    #金桥永旺
sid_mj = '90936314'      #M+购物中心

sid = sid_mj
cid = cid_wuhan

req = http.request(
        'GET',
        defUrl,
        fields = {'shopid': sid, 'cityid': cid, 'floor': '1%E5%B1%82'},
        headers = {
                'User-Agent': 'Mozilla/5.0 (Linux; Android 7.1.1; OS105 Build/NMF26X; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.97 Mobile Safari/537.36 TitansNoX/11.6.12.5 KNB/1.2.0 android/7.1.1 dp/com.dianping.v1/10.2.14 com.dianping.v1/10.2.14',
                'Host': 'm.dianping.com',
                'Connetction': 'keep-alive',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,en-US;q=0.8',
                }
        )



def load(floorNo, pageNo, pageSize):    
    req = http.request(
            'GET',
            'https://mapi.dianping.com/shopping/getfloorshoplist?shopid='+sid+'&cityid='+cid+'&page='+pageNo+'&pageSize='+pageSize+'&floor='+floorNo+'%E5%B1%82',
            headers = {
                    'User-Agent': 'Mozilla/5.0 (Linux; Android 7.1.1; OS105 Build/NMF26X; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.97 Mobile Safari/537.36 TitansNoX/11.6.12.5 KNB/1.2.0 android/7.1.1 dp/com.dianping.v1/10.2.14 com.dianping.v1/10.2.14',
                    'Host': 'mapi.dianping.com',
                    'Connetction': 'keep-alive',
                    'Origin': 'https://m.dianping.com',
                    'Accept': '*/*',
                    'Accept-Encoding': 'gzip, deflate',
                    'Accept-Language': 'zh-CN,en-US;q=0.8',
                    }
            
            )


    loadResult = json.loads(req.data)   
    loadStatus = loadResult.get('code', False)
    
    if loadStatus == 200:
        shopData = fetch_json(floorNo, loadResult)
        #ata_to_txt('shopList.txt', shopData)
    else:
        print('load fail')
        #print(loadResult)

   

def fetch_json(floorNo, json_data):
    data = json_data['msg']
    shopList = data['shopInfoList']
    shop = []
    
    for each in shopList:
        shopInfo = {}
        if each.get('shopName', False):
            shopInfo['floor'] = floorNo+'F'
            #shopInfo['id'] = each['shopId']
            shopInfo['shopName'] = each['shopName']
            shopInfo['categoryName'] = each['categoryName']
            print(floorNo+'F', each['shopName'], each['categoryName'])
            shop.append(shopInfo)
    return shop


def data_to_txt(file_name, contents):
    fh = open(file_name, 'w')
    fh.write(str(contents))
    fh.close()
    
    

if __name__ == '__main__':
    #for i in range(1,1):
        #floorNo, pageNo, pageSize
        load('1', '1', '200')
        load('2', '1', '200')
        #load('6', '1', '200')
        #load('4', '1', '200')
        #load('5', '1', '200')        
        #load('6', '1', '200')


