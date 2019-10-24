# coding='utf-8'

from bs4 import BeautifulSoup
import urllib.request as ur
from DataBase.Mysql import MySql
import time,os
import threading
# 使用 threading 模块创建线程
import queue
import urllib.response.session


class MySpider(threading.Thread):
    def __init__(self, threadID=None, name=None, q=None,items = None):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.q = q
        self.items = items
    def run(self):
        print("开启线程：" + self.name)
        self.process_data(self.threadID, self.name, self.q,self.items)
        # print(self.q, '  ', self.items[self.q])
        print("退出线程：" + self.name)
    def process_data(self, id, threadName, q,items):

        while exitFlag:
            if q.empty():
                break
            else:
                print('还剩下{}'.format(q.qsize()))
            key = q.get()
            item_url = items[key]
            print('线程：{}\n 正在爬取{}：{}'.format(threadName,key, item_url))
            GetPic(url=item_url,item=key)



def GetPage2(url):
    USER_AGENTS = [
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
        "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
        "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
        "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5"
    ]
    httpProxy = [{'http': '180.101.49.12:80'}, {'http': '120.26.95.202:8089'}, {'http': '127.0.0.1:8080'},
                 {'http': '106.14.190.70:8080'}, {'http': '183.129.207.80:12608'}]
    import random
    try:
        head = ur.Request(url)
        # 添加头文件
        head.add_header('User-Agent',random.choice(USER_AGENTS))
        # 添加代理
        pro = random.choice(httpProxy)
        opener = ur.build_opener(pro)
        ur.install_opener(opener)
        # 打开网页
        req = ur.urlopen(url)
        page = req.read()
    except Exception as e:
        print(str(e))
        print(url)
        with open('e.txt','a') as f:
            f.write(url)
        return False
    else:
        return page




def GetPage(url):
    try:
        req = ur.urlopen(url)
        page = req.read()
    except Exception as e:
        print(str(e))
        print(url)
        with open('e.txt','a') as f:
            f.write('打开网页失败：{}\n'.format(url))
        return False
    else:
        return page

def GetItems(url):
    __item = {}
    __tags=[]
    page = GetPage(url).decode('utf-8')
    # print(page)
    soup = BeautifulSoup(page,'html.parser')
    tags1 = soup.select('.model_source')
    tags2 = soup.select('.link_b')
    tags3 = soup.select('.menu')

    __tags.append(tags1)
    __tags.append(tags2)
    __tags.append(tags3)
    for tags in __tags:
        for tag in tags:
            items = tag.find_all('a')
            for item in items:
                if item.get_text() not in ['首页','斗罗大陆3龙王传说','图集分类','优姿美女','7160美女图片','三眼哮天录','穿越西元3000后','超高清美女图片','斗罗大陆漫画'] and item['href'] not in ['https://www.meitulu.com/','http://www.meitulu.com/']:
                    item_name = item.get_text()
                    item_url = item['href']
                    __item.update({'%s'%item_name:item_url})
    return __item

def GrtGroup(attrs):
    try:
        pic_group = attrs[1].get_text().split('： ')[1]
        group_url = attrs[1].find('a')['href']
        group_id = group_url.split('/')[4]
    except IndexError as e:
        # print(attrs)
        # print(str(e))
        pass
    else:
        group_sql = 'replace into pic_group(group_id,group_name,group_url,up_date) values("%s","%s","%s",now());' % (
        group_id, pic_group, group_url)
        db.Excute(sql=group_sql)
def GetMouble(attrs):
    try:
        pic_mouble = attrs[2].get_text().split('：')[1]
        mouble_url = attrs[2].find('a')['href']
        mouble_id = mouble_url.split('/')[4]
    except:
        # print(attrs)
        pass
    else:
        mouble_sql = 'replace into pic_mouble(mouble_id,mouble_name,mouble_url,up_date) values("%s","%s","%s",now());' % (
        mouble_id, pic_mouble, mouble_url)
        db.Excute(sql=mouble_sql)
