import os
import pickle
import pandas as pd

path=os.getcwd()

def savelist(file,name):
    global path
    with open(path+'\\save\\'+name+'.pickle', 'wb') as file_path:
        pickle.dump(file,file_path)
    print('finish save')

def loadlist(name):
    global path
    with open(path+'\\save\\'+name+'.pickle', 'rb') as file:
        hashlist =pickle.load(file)
    return hashlist

def month2num(ethtime):
    month={'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06',
    'Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}
    mon=month[ethtime[0:3]]
    year=ethtime[7:]
    day=ethtime[4:6]
    date_row=(year,mon,day)
    joiner='-'
    date=joiner.join(date_row)
    return date

def adjust_txdata(txdata,token_address):
    txdata['date']=txdata['date'].map(month2num)
    txdata2=txdata[txdata.token==token_address]
    return txdata2

def savecsv(data,name):
    global path
    data.to_csv(path+'\\save\\'+name+'.csv',sep=',',index=False)
    print('finish save')


