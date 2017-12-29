import requests
import threading # 多线程
import re
from lxml import  etree
from  bs4 import  BeautifulSoup



def get_html(url):

    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/604.3.5 (KHTML, like Gecko) Version/11.0.1 Safari/604.3.5'}
    request = requests.get(url=url,headers=header)
    response = request.text
    return  response


def get_img_html(html):
    soup = BeautifulSoup(html,'lxml')
    all_a = soup.find_all('a',class_='pull-rs')
    for i in all_a:
        url = ' http://image.baidu.com/'+i['href']
        img_html = get_html(url)
        get_img(img_html)



def get_img(html):
    url_list = re.findall('"objURL":"(.*?)"',html,re.S) #正则获取imgeurl
    print(url_list)
    start_save_img(url_list)


x = 1
def save_img(img_url):
    global x

    # img_url = img_url.split('=')[-1][1:-2].replace('jp','jpg')
    print('正在下载' + img_url)
    img_content = requests.get(img_url).content
    with open('meitu/%s.jpg'% x,'wb') as f:
        x+= 1
        f.write(img_content)


def start_save_img(url_list):
    for i in url_list:
        th = threading.Thread(target=save_img,args=(i,))
        th.start()



def main():
    search_key_word = '美女'
    start_url = 'http://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&sf=1&fmq=&pv=&ic=0&nc=1&z=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&fm=result&pos=history&word='+search_key_word
    start_html = get_html(start_url) #获取网页源码
    get_img_html(start_html)



if __name__ == '__main__': #入口
    main()

