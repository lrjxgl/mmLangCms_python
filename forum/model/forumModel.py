from model import Model
from model import MM 
import ext.tool as tool
import ext.oos as oos
class ForumModel(Model):
    ntable="mod_forum"
    
    def Dselect(self):
        list=self.all()
        mlen=len(list)
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
            list[i]=arr

        return list

