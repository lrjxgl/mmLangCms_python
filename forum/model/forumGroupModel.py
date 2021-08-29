from model import Model
 
class ForumGroupModel(Model):
    ntable="mod_forum_group"
    
    def Dselect(self):
        return self.all()

