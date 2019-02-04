import requests
import re
from bs4 import BeautifulSoup
import time
import random
from ip_pool import ip_pool
import pandas as pd

def get_pages(token):
    url='https://etherscan.io/token/generic-tokentxns2?contractAddress='+token+'&mode=&p=1'
    r_t= requests.get(url)
    text_t=r_t.text
    page_raw = re.search(r'Page <b>1</b> of <b>\d+</b>',text_t, flags=0).group()
    page_half=page_raw[page_raw.find('of'):]
    pages=re.search(r'<b>\d+</b>',page_half, flags=0).group()[3:][:-4]
    return pages

def get_hash_page(token,page): 
    url='https://etherscan.io/token/generic-tokentxns2?contractAddress='+token+'&mode=&p='+str(page)
    proxies=ip_proxy()
    r= requests.get(url,proxies=proxies)
    text=r.text
    soup = BeautifulSoup(text,features="lxml")
    table = soup.find('table')
    rows = table.find_all('tr')
    txhashs=[]
    if text.find('There are no matching entries')==-1:
        for row in rows[1:]:
            columns = row.find_all('td')
            txhash=re.search(r'>[a-zA-Z0-9]+</a>',str(columns[0]), flags=0).group()[1:-4]
            txhashs.append(txhash)
        return txhashs
    else:
        return('finish all hash')

def ip_proxy():
    ip = ip_pool[random.randrange(0,len(ip_pool))]
    proxy_ip = 'http://'+ip
    proxies = {'http':proxy_ip}
    return proxies

def get_hash_all(token):
    pages_raw=get_pages(token)
    pages=int(pages_raw)+2
    print(pages)
    total=[]
    for page in range(pages):
        print(str(page)+'/'+str(pages))
        a=get_hash_page(token,page)
        second=random.randint(1,5)
        time.sleep(0.1*second)
        if type(a) is str:
            print(a)
        else:
            total=total+a
    return total

def find_time(soup):
    time_span=soup.find('span',attrs={'id':'clock'})
    time_raw=time_span.parent.text
    begin=time_raw.find('(')
    end=time_raw.find('+UTC')
    time=time_raw[begin+1:end]
    time_list=time.split()
    if time_list[2]=='PM':
        hour=int(time_list[1][:2])+12
        time_list[1]=str(hour)+time_list[1][2:]
    return time_list[0:2]

def find_trans(soup):       
    trans_raws=soup.find_all('span',attrs={'class':'row-count'})
    headers=['From','to','amount']
    trans_table=[]
    re_address = re.compile(r'>[a-zA-Z0-9]{42}</a>')
    for trans_raw in trans_raws:
        trans_raw=str(trans_raw)
        fr_loc=trans_raw.find('From')
        to_loc=trans_raw.find('To')
        am_loc=trans_raw.find('for')
        end_loc=trans_raw.find('(')
        from_r=trans_raw[fr_loc+4:to_loc]
        to_r=trans_raw[to_loc+2:am_loc]
        From=re_address.search(from_r).group()[1:-4]
        to=re_address.search(to_r).group()[1:-4]
        amount=trans_raw[am_loc+5:end_loc].replace(' ','')
        result=[From,to,amount]
        trans_table.append(result)
    df = pd.DataFrame(trans_table, columns=headers)    
    return df

def get_tx(txhash):
    url_tx='https://etherscan.io/tx/'+txhash
    tx= requests.get(url_tx)
    text=tx.text
    soup = BeautifulSoup(text,features="lxml")
    trans=find_trans(soup)
    time=find_time(soup)
    trans.loc[:,'date']=time[0]
    trans.loc[:,'hms']=time[1]
    return trans