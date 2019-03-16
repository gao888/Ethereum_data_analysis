import os
import pickle
import pandas as pd

path=os.getcwd()

# def savelist(file,name):
#     global path
#     with open(path+'\\save\\'+name+'.pickle', 'wb') as file_path:
#         pickle.dump(file,file_path)
#     print('finish save')

# def loadlist(name):
#     global path
#     with open(path+'\\save\\'+name+'.pickle', 'rb') as file:
#         hashlist =pickle.load(file)
#     return hashlist

def savecsv(data,name):
    global path
    file_path=path+'\\save\\'+name+'.csv'
    data.to_csv(file_path,sep=',',index=False)
    print('save to {}'.format(file_path))

def loadcsv(name):
    global path
    file_path=path+'\\save\\'+name+'.csv'
    print('load {}'.format(file_path))
    data=pd.read_csv(file_path)
    return data


