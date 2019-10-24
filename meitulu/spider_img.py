# coding=utf-8

import urllib.request as ur
import re, os
import time
import threading
# 使用 threading 模块创建线程
import queue
import pymysql
# 优先级队列模块
# 线程优先级队列(Queue)




class MySpider(threading.Thread):
    def __init__(self, threadID=None, name=None, q=None):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.q = q

    def run(self):
        print("开启线程：" + self.name)
        self.process_data(self.threadID, self.name, self.q)
        print("退出线程：" + self.name)
    def process_data(self, id, threadName, q):
        while not exitFlag:
            id += 1
            if id >= ThNum + 1:
                data = q.get()
                print("%s processing %s ： %s" % (threadName, data, items[data]) + "\t开启时间：" + str(
                    time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))))
                self.GetImgUrl(data)
    def GetPage(self, url):
        try:
            reponse = ur.urlopen(url)
            page = reponse.read()
            return page
        except Exception as e:
            with open('error.txt', 'a') as f:
                f.write('GetPage :' + url + '--' + str(e) + '\n')

    def GetItem(self, url):
        try:
            page = self.GetPage(url).decode('utf-8')
            re2 = re.findall('.*?<li.*?>.*?<a.*?href="(http|https.*?)".*?>(.*?)</a></li>', page)
            items = {}
            for r in re2:
                if r[1].find('img') > 0:
                    name = re.search('<img.*?alt="(.*?)".*?/>', r[1]).group(1)
                    items[name] = r[0]
                if r[1].find('img') < 0 and r[1] != '首页':
                    items['%s' % r[1]] = r[0]
            return items
        except Exception as e:
            with open('error.txt', 'a') as f:
                f.write('GetItem :' + url + '--' + str(e) + '\n')

    def GetImgUrl(self, data):
        try:
            # print(item,'  ',items['%s'%item])
            url = items['%s' % data]
            base_path = 'E:\\文档\\MySelf\\pic'
            path = os.path.join(base_path, data)
            self.mk(path)
            page = self.GetPage(url).decode('utf-8')
            img_urls = re.findall('<a href="(http|https.*?)".*?<img.*?alt="(.*?)".*?/></a>', page)
            for img_url in img_urls:
                if img_url[1] != '美图录':
                    # print(img_url[0])
                    url = img_url[0].split('.')
                    self.getPic(url=img_url[0], path=path)
        except Exception as e:
            with open('error.txt', 'a') as f:
                f.write('GetImgUrl :' + '--' + str(e) + '\n')

    def getPic(self, url, path):
        try:
            # print(url)
            page = self.GetPage(url).decode('utf-8')
            img_urls = re.findall(r'<img src="(http|https.*?)".*?alt="(.*?)".*?class="content_img"', page)
            # num = re.findall(r'<a.*>(\d.*?)</a>', page)
            imgurl = 'https://mtl.xtpxw.com/images/img/'
            item_id = []
            # print('getPic: ' + path)
            for img_url in img_urls:
                imgnum = img_url[0].split('/')[-2]
                i = 1
                if imgnum not in item_id:
                    while True:
                        url = imgurl + imgnum + '/' + str(i) + '.' + img_url[0].split('.')[-1]
                        content = self.GetPage(url)
                        if content:
                            self.savaPic(path=path, pic_url=url, content=content,
                                    name=img_url[1].replace(' ', '').replace('\\', '').replace('/', '') + '_' + str(i))
                            i += 1
                            item_id.append(imgnum)
                        else:
                            break

        except Exception as e:
            with open('error.txt', 'a') as f:
                f.write('getPic :' + url + '--' + str(e) + '\n')

    def mk(self, name):
        try:
            os.makedirs(name=name)
        except:
            pass

    def savaPic(self, path, pic_url, content, name):
        try:
            pic_path = os.path.join(path, name + '.' + pic_url.split('/')[-1].split('.')[-1])
            with open(pic_path, 'wb') as f:
                f.write(content)
        except Exception as e:
            with open('error.txt', 'a') as f:
                f.write('savaPic :' + pic_url + '--' + str(e) + '\n')


if __name__ == '__main__':
    global exitFlag, items, ThNum, f_ppic
    pic = MySpider()
    url = 'https://www.meitulu.com/'
    items = pic.GetItem(url)
    exitFlag = 0
    threadList = []
    ThNum = 50
    for i in range(1, ThNum + 1):
        threadList.append('Thread-%d' % i)
    nameList = []
    for item in items:
        nameList.append(item)

    workQueue = queue.Queue(len(nameList))
    threads = []
    threadID = 3
    print(len(nameList))
    print(nameList)
    # 填充队列
    for word in nameList:
        workQueue.put(word)
    # 创建新线程
    for tName in threadList:
        thread = MySpider(threadID, tName, workQueue)
        thread.start()
        threads.append(thread)
        threadID += 1
    # 等待队列清空
    while not workQueue.empty():
        pass
    # 通知线程是时候退出

    exitFlag = 1
    # 等待所有线程完成
    for t in threads:
        t.join()
    print("退出主线程")
