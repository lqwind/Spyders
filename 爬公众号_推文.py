# -*- coding: utf-8 -*-
"""
Created on Tue Aug 14 17:52:16 2018

@author: Luis.Lu

武汉天地Live公众号全部历史消息（即推文）

wx_key有时效

"""

import urllib3
import requests
import re
import json
import time

requests.packages.urllib3.disable_warnings()


http = urllib3.PoolManager()

def main(wx_key, defUrl):
    req = http.request(
            'GET',
            defUrl,
            headers = {
                    'Host': 'mp.weixin.qq.com',
                    'Connection': 'keep-alive',
                    'User-Agent': 'Mozilla/5.0 (Linux; Android 7.1.1; OS105 Build/NGI77B; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/044204 Mobile Safari/537.36 MicroMessenger/6.6.7.1321(0x26060739) NetType/WIFI Language/zh_CN',
                    'x-wechat-key': wx_key,
                    'x-wechat-uin': 'MTM2OTY0OTU1',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,image/wxpic,image/sharpp,image/apng,*/*;q=0.8',
                    'Accept-Encoding': 'gzip, deflate',
                    'Accept-Language': 'zh-CN,en-US;q=0.8',
#                    'Cookie': 'sd_userid=85611532253350994; sd_cookie_crttime=1532253350994; pgv_info=ssid=s9177841282; pgv_pvid=9831643111; rewardsn=; wxtokenkey=777; wxuin=136964955; devicetype=android-25; version=26060739; lang=zh_CN; pass_ticket=1UKSiOjtKvelKDjOSSE71SRnJ+1bxDv17d/ueUCnVMM=; wap_sid2=CNvWp0ESXGVnM2N4dllMVENIR3R6Nll6cGR4ZGhoeVZOejRlQVN3WlFhVlRTZ1Zmc0EwOVh2dXlTdDd0RHdMTnBhNWNvZm9Pd2lyWnNVU1NNcUZOTl9kVjhteWVNd0RBQUF+MKHit9wFOA1AlU4='
                    }        
            )
    
    preHtml = req.data.decode('utf-8')
    reFormat = re.compile(r"msgList = '(.*)';")
    html = reFormat.findall(preHtml)
    
    if len(html) != 0:
        preResult = ''.join(html).replace('&quot;', '"').replace('\\', '')        
        
        if preResult is not None:
            value = json.loads(preResult)
            firLevel = value.get('list')
            
            for i in range(len(firLevel)):
                firTitle = firLevel[i].get('app_msg_ext_info').get('title')
                firUrl = firLevel[i].get('app_msg_ext_info').get('content_url')
                firFlag = firLevel[i].get('app_msg_ext_info').get('is_multi')            
                secLevel = firLevel[i].get('app_msg_ext_info').get('multi_app_msg_item_list')
                print(firTitle+','+firUrl)
                
                if firFlag == 1:
                    for j in range(len(secLevel)):
                        secTitle = secLevel[j].get('title')
                        secUrl = secLevel[j].get('content_url')
                        print(secTitle+','+secUrl)
    else:
        print('ERROR MSG: No Article Data in HTML')
# /mp/profile_ext?action=getmsg&__biz=MzAwMjg1MjAxMQ==&f=json&offset=10&count=10&is_ok=1&scene=124&uin=777&key=777&pass_ticket=1UKSiOjtKvelKDjOSSE71SRnJ%2B1bxDv17d%2FueUCnVMM%3D&wxtoken=&appmsg_token=972_brMnfgunHR097oa3PPOva_YkaAJxuUpW1najVg~~&x5=1&f=json
                       
                        

def load_more(loadUrl, loadCookies, accuPage):
    req = http.request(
            'GET',
            loadUrl,
            headers = {
                    
                    'Host': 'mp.weixin.qq.com',
                    'Connection': 'keep-alive',
                    'X-Requested-With': 'XMLHttpRequest',
                    'User-Agent': 'Mozilla/5.0 (Linux; Android 7.1.1; OS105 Build/NGI77B; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/044204 Mobile Safari/537.36 MicroMessenger/6.6.7.1321(0x26060739) NetType/WIFI Language/zh_CN',
                    'Accept': '*/*',
#                    'Referer': 'https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MzAwMjg1MjAxMQ==&scene=124&devicetype=android-25&version=26060739&lang=zh_CN&nettype=WIFI&a8scene=3&pass_ticket=1UKSiOjtKvelKDjOSSE71SRnJ%2B1bxDv17d%2FueUCnVMM%3D&wx_header=1',
                    'Accept-Encoding': 'gzip, deflate',
                    'Accept-Language': 'zh-CN,en-US;q=0.8',
                    'Cookie': loadCookies
                    }
            )
    html = req.data.decode('utf-8')
    reFormat = re.compile(r"app_msg_ext_info")
    isData = reFormat.findall(html)
    
    if len(isData) != 0:
        preValue = json.loads(html)
        msgList = preValue.get('general_msg_list')
        
        value = json.loads(msgList)
        firLevel = value.get('list')
        
        for i in range(len(firLevel)):
            firTitle = firLevel[i].get('app_msg_ext_info').get('title')
            firUrl = firLevel[i].get('app_msg_ext_info').get('content_url')
            firFlag = firLevel[i].get('app_msg_ext_info').get('is_multi')            
            secLevel = firLevel[i].get('app_msg_ext_info').get('multi_app_msg_item_list')
            print(firTitle+','+firUrl)
            
            if firFlag == 1:
                for j in range(len(secLevel)):
                    secTitle = secLevel[j].get('title')
                    secUrl = secLevel[j].get('content_url')
                    print(secTitle+','+secUrl)
    else:
        print('ERROR MSG: No LoadMore Article Data')

    
    