def GetTip(attrs):
    try:
        tip_urls = attrs[3].find_all('a')
        tips = {}
        for tip_url in tip_urls:
            url = tip_url['href']
            name = tip_url.get_text()
            tips.update({'%s' % name: url})
    except:
        # print(attrs)
        pass
    else:
        for tip in tips.keys():
            tip_sql = 'replace into pic_tip(tip_id,tip_url,up_date) values("%s","%s",now());' % (tip, tips[tip])
            db.Excute(sql=tip_sql)
def GetImg(p_url,p_title,item):
    base_url = 'https://www.meitulu.com'
    page = GetPage(p_url)
    if page:
        page = page.decode('utf-8')
        soup = BeautifulSoup(page, 'html.parser')
        imgs = soup.select('.content_img')
        for img in imgs:
            img_url = img['src']
            img_name = img['alt']
            pic_name = img_url.split('/')[-1]

            path = os.path.join(r'E:\文档\MySelf\img',item.strip(),p_title.strip().replace('/','').replace(' ',''))
            MkDir(path)
            name = os.path.join(path,pic_name)
            SavaPic(img_url, name)
        try:
            pages = soup.select('#pages')[-1].find_all('a')[-1]
            next_url = base_url+pages['href']
            # print(next_url)
            if next_url != p_url:
                GetImg(p_title=p_title,p_url=next_url,item=item)
        except:
            with open('error.txt','a') as f:
                f.write('获取页码失败：{}\n'.format(url))


def MkDir(path):
    try:
        os.makedirs(path)
    except:
        pass

def SavaPic(pic_url,pic_name):
    page = GetPage(pic_url)
    if page:
        pic_name = pic_name
        with open(pic_name,'wb') as f:
            f.write(page)
def GetPic(item,url):
    page = GetPage(url)
    if page:
        page = page.decode('utf-8')
        soup = BeautifulSoup(page, 'html.parser')
        tags = soup.select('.img')
        for tag in tags:
            lis = tag.find_all('li')
            for li in lis:
                # print(li)
                # 图片链接
                p_url = li.find('a')['href']
                # 获取属性
                attrs = li.find_all('p')
                # 线程加锁
                lock.acquire()
                GetMouble(attrs)
                GetTip(attrs)
                GrtGroup(attrs)
                # 线程解锁
                lock.release()
                # 图片数
                pic_num = attrs[0].get_text().split('： ')[1]
                # 照片名
                # p_title = attrs[4].get_text()
                p_title = li.find('p', class_='p_title').find('a').get_text()
                # print(p_title,'  ',p_url,'   ',pic_num)
                GetImg(p_url,p_title,item)
        try:
            print('当前页url地址{}'.format(url))
            pages = soup.select('#pages')[-1].find_all('a')[-1]
            next_url = pages['href']
            print('下一页url地址{}'.format(next_url))
            if next_url != url:
                GetPic(item,next_url)
        except:
            with open('error.txt','a') as f:
                f.write('获取页码失败：{}\n'.format(url))
if __name__ == '__main__' :


    global exitFlag,lock

    exitFlag = True
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    url = 'https://www.meitulu.com/'
    items = GetItems(url)
    db = MySql()
    lock = threading.Lock()

    keys = items.keys()

    ThNum = 50
    # 创建队列
    WorkQueue = queue.Queue(len(keys))
    # 填充队列
    for key in keys:
        WorkQueue.put(key)

    # 创建线程名
    Threads = []
    for num in range(ThNum):
        Threads.append('Thread Name - %d'%num)

    # 线程集合
    Thread_s= []
    # 创建线程
    i = 0
    print(len(keys))
    for Thread in Threads:
        # print()
        thread = MySpider(name=Thread,q=WorkQueue,items=items)
        thread.start()
        Thread_s.append(thread)




    # 等待队列清空
    while not WorkQueue.empty():
        pass
    exitFlag = False
    # 等待所有线程完成
    for t in Thread_s:
        t.join()

    db.Close()
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))