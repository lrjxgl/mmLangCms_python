from model import Model,MM
class ForumGroupModel(Model):
    ntable="mod_forum_group"
    
    def Dselect(self):
        return self.all()

    def groupChild(self):
        glist=self.where("status=1").order("orderindex ASC").limit(1000).all()
        catList=MM("forum","forumCategory").where("status=1").order("orderindex ASC").limit(100000).all() 
        mlen=len(glist)
        for i in range(mlen):
            g=glist[i]
            child=[]
           
            for cat in catList:
               if(cat["gid"]==g["gid"]):
                    child.append(cat)
            
            g["child"]=child
            glist[i]=g
        return glist   
            



            

