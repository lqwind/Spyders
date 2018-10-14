# -*- coding: utf-8 -*-
"""
Created on Wed Sep  5 13:24:53 2018

@author: Luis.Lu

待取数据在HTML标签中
"""

import urllib3
import requests
from bs4 import BeautifulSoup
import re
import time
import random
import pymssql
from PIL import Image
from io import BytesIO
import os
import datetime
from aip import AipOcr
import logging
import logging.config
from decimal import Decimal
import urllib


requests.packages.urllib3.disable_warnings()

""" BAIDU APPID AK SK """
APP_ID = '11793530'
API_KEY = 'yFbKKeooeTGQ5aGc1RUYG2yz'
SECRET_KEY = 'WcNM0FooXc2lENQ8BVGkg8FFpANxGduj'


"""配置日志格式"""
logger = logging.getLogger(__name__)

time_stamp = datetime.datetime.strftime(datetime.datetime.now(),'%Y%m%d')
#log_path = os.path.dirname(os.getcwd()) + "/logs/"
log_path = os.getcwd() + "/"
log_name = log_path + time_stamp + ".txt"
fh = logging.FileHandler(log_name, mode = 'a', encoding = 'utf-8')  #文本输出
ch = logging.StreamHandler()                    #控制台输出

fh.setLevel(level = logging.DEBUG)
ch.setLevel(level = logging.INFO)

formatter = logging.Formatter("[%(asctime)s] %(levelname)s [%(filename)s：%(lineno)d] %(message)s")
fh.setFormatter(formatter)
ch.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(ch)

#logging.basicConfig(level = logging.DEBUG,
##                    format = '[%(asctime)s] %(levelname)s [%(funcName)s: %(filename)s, %(lineno)d] %(message)s',
#                    format = '[%(asctime)s] %(levelname)s [%(filename)s：%(lineno)d] %(message)s',
#                    datefmt = '%Y-%m-%d %H:%M:%S',
#                    filename = log_name,
#                    filemode = 'w')


"""
数据库：PublicData
数据表：FGJ_Housing
字段名：(2018.9.26)
HousingID	int	Unchecked
Name	nvarchar(100)	Checked
Area	numeric(6, 2)	Checked
Price	numeric(8, 2)	Checked
Status	nvarchar(50)	Checked
PriceJPG	image	Checked
PricePath	nvarchar(100)	Checked
BuildingName	nvarchar(100)	Checked
ProjectName	nvarchar(100)	Checked
BuildingID	nvarchar(50)	Checked
ProjectID	nvarchar(50)	Checked

"""
conn = pymssql.connect(host = "10.1.65.51:1433", 
                       user = "sa", 
                       password = "xintiandi@1234", 
                       database = "PublicData")
cursor = conn.cursor()

if not cursor:
    raise Exception('数据库连接失败，取消执行！')

g_folder_root = "E:/WorkSpace/"
g_folder_building = ""
g_cnt_house_in_building = 0
g_cnt_house_in_project = 0
g_pic_cnt = 0

"""房管局访问的间隔时间"""
fgj_min_sec = 5
fgj_max_sec = 15
"""其他访问的间隔时间"""
qt_min_sec = 5
qt_max_sec = 10


def get_html(url, cookie):
#    with open('config_Proxys.txt') as fp:
#        list_proxies = fp.read().splitlines()
#        str_proxy = random.choice(list_proxies)
#        logger.info("Proxy URL：" + str_proxy)
        
#    with open('config_Headers.txt') as fh:
#        list_headers = fh.read().splitlines()
#        str_header = random.choice(list_headers)
#        logger.info("User-Agent：" + str_proxy)
        
    proxy = urllib3.ProxyManager('http://61.135.217.7:80',headers={'user-agent': 'Mozilla/5.0 (Darwin; FreeBSD 5.6; en-GB; rv:1.9.1b3pre)Gecko/20081211 K-Meleon/1.5.2'})

    req = proxy.request(
        'GET',
        url,
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
#            'Host': 'fgj.wuhan.gov.cn',
#            'Connetction': 'keep-alive',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,en-US;q=0.8',
            'Cookie': cookie
        },
        preload_content = False,
        retries = 2,
        timeout = urllib3.Timeout(connect = 10, read = 10)
    )

    html = req.data.decode('utf-8')

    return html


