 
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

