def getListByKey(list,key,val):
    for item in list:
        if(item[key]==val):
            return item    
    return []
 
list=[{
    "id":12,
    "title":"123"
},{
    "id":23,
    "title":"234"
}]    
a=getListByKey(list,"id",12)
print(a)