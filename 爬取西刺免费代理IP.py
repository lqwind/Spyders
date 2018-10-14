# -*- coding: utf-8 -*-
"""
Created on Wed Oct 10 15:13:56 2018

@author: Luis.Lu
"""

from bs4 import BeautifulSoup
import urllib3
import urllib
import threading 

#获取网页HTML码
def getContent(url):
    http=urllib3.PoolManager()
    response=http.request('get',url)
    print('网页 %s 返回代码：%s'%(url,response.status))
    return response.data

#测试代理是否可用
def testProxy(pro):
    protocol=pro.split(':')[0]

    #设置urllib中的代理IP
    opener=urllib.request.build_opener( urllib.request.ProxyHandler({protocol:pro}) )
    urllib.request.install_opener(opener)

    #若能打开test_url则保存该代理IP
    try:
        response=urllib.request.urlopen(test_url,timeout=timeout)
        response.read()
    except:
        print("代理IP：%s 无效"%pro)
    else:
        if pro not in alive_Proxys:
            alive_Proxys.append(pro)

#获取代理IP
Proxys=[]
pages=5
#爬去西刺10页的代理IP
for i in range(0,pages):
    url='http://www.xicidaili.com/nn/%d'%(i+1)
    content=getContent(url) #获取网页内容
    if content!=None:
        soup=BeautifulSoup(content,'lxml')

        #分析网页源码得，tr标签中class=''或class='odd'都满足
        Tags=soup.find_all('tr',attrs={'class':'odd'})+soup.find_all('tr',attrs={'class':''})[1:]

        #获取该页所有的代理IP
        for tag in Tags:
            t=tag.find_all('td')
            ip=t[1].get_text()
            post=t[2].get_text()
            protocol=t[5].get_text().lower()
            Proxys.append(protocol+'://'+ip+':'+post)

print('共爬取了%d个代理IP'%len(Proxys))


#测试代理IP是否可用
test_url='http://fgj.wuhan.gov.cn'
n=10 #线程数
timeout=3 
alive_Proxys=[] #保存可用代理

pro=Proxys.pop()
while Proxys:
    T=[]
    for i in range(n):
        t=threading.Thread(target=testProxy,args=(pro,))
        T.append(t)
        t.start()
        if Proxys:
            pro=Proxys.pop()
        else:
            break 

    #阻塞n个进程结束后再重新创建线程
    for t in T:
        t.join()

print("可用代理IP：%d"%len(alive_Proxys))

#写入文件
with open('Proxys.txt','w') as fp:
    for line in alive_Proxys:
        fp.write("%s\n"%line)
print("写入完毕")

