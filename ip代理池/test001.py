from random import random
import requests
from lxml import etree
check_url='http://www.httpbin.org/ip'
host_ip=requests.get(check_url).text
class Pool(object):
    def __init__(self):
        self.db=DB(r'D:\hyl\ip代理池\ips.txt')
        self.yuzhi=50
        self.pagenum=1
    def check_ip(self,ip):
        try:
            target_ip=requests.get(check_url,proxies=ip).text
            if target_ip!=host_ip:
                return True
        except:
            return False
    def crawl_ip(self,url):
        while True:
            html=etree.HTML(requests.get(url+str(self.pagenum),headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}).text)
            for tr in html.xpath('//tr')[1:]:
                tds = tr.xpath('./td/text()')
                ip = {tds[5].lower(): tds[5].lower()+'://'+tds[0] + ':' + tds[1]}
                print(ip)
                if self.check_ip(ip):
                    print('**********'+str(ip))
                    self.db.save(str(ip))
            self.pagenum+=1
    def get_ip(self):
        ip=self.db.get_ip()
        self.db.delete_ip(ip)
        self.check_ip_by_yuzhi()
        return ip
    def check_ip_by_time(self):
        ips=self.db.get_all()
        for ip in ips:
            if not self.check_ip(ip):
                self.db.delete_ip(ip)
        self.check_ip_by_yuzhi()
    def check_ip_by_yuzhi(self):
        count=self.db.get_count()
        while count<self.yuzhi:
            url = 'https://www.xicidaili.com/nn/' + str(self.pagenum)
            self.crawl_ip(url)
class DB(object):
    def __init__(self,filename):
        self.filename=filename
        self.ll=[]
# 1. 存ip
    def save(self,ip):
        with open(self.filename,'r')as r:
            s=r.read()
        if s!='':
            self.ll = [str(j) for j in eval(s)]
        self.ll.append(ip)
        print('++++++++++'+str(ip))
        with open(self.filename,'w')as w:
            self.l=[eval(i) for i in list(set(self.ll))]
            w.write(str(self.l))
# 2. 取ip
    def get_ip(self):
        with open(self.filename,'r')as r:
            ips=eval(r.read())
            ip=random(ips)
            return ip
# 3. 删除ip
    def delete_ip(self,target_ip):
        with open(self.filename,'r')as r:
            ips=eval(r.read())
            for ip in ips:
                if target_ip==ip:
                    ips.remove(ip)
        with open(self.filename,'w')as w:
               w.write(str(ips))
# 4. 获取所有ip地址数量
    def get_count(self):
        with open(self.filename, 'r')as r:
            return len(eval(r.read()))
# 5. 获取所有ip地址
    def get_all(self):
        with open(self.filename, 'r')as r:
            return eval(r.read())
if __name__=='__main__':
    pool1=Pool()
    pool1.crawl_ip(url='https://www.xicidaili.com/nn/')

