import requests
from bs4 import BeautifulSoup
import re
import time

ip = []
port = []
type =[]
def get_url(page):
    for i in range(int(page)):
        try:
            print('正在爬取第{}页'.format(i))
            url = 'https://www.kuaidaili.com/free/inha/{}/'.format(i+1)
            print("爬取网址为：",url)
            IP1, PORT1, TYPE1 = get_content(url)
            process_data(IP1, PORT1, TYPE1)
            time.sleep(2)
        finally:
            print("爬取失败")



def get_content(url):
    headers ={
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36',
    }
    response = requests.get(url,headers=headers)
    if response.status_code == 200:
        print("连接正常")
        soup = BeautifulSoup(response.text,'lxml')
        contents = soup.find_all('td')
        IP = []
        PORT = []
        TYPE = []
        for content in contents:
            content = str(content)
            if re.findall(r'[0-9]*\.[0-9]*\.[0-9]*\.[0-9]*', content):
                IP.append(re.findall(r'[0-9]*\.[0-9]*\.[0-9]*\.[0-9]*', content))
            elif re.findall(r'<td data-title="PORT">', content):
                PORT.append(re.findall(r'\d{4}', content))
            elif re.findall(r'<td data-title="类型">', content):
                TYPE.append(re.findall('[A-Z]{4,5}', content))
        return IP, PORT, TYPE
    else:
        print('链接失败')


def process_data(IP,PORT,TYPE):
    for content in IP:
        ip.append(content[0])
    for content in PORT:
        port.append(content[0])
    for content in TYPE:
        type.append(content[0])
    reg = []
    for i in range(len(ip)):
        dic = {}
        dic[type[i]] = ip[i] + ':'+ port[i]
        reg.append(dic)
    can_use = check_ip(reg)
    print("有用的ip个数为{}".format(len(can_use)))
    save_ip(can_use)



def check_ip(reg):
    url = "https://www.baidu.com"
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36',
    }
    can_use = []
    for i in reg:
        try:
            res = requests.get(url,headers = headers)
            if res.status_code == 200:
                can_use.append(i)

        except Exception as e:

            print("有问题",e)
    return can_use


def save_ip(data):
    with open('ip.txt','w+') as f:
        for i in data:
            f.write(str(i)+'\n')
        f.close()

if __name__ == '__main__':

    page = input("爬取页数：")
    get_url(page)
    print("爬去完成")





























