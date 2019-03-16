import requests
import re
# from bs4 import BeautifulSoup
import pandas as pd
from util import requests_util as requests_u
from util import constant

import requests
import re
import pandas as pd
from util import requests_util as requests_u
from util import constant

def get_pages(token):
    url='https://etherscan.io/token/generic-tokentxns2?contractAddress='+token+'&mode=&p=1'
    r_t= requests.get(url)
    text_t=r_t.text
    page_raw = re.findall(r'<span Class="page-link text-nowrap">(.*?)</span>',text_t, flags=0)[0]
    pages= re.findall(r'<strong class="font-weight-medium">(.*?)</strong>',page_raw)[1]
    pages=int(pages)
    return pages

def get_page_single(token,page):
    url='https://etherscan.io/token/generic-tokentxns2?contractAddress='+token+'&mode=&p='+str(page)
    get_result=requests_u.get(url)
    text_t=get_result.text
    table=re.search(r'<table class="table table-md-text-normal table-hover mb-4">([\s\S]*?)</table>',text_t, flags=0).group()
    lines=re.findall(r'<tr>(.*?)</tr>',table)
    return lines

def get_page_all(token,pages):
    pages_plus=pages+3
    total_lines=[]
    for page in range(1,pages_plus+1):
        lines=get_page_single(token,page)
        print('{0}/{1} {2} records'.format(page,pages_plus,len(lines)))
        total_lines+=lines
    return total_lines
    
def lines_table(total_lines):
    line_table=[]
    for single_line in total_lines:
        col=re.findall(r'<td>(.*?)</td>',single_line)
        re_find_a = re.compile(r'<a.*?>(.*?)</a>')
        txhash=re_find_a.search(col[0]).groups()[0]
        time_list=re.search("title=\'(.*?)\'",col[1], flags=0).groups()[0].split(' ')
        date=time_list[0]
        time=time_list[1]
        from_ad=re_find_a.search(col[2]).groups()[0]
        to_ad=re_find_a.search(col[4]).groups()[0]
        amount=col[5]
        single_proceed=[date,time,from_ad,to_ad,amount,txhash]
        line_table.append(single_proceed)
    table=pd.DataFrame(line_table,columns=['date','time','from_address','to_address','amount','hash'])
    table['date']=table['date'].apply(ethercan_time)    
    return table

def ethercan_time(time):
    date_list=time.split('-')
    month=constant.month[date_list[0]]
    date_proceed=date_list[2]+'-'+month+'-'+date_list[1]
    return date_proceed
    
def main(token):
    pages=get_pages(token)
    total_lines=get_page_all(token,pages)
    table=lines_table(total_lines)
    return table 

# def get_hash_page(token,page): 
#     url='https://etherscan.io/token/generic-tokentxns2?contractAddress='+token+'&mode=&p='+str(page)
#     r= requests_u.get(url)
#     text=r.text
#     soup = BeautifulSoup(text,features="lxml")
#     table = soup.find('table')
#     rows = table.find_all('tr')
#     txhashs=[]
#     if text.find('There are no matching entries')==-1:
#         for row in rows[1:]:
#             columns = row.find_all('td')
#             txhash=re.search(r'>[a-zA-Z0-9]+</a>',str(columns[0]), flags=0).group()[1:-4]
#             txhashs.append(txhash)
#         return txhashs
#     else:
#         return('finish all hash')

# def get_hash_all(token):
#     pages_raw=get_pages(token)
#     pages=int(pages_raw)+3
#     print(pages)
#     total=[]
#     for page in range(pages)[1:]:
#         print(str(page)+'/'+str(pages))
#         a=get_hash_page(token,page)
#         if type(a) is str:
#             print(a)
#         else:
#             total=total+a
#     total=list(set(total))
#     return total

# def find_time(soup):
#     time_span=soup.find('span',attrs={'id':'clock'})
#     time_raw=time_span.parent.text
#     begin=time_raw.find('(')
#     end=time_raw.find('+UTC')
#     time=time_raw[begin+1:end]
#     time_list=time.split()
#     if time_list[2]=='PM':
#         hour=int(time_list[1][:2])+12
#         time_list[1]=str(hour)+time_list[1][2:]
#     return time_list[0:2]

# def find_trans(soup):       
#     trans_raws=soup.find_all('span',attrs={'class':'row-count'})
#     headers=['from','to','amount','token']
#     trans_table=[]
#     re_address = re.compile(r'>[a-zA-Z0-9]{42}</a>')
#     for trans_raw in trans_raws:
#         trans_raw=str(trans_raw)
#         fr_loc=trans_raw.find('From')
#         to_loc=trans_raw.find('To')
#         am_loc=trans_raw.find('for')
#         end_loc=trans_raw.find('(')
#         from_r=trans_raw[fr_loc+4:to_loc]
#         to_r=trans_raw[to_loc+2:am_loc]
#         amount_r=trans_raw[am_loc+5:end_loc]
#         From=re_address.search(from_r).group()[1:-4]
#         to=re_address.search(to_r).group()[1:-4]
#         amount=re.match(r'[0-9,.]*',amount_r, flags=0).group().replace(',','')
#         token=re.search(r'token/[a-zA-Z0-9]{42}',trans_raw, flags=0).group()[6:]
#         result=[From,to,amount,token]
#         trans_table.append(result)
#     df = pd.DataFrame(trans_table, columns=headers)    
#     return df

# def get_tx(txhash):
#     url_tx='https://etherscan.io/tx/'+txhash
#     tx= requests_u.get(url_tx)
#     text=tx.text
#     soup = BeautifulSoup(text,features="lxml")
#     trans=find_trans(soup)
#     time=find_time(soup)
#     trans.loc[:,'date']=time[0]
#     trans.loc[:,'hms']=time[1]
#     return trans

