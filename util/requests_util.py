import requests
from util import ip_pool as ip
from util import ua_pool as ua
import random
import time

def get(url):
    ip_now= ip.ip_pool[random.randrange(0,len(ip.ip_pool))]
    ua_now=ua.ua_pool[random.randrange(0,len(ua.ua_pool))]    
    proxy_ip = 'http://'+ip_now
    proxies = {'http':proxy_ip}
    headers = {'User-Agent': ua_now} 
    r= requests.get(url,proxies=proxies,headers=headers)
    second=random.randint(1,3)
    time.sleep(0.1*second)
    return r
