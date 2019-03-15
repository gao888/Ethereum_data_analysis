import os
import pandas as pd
import datetime

def getEveryDay(begin_date,end_date):
    begin_date = datetime.datetime.strptime(begin_date, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(end_date,"%Y-%m-%d")
    periods=(datetime_end-datetime_begin).days
    dates=pd.date_range(date_start, periods=periods+1, freq='D')
    date_list=dates.to_native_types().tolist()
    return date_list

def fill(num):
    if pd.isna(num)==True:
        return 0
    else:
        return num

def tx_to_change(txdata):
    subdata_from=txdata.loc[:,['from','amount','date']]
    subdata_from['amount']=-subdata_from['amount']
    subdata_from=subdata_from.rename(index=str, columns={'from': 'account'})
    subdata_to=txdata.loc[:,['to','amount','date']]
    subdata_to=subdata_to.rename(index=str, columns={'to': 'account'})
    data_total=subdata_from.append(subdata_to)
    data_total=data_total.groupby(['account','date'])['amount'].agg(sum)
    data_total=pd.DataFrame(data_total)
    return data_total

def get_tag(change_data):
    result=change_data.groupby(['account'])['amount'].apply(max)
    return result



def balance_visual(tokenpath,tagpath,tokennum=1):
    T=pd.read_csv(tagpath)  
    taglist=T.loc[:,'tag'].tolist()

    R1=pd.read_csv(tokenpath)
    timelist=R1.loc[:,'date'].tolist()
    end=max(timelist)
    begin=min(timelist)

    taglist=list(set(taglist))
    dict2={'account':[],'date':[]}
    # for tag in taglist:
    #     for time in getEveryDay(str(begin),str(end)):
    #         dict2['date'].append(time[0:4]+'-'+time[5:7]+'-'+time[8:10])
    #         dict2['account'].append(tag)
    # Final=pd.DataFrame(dict2)

    Merge=pd.merge(R1, T, how='left', on='account')
    Merge=Merge.groupby(['tag', 'date'])['daychange'].sum().reset_index()
    Merge['account']=Merge['tag']

    Merge2=pd.merge(Final,Merge, how='left', on=['account','date'])
    Merge2=Merge2.sort_values(by='date')
    Merge2['daychange']=Merge2['daychange'].apply(fill)
    Merge2['dailybalance'] = Merge2.groupby(['account'])['daychange'].apply(lambda x: x.cumsum())
    Merge2.loc[:,'dailybalance']=Merge2.loc[:,'dailybalance'].map(int)       
    Merge2['percent']=Merge2['dailybalance']/tokennum
    outpath=tokenpath[:-4]+'_visual.csv'
    Merge2.to_csv(outpath,index=False,sep=',')