# 第二层项目信息
def get_project_info(buildingList_url, cookie):
    
    html = get_html(buildingList_url, cookie)

    soup = BeautifulSoup(html, 'lxml')
    #    print(soup.prettify())

    building_tag = soup.select('.tabls a')[0]
    building_attr = building_tag['onclick']

    re_attr = re.compile(r"/(.+)'\)")
    building_url = 'http://fgj.wuhan.gov.cn/' + re_attr.findall(building_attr)[0]

    name = soup.select('.tabls #xiangmmc')[0].get_text().strip()
    position = soup.select('.tabls #MenPhm')[0].get_text().strip()
    house = soup.select('.tabls #zts')[0].get_text().strip()
    building = soup.select('.tabls #ZDongS')[0].get_text().strip()

    print(name, position, house, building)

    return building_url


# 第三层项目楼栋信息
def get_building_list_info(building_list_url, cookie):
    urls = []

    html = get_html(building_list_url, cookie)
    soup = BeautifulSoup(html, 'lxml')
    #    print(soup.prettify())
        
    """
页面代码：
<div class="tabls" style="padding-top: 10px;">				
<table cellspacing="1" cellpadding="0" width="100%" border="0">                    
<tr align="middle" style="background:#ADD8E6;"> 
<td width="42%" height="30" >楼栋名称 </td>                         
<td width="11%" >建筑结构</td>
<td width="11%" >总层数</td>
<td width="13%" >总套数 </td>
</tr>                        
<tr>
<td align="center">
<a href='javascript:void(0);' onclick="openEncodeURL('/zz_spfxmcx_fang.jspx?dengJh=阳1700480&houseDengJh=阳0003001');return false;" target='_blank' style='color: blue;'>新建居住、商业及商务设施项目（碧桂园滨江项目）1</a>
</td>
<td align="center">钢混</td>
<td align="center">52</td>
<td align="center">154</td>									
</tr>
<tr>
<td align="center">
<a href='javascript:void(0);' onclick="openEncodeURL('/zz_spfxmcx_fang.jspx?dengJh=阳1700480&houseDengJh=阳0002906');return false;" target='_blank' style='color: blue;'>新建居住、商业及商务设施项目（碧桂园滨江项目）2#</a>
</td>
<td align="center">框剪</td>
<td align="center">25</td>
<td align="center">108</td>									
</tr>
</table>
</div>
    """
    
    re_attr = re.compile(r"/(.+)'\)")
    # 获取表格中楼栋的url链接
    building_tag = soup.select(".tabls tr a['onclick']")
    for a in building_tag:
        house_attr = a['onclick']
        house_url = 'http://fgj.wuhan.gov.cn/' + re_attr.findall(house_attr)[0]
        urls.append(house_url)

    # 获取表格中楼栋的信息
    building_list = soup.select(".tabls tr td['align'='center']")
    for tr in building_list:
        logger.debug("楼栋信息：" + tr.get_text().strip())

    return urls


