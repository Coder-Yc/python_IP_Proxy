import requests
from lxml import etree
import re
import time
import ip
import pandas as pd

start_time=time.time()

i=1
headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36',
    'accept-encoding':'gzip, deflate, br'
    }


def main(startNo,endNo):

    for i in range(startNo,endNo):
        k = i
        proxies = ip.randonm_ip()
        print(proxies)
        url= 'https://zh.58.com/ershoufang/p'+str(i)
        print(url)
        page_text = requests.get(url = url,headers = headers,proxies = proxies).text
        print()
        tree = etree.HTML(page_text)
        d = tree.xpath('//*[@id="__layout"]/div/section/section[3]/section[1]/section[2]/div')
        d = d[0]
        name = d.xpath('//div/a/div[2]/div[1]/section/div[2]/p[1]/text()')
        local1 = d.xpath('//div/a/div[2]/div[1]/section/div[2]/p[2]/span[1]/text()')
        local2 = d.xpath('//div/a/div[2]/div[1]/section/div[2]/p[2]/span[2]/text()')
        local = []
        for i in range(len(local1)):
            local.append(local1[i]+local2[i])
        area1 = d.xpath('//div/a/div[2]/div[1]/section/div[1]/p[2]/text()')
        # print(area)
        area = []
        for j in area1:
            a = re.findall(r'\d+',j)[0]
            area.append(a)
        result=pd.DataFrame({"name":name,"area":area})
        # time.sleep(1)
        print("----------已爬取第{}页数据------------".format(k))
        i+=1
    end_time=time.time()#⏲
    all_time=end_time-start_time
    print('over')
    print("总时间位",all_time)
if __name__ =="__main__":


    startNo = input("输入开始的页数：")
    endNo = input("输入结束的页数：")
    main(startNo,endNo)