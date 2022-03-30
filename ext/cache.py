from model import MM
import time
def cacheSet(k,v,expire):
    row=MM("index","dbcache").where("k=%s").row(k)
    expire=int(time.time())+expire
    if(row!=None):
        MM("index","dbcache").where("k=%s").update("v=%s,expire=%s",[str(v),expire,k])
    else:
        MM("index","dbcache").insert("k=%s,v=%s,expire=%s",[k,str(v),expire])    
    commit()
    return True
def cacheGet(k):
    row=MM("index","dbcache").where("k=%s").row(k)
    if row==None:
        return None
    return row["v"]
def cacheDel(k):
    MM("index","dbcache").where("k=%s").delete(k)
    commit()
def commit():
    MM("index","dbcache").commit()    