# 第四层单楼栋信息
def get_building_info(building_url, cookie, project_id, building_id):
    house_urls = []
    house_flags = []
    str_data = ""
    
    html = get_html(building_url, '')
    soup = BeautifulSoup(html, 'lxml')
    #    print(soup.prettify())

    """
    <div class="xinjia" style="position: absolute;">
    <table class="tab_css_1" style="margin-top:10px;">
    <tr style="background:#ADD8E6;">
    <th style="color: #fff;font-size: 16px;font-weight: 400;">栋号</th>
    <th style="color: #fff;font-size: 16px;font-weight: 400;">单元</th>
    <th style="color: #fff;font-size: 16px;font-weight: 400;">层数</th>
    <th style="color: #fff;font-size: 16px;font-weight: 400;">室号</th>
    </tr>							
    <tr>  									
    <td align="center">1</td>	
    <td align="center">/</td>
    <td align="center">1-2</td>										 
    <td align="center" bgcolor="#FFFF00"><a href="http://119.97.201.22:8080/chktest2.aspx?gid=A2BAF2BF-77CA-4786-A023-3ACCEFF1A95C" target=_blank>1</a> </td>
    </tr>
    <tr>  									
    <td align="center">1</td>	
    <td align="center">1</td>
    <td align="center">3</td>										 
    <td align="center" bgcolor="#FFFF00"><a href="http://119.97.201.22:8080/chktest2.aspx?gid=03F8526D-83DC-4A8D-B944-B2316831CB28" target=_blank>1</a> </td>
    </tr>
    </table>
    </div>
    """

    # 获取表格中房间的url链接
    house_link = soup.select(".tab_css_1 tr a['target']")
    house_color = soup.select(".tab_css_1 tr td['bgcolor']")

    if house_link:
        for a in house_link:
            house_url = a['href']
            house_urls.append(house_url)
        
        for tr in house_color:
            house_attr = tr.get('bgcolor')
    
            if house_attr == '#FF0000':
                house_flag = '已网上销售'
            elif house_attr == '#CCFFFF':
                house_flag = '未销（预）售'
            elif house_attr == '#000000':
                house_flag = '限制出售'
            elif house_attr == '#FFFF00':
                house_flag = '已抵押'
            elif house_attr == '#CC0099':
                house_flag = '已查封'
            elif house_attr == '#FFFF00':
                house_flag = '已抵押已查封'
            else:
                house_flag = '未知状态'
                
            house_flags.append(house_flag)
    
        global g_cnt_house_in_building
        g_cnt_house_in_building = len(house_urls)
        
        if len(house_urls) != len(house_flags):
            raise Exception("页面标签错误：房屋的链接总数与销售状态总数不相等 >>> " + building_url)
        
        for i in range(len(house_urls)):
            is_value = house_urls[i][len(house_urls[i])-10:len(house_urls[i])]
            
            if is_value != '0000000000':
    
                logger.debug("---楼栋号 "+building_id+" ，第"+str(i)+"个房屋 正在执行 >>> " + house_urls[i])
                
                str_data += get_house_info(house_urls[i], cookie)
                str_data += "','" + house_flags[i] + "','" + building_id + "','" + project_id + "','" + datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d') + "'),"
                
                if str_data.find("未保存") > 0:
                    logger.debug("---楼栋号 "+building_id+" ，第"+str(i)+"个房屋：无楼栋关键字*栋*，取消执行")
                    raise Exception("页面楼栋名称错误：无关键字*栋*，程序关闭")
    
                if ( i != 0 and i % 20 == 0 ):
                    sql_param = str_data.rstrip(",")
                    sql = """insert into FGJ_Housing("Name", "Area", "PricePath", "BuildingName", "Status", "BuildingID", "ProjectID", "AddDate") values %s """ % sql_param
                    
                    logger.debug("---第"+str(i)+"批， Insert SQL >>> " + sql)
                    
                    cursor.execute(sql)
                    conn.commit()
                    
                    str_data = ""
                
                request_sleep(fgj_min_sec, fgj_max_sec)
                
            else:
                logger.debug("---楼栋号 "+building_id+" ，第"+str(i)+"个房屋 >>> 暂无备案价")
    
        if str_data != "":
            sql_param = str_data.rstrip(",")
            sql = """insert into FGJ_Housing("Name", "Area", "PricePath", "BuildingName", "Status", "BuildingID", "ProjectID", "AddDate") values %s """ % sql_param
            
            logger.debug("---最后一批， Insert SQL >>> " + sql)
            
            cursor.execute(sql)
            conn.commit()
        else:
            logger.debug("---无最后一批 SQL or 该楼栋所有房屋均无备案价")
    else:
        logger.debug("该楼栋页面访问失效 >>> " + building_url)
    
    return None


# 第五层室号信息
def get_house_info(house_url, cookie):
    str_data = ''
    str_txt = "('"

    html = get_html(house_url, cookie)
    soup = BeautifulSoup(html, 'lxml')
    #    print(soup.prettify())

    re_no = re.compile(r"房屋座落(.*)预售许")
    re_area = re.compile(r"预测面积（平方米）(.*)实测")
    
    result_tab = soup.select(".container td")

    if result_tab:
        price_attr = soup.select(".container td img")[0].get('src')
        price_url = 'http://119.97.201.22:8080/' + price_attr

        for td in result_tab:
            str_data += td.get_text().strip()

        house_name = re_no.findall(str_data)
        house_area = re_area.findall(str_data)
        
        global g_folder_building
        if g_folder_building == "":
