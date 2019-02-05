import requests
from ip_pool import ip_pool
from ua_pool import ua_pool
import random
import time

def get(url):
    ip = ip_pool[random.randrange(0,len(ip_pool))]
    ua=ua_pool[random.randrange(0,len(ua_pool))]    
    proxy_ip = 'http://'+ip
    proxies = {'http':proxy_ip}
    headers = {'User-Agent': ua} 
    r= requests.get(url,proxies=proxies,headers=headers)
    second=random.randint(1,5)
    time.sleep(0.1*second)
    return r
