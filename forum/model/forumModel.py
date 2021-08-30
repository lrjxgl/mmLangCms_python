from model import Model
from model import MM 
import ext.tool as tool
import ext.oos as oos
import datetime
class ForumModel(Model):
    ntable="mod_forum"
    
    def Dselect(self,params=()):
        list=self.all(params)
        mlen=len(list)
        if(mlen==0):
            return []
        uids=[]
        for item in list:
            uids.append(item["userid"])
        userModel=MM("index","user")
         
        us=userModel.getListByIds(uids)

        for i in range(mlen):
            arr=list[i]
            arr["user"]=mlen
            arr["user"]=tool.getListByKey(us,"userid",arr["userid"])
            arr["imgList"]=oos.parseImgList(arr["imgsdata"])
            arr["timeago"]=arr["createtime"].strftime('%Y-%m-%d %H:%M:%S')
            list[i]=arr

        return list

