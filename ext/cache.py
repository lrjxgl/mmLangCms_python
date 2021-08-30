from model import MM
def cacheSet(k,v,expire):
    row=MM("index","dbcache").where("k=%s").row(k)
    if(row!=None):
        MM("index","dbcache").where("k=%s").update("v=%s,expire=%s",[str(v),expire,k])
    else:
        MM("index","dbcache").insert("k=%s,v=%s,expire=%s",[k,str(v),expire])    
    return True
def cacheGet(k):
    row=MM("index","dbcache").where("k=%s").row(k)
    if row==None:
        return None
    return row["v"]
def commit():
    MM("index","dbcache").commit()    