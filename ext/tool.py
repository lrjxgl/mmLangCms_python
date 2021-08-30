#!/usr/bin/python3
import hashlib
def _implode(list):
    ss=""
    for i in range(len(list)):
        if i>0 :
            ss+=","
        ss+="'"+str(list[i])+"'"
    return ss
def getListByKey(list,key,val):

    for item in list:
        if(item[key]==val):
            return item    
    return []

def umd5(ss):
    ss=hashlib.md5(ss.encode(encoding='utf-8')).hexdigest()
    ss=hashlib.md5(ss.encode(encoding='utf-8')).hexdigest()
    return ss
def sql(ss):
    return ss    