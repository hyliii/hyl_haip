import requests
# url='http://www.httpbin.org/ip'
url='https://www.xicidaili.com/nn/1'
target_ip=requests.get(url=url ,headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}).text
print(target_ip)
l=[]
l.append({'1':'1'})
print(set(l))