#            folder_proj = house_name[0][:house_name[0].find("栋")+1]
            g_folder_building = house_name[0][:house_name[0].find("栋")+1]
            
        short_path = save_image(price_url)
                
        str_txt += house_name[0] + "','" + house_area[0] + "','" + short_path + "','" + house_name[0][:house_name[0].find("栋")+1]
    else:
        logger.debug("该房屋页面访问失效 >>> " + house_url)

    return str_txt


def mkdir(path):
    path = path.strip()
    path = path.rstrip("\\")

    is_exists = os.path.exists(path)

    if not is_exists:
        os.makedirs(path)

        return True
    else:
        return False


def save_image(url):
    
    request_sleep(qt_min_sec, qt_max_sec)
    
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    
#    local_folder = folder_root + folder_proj
    local_folder = g_folder_root + g_folder_building
    
    str_now = datetime.datetime.strftime(datetime.datetime.now(), '%H%M%S%f')
    
    if g_folder_building != "":
        mkdir(local_folder)
    
        full_path = local_folder + "/" + str_now + ".jpg"
        
        img.save(full_path)
        
        logger.debug("------备案价图片保存路径 >>> " + full_path)
    
        return g_folder_building + "/" + str_now + ".jpg"
    else:
        return "未保存因无图片文件夹名"


def data_to_txt(file_name, contents):
    fh = open(file_name, 'w')
    fh.write(str(contents))
    fh.close()


def close_mssql(conn):
    return conn.close()


""" 读取图片 """
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()
    

def ocr_jpg(full_path):
    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    
    image = get_file_content(full_path)
    
    """ 如果有可选参数 """
    options = {}
    options["language_type"] = "CHN_ENG"   #识别语言类型，CHN_ENG：中英文混合
    options["detect_direction"] = "false"  #是否检测图像朝向
    options["detect_language"] = "false"
    options["probability"] = "false"  # 行置信度信息
    
    """ 调用通用文字识别, 图片参数为本地图片，可参数2为options """
    dict_result = client.basicGeneral(image, options)
    
    if dict_result['words_result']:
        value = dict_result['words_result'][0]['words']
    
        logger.debug(dict_result)
        
        if value.find(".") > 0:
            return value.split(".")[0]
        else:    
            if len(value) == 7:
                return value[:len(value)-2]
            elif len(value) == 6:
                return value[:len(value)-1]
            elif len(value) == 5:
                return value
            elif len(value) == 4:
                return value
            else:
                return '0'
    else:
        return '0'
    
    
""" 查询数据库JPG路径，调用OCR识别，再更新数据库"""
def modify_price(str_where):
    sql = "select pricePath from FGJ_Housing where (price is null or price=0) and ProjectID='"+str_where+"'"
    
    cursor.execute(sql)
    list_result = cursor.fetchall()
    
    global g_pic_cnt
    g_pic_cnt = str(cursor.rowcount)
    
    logger.debug("待识别图片记录总数：" + g_pic_cnt)
    
    if list_result:
        if cursor.rowcount != 0:            
            for i, item in enumerate(list_result):
                
                pic_path = g_folder_root + item[0]
                
                value = ocr_jpg(pic_path)
                
                logger.debug("第"+str(i)+"个图片记录 正在执行 >>> " + item[0])
                
                sql_update_price(value, item[0])
                
                request_sleep(qt_min_sec, qt_max_sec)
        else:
            logger.debug("数据库图片路径记录查询无记录，待检查查询条件")
    else:
        logger.debug("数据库图片路径查询失败")
        
    return None


def sql_update_price(price_value, price_where):    
    sql = "update FGJ_Housing set Price=" + price_value + " where PricePath='"+ price_where +"'"

    logger.debug("预售价， Update SQL >>> " + sql)
            
    cursor.execute(sql)
    conn.commit()
    
    return None