if __name__ == '__main__':
    defUrl = 'https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MzAwMjg1MjAxMQ==&scene=124&devicetype=android-25&version=26060739&lang=zh_CN&nettype=WIFI&a8scene=3&pass_ticket=1UKSiOjtKvelKDjOSSE71SRnJ%2B1bxDv17d%2FueUCnVMM%3D&wx_header=1'
    loadUrl = 'https://mp.weixin.qq.com/mp/profile_ext?action=getmsg&__biz=MzAwMjg1MjAxMQ==&f=json&offset=20&count=10&is_ok=1&scene=124&uin=777&key=777&pass_ticket=1UKSiOjtKvelKDjOSSE71SRnJ%2B1bxDv17d%2FueUCnVMM%3D&wxtoken=&appmsg_token=972_N%252BLD0RFec1odOP51SeeLfpYiOHeTW9hg9DCQCg~~&x5=1&f=json'
    wx_key = 'aa256902c0e8bb5b2452b208826804034f4afeea9778441b163a4e07724b34c0f6e80eff54877582336fec09e0768432d29a138a48bf0267e7786c87930cf55cf6f6dc15d3499df246065811967992b3'
    
#    defCookies = 'sd_userid=85611532253350994; sd_cookie_crttime=1532253350994; pgv_info=ssid=s9177841282; pgv_pvid=9831643111; rewardsn=; wxtokenkey=777; wxuin=136964955; devicetype=android-25; version=26060739; lang=zh_CN; pass_ticket=1UKSiOjtKvelKDjOSSE71SRnJ+1bxDv17d/ueUCnVMM=; wap_sid2=CNvWp0ESXGJjY21lQUpWdDRBZHB0MjM0OURJcEFQZnU3NjBfWlFRQmxWMlZZcVJwME1MekpjOXJtLWR2SHRTMnpNbTlicmhMSmJneXl6SGE5ZnRfdkJMblY2UWk4d0RBQUF+MKneuNwFOA1AlU4='
    loadCookies = 'sd_userid=85611532253350994; sd_cookie_crttime=1532253350994; pgv_info=ssid=s9177841282; pgv_pvid=9831643111; rewardsn=; wxtokenkey=777; wxuin=136964955; devicetype=android-25; version=26060739; lang=zh_CN; pass_ticket=1UKSiOjtKvelKDjOSSE71SRnJ+1bxDv17d/ueUCnVMM=; wap_sid2=CNvWp0ESXGJjY21lQUpWdDRBZHB0MjM0OURJcEFQZnU3NjBfWlFRQmxWMlZZcVJwME1MekpjOXJtLWR2SHRTMnpNbTlicmhMSmJneXl6SGE5ZnRfdkJMblY2UWk4d0RBQUF+MKneuNwFOA1AlU4='
    
    # Accumulative 累计的
    accuPage = '20'
    
#    main(wx_key, defUrl)
    print('had complete main(), sleep 5sec')
    time.sleep(5)
    load_more(loadUrl, loadCookies, accuPage)
    
'''
抓取默认页和加载页成功的参数组01
def
wx_key = aa256902c0e8bb5b2452b208826804034f4afeea9778441b163a4e07724b34c0f6e80eff54877582336fec09e0768432d29a138a48bf0267e7786c87930cf55cf6f6dc15d3499df246065811967992b3
url = https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MzAwMjg1MjAxMQ==&scene=124&devicetype=android-25&version=26060739&lang=zh_CN&nettype=WIFI&a8scene=3&pass_ticket=1UKSiOjtKvelKDjOSSE71SRnJ%2B1bxDv17d%2FueUCnVMM%3D&wx_header=1

load
url = https://mp.weixin.qq.com/mp/profile_ext?action=getmsg&__biz=MzAwMjg1MjAxMQ==&f=json&offset=10&count=10&is_ok=1&scene=124&uin=777&key=777&pass_ticket=1UKSiOjtKvelKDjOSSE71SRnJ%2B1bxDv17d%2FueUCnVMM%3D&wxtoken=&appmsg_token=972_N%252BLD0RFec1odOP51SeeLfpYiOHeTW9hg9DCQCg~~&x5=1&f=json
cookies = sd_userid=85611532253350994; sd_cookie_crttime=1532253350994; pgv_info=ssid=s9177841282; pgv_pvid=9831643111; rewardsn=; wxtokenkey=777; wxuin=136964955; devicetype=android-25; version=26060739; lang=zh_CN; pass_ticket=1UKSiOjtKvelKDjOSSE71SRnJ+1bxDv17d/ueUCnVMM=; wap_sid2=CNvWp0ESXGJjY21lQUpWdDRBZHB0MjM0OURJcEFQZnU3NjBfWlFRQmxWMlZZcVJwME1MekpjOXJtLWR2SHRTMnpNbTlicmhMSmJneXl6SGE5ZnRfdkJMblY2UWk4d0RBQUF+MKneuNwFOA1AlU4=
---------------
抓取默认页和加载页成功的参数组02

------------

'''