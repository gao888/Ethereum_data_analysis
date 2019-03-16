import os
import pickle

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
    data.to_csv(path+'\\save\\'+name+'.csv',sep=',',index=False)
    print('finish save')