"""Url中文与编码之间互转"""
def url_transfer(str_id):
    list_rtn = []
    
    if type(str_id) == str:
        if str_id.find("%") >= 0:
    #        str_rtn = urllib.parse.unquote(content)
            return str_id
        else:
            return urllib.parse.quote(str_id)
    elif type(str_id) == list:
        for item in str_id:
            if item.find("%") >= 0:
                list_rtn.append(item)
            else:
                list_rtn.append(urllib.parse.quote(item))
        return list_rtn
    else:
        return str_id
    

"""系统进程休眠，控制页面请求间隔"""
def request_sleep(sleep_min, sleep_max):
    """
    需注意：可以传递给Decimal整型或者字符串参数，但不能是浮点数据，因为浮点数据本身就不准确。
    Decimal还可以用来限定数据的总位数。
    """
    f_sec = Decimal(str(random.uniform(sleep_min, sleep_max))).quantize(Decimal('0.0'))
    
    time.sleep(f_sec)
    
    return None

if __name__ == '__main__':
    
    houseCookie = 'ASP.NET_SessionId=w4dnub5jkwmhdg2su0qv4a32'
    url_mx = 'http://fgj.wuhan.gov.cn/zz_spfxmcx_mx.jspx?dengJh=%E5%B2%B81700701'
    url_loupan = 'http://fgj.wuhan.gov.cn/zz_spfxmcx_loupan.jspx?dengJh='
    url_fang = 'http://fgj.wuhan.gov.cn/zz_spfxmcx_fang.jspx?dengJh='
    
    str_dengJh = '岸1700755'
    list_houseDengJh = []

    start_time1 = datetime.datetime.now()
    
    try:
        param_dJh = url_transfer(str_dengJh)
                
        """获取所有楼栋Url链接"""
        buildingList_url = url_loupan + param_dJh
        urls = get_building_list_info(buildingList_url, "")
        
        for item in urls:
            list_houseDengJh.append(item[item.find("=", 60, 80)+1:len(item)])
        
        param_houseDJh = url_transfer(list_houseDengJh)
        
        
        """获取单楼栋房屋信息"""
        logger.debug("待执行楼栋总数：" + str(len(list_houseDengJh)))
        logger.debug("待执行楼栋分别为 >>> " + "' , '".join(list_houseDengJh))

        for i, item in enumerate(param_houseDJh):
            
            start_time2 = datetime.datetime.now()
            
            building_url = url_fang + param_dJh + "&houseDengJh=" + item
            
            logger.debug("第" +str(i+1)+ "个楼栋 正在执行 >>> "+ building_url)

            get_building_info(building_url, houseCookie, param_dJh, item)
            
            end_time2 = datetime.datetime.now()
            
            logger.debug("当前楼栋 ***"+g_folder_building+"***，其房屋总数：" + str(g_cnt_house_in_building))
            logger.debug("当前楼栋 用时：" + str(end_time2 - start_time2).split(".")[0])
                
            g_cnt_house_in_project = g_cnt_house_in_project + g_cnt_house_in_building
            
            g_folder_building = ""            
            g_cnt_house_in_building = 0
            
        logger.debug("*****程序（楼栋&房屋）已经执行完成*****")
        logger.debug("房屋总数：" + str(g_cnt_house_in_project))
            
        """批量更新预售价"""        
#        modify_price(param_dJh)
#        logger.debug("*****程序（更新预售价格）已经执行完成*****")
#        logger.debug("预售价识别总数：" + str(g_pic_cnt))
        
        
        """尚未完成定期更新房屋销售状态的代码"""
    
    except Exception as e:
        logger.error(e)
        print(e)
    finally:
        """关闭数据库连接"""
        close_mssql(conn)
        
        end_time1 = datetime.datetime.now()
        
        logger.debug("累计用时：" + str(end_time1 - start_time1).split(".")[0])

    

'''

岸0002218 -- 岸0002217 -- 岸0002219 -- 岸0002220 -- 岸0002216



岸 = %E5%B2%B8
阳 = %E9%98%B3
青 = %E9%9D%92



'''
