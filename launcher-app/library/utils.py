import os

def getListDirFilePath():
        for (root,dirs,files) in os.walk('C:\workspace\learning\lmn_tools', topdown=True):
            pathAddress = root
        

a = getListDirFilePath()

print(a)