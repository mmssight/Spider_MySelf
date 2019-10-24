# coding=utf-8
import urllib.request as ur
import random
import re
import time, pickle,pymysql
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


def getPage(url):
    time.sleep(1)
    try:
        req = ur.Request(url)
        req.add_header('User-Agent', random.choice(USER_AGENTS))
        a = random.choice(httpProxy)
        proxy = ur.ProxyHandler(a)
        opener = ur.build_opener(proxy)
        ur.install_opener(opener)
        response = ur.urlopen(req)
        # print(response.getcode())
        if response.getcode() == 200:
            html = response.read().decode('utf-8')
            pick_file = open('ip.pkl', 'wb')
            pickle.dump(httpProxy, pick_file)
            pick_file.close()
            return True, html
        else:
            print('Falied')
            return False, 1
    except Exception as e:
        print(e)
        httpProxy.remove(a)
        isTrue, html = getPage(url)
        return isTrue, html


if __name__ == '__main__':
    conn = pymysql.connect(host='127.0.0.1', user='root', password='root', database='myself', charset='utf8')
    flg = True
    page_code = 1
    num = 0
    while flg:
        # url = 'https://www.kuaidaili.com/free/inha/%s/' % str(page_code)
        # url='https://www.xicidaili.com/nn/'+str(page_code)
        url='http://www.xsdaili.com/dayProxy/ip/%s.html'%str(page_code)
        print(url)
        isTrue, html = getPage(url)
        if isTrue:
            _ip = re.findall(r'<td.*?>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', html)
            _port = re.findall(r'<td.*?>(\d{1,8})</td>', html)
            _type = re.findall(r'<td.*?>(HTTP.*?|http.*?)</td>', html)
            with open('ipdaili.csv', 'a') as f:
                for i in range(len(_ip)):
                    # print(_ip[i],_port[i],_type[i])
                    sql = 'insert into IpDaiLi(ip,port,type) values ("%s","%s","%s");'%(_ip[i], _port[i], _type[i])
                    try:
                        conn.cursor().execute(sql)
                        conn.commit()
                    except Exception as e:
                        print(str(e))
                        conn.rollback()
                    f.write('%s,%s,%s\n' % (_ip[i], _port[i], _type[i]))
                    ip = {}
                    ip[_type[i]] = '%s:%s' % (_ip[i], _port[i])
                    httpProxy.append(ip)


        else:
            num += 1

        if num >= 10:
            flg = False
        page_code += 1
    conn.cursor().close()
    conn.close()