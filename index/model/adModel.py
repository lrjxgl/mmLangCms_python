from model import Model
from model import MM 
from ext.oos import images_site
class AdModel(Model):
    ntable="ad"
    
    def Dselect(self):
        return self.all()
    def listByNo(self,tagno):
       tag= MM("index","adTags").where("tagno='"+tagno+"' AND status=1 ").row()
       if(tag is None):
           return []
       
       tid=tag["tag_id"]
      
       list=self.where("tag_id_2nd="+str(tid)+" AND status=1 ").all()
        
       for i in range(len(list)):
           list[i]["imgurl"]=images_site(list[i]["imgurl"])
       return list




