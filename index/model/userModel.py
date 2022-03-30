from model import Model
from model import MM 
import ext.oos as oos
import ext.tool as tool
 
class UserModel(Model):
    ntable="user"
    def get(self,userid):
        u=self.where("userid="+str(userid)).row()
        u["user_head"]=oos.images_site(u["user_head"])
        return u
    def getListByIds(self,ids):
        w= " userid in("+tool._implode(ids)+") "
        list=self.where(w).all()
        for i in range(len(list)):
           list[i]["user_head"]=oos.images_site(list[i]["user_head"])
        return list
    def Dselect(self,params=[]):
        list=self.all(params)
        mlen=len(list)
        if(mlen==0):
            return []
        for i in range(mlen):
            list[i]["user_head"]=oos.images_site(list[i]["user_head"])
        return list
          