from model import Model
class MaxidModel(Model):
    ntable="maxid"
    def get(self):
        return self.insert("t=1")

