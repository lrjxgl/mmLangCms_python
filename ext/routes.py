import os
def getCtrl(mds):
    refile=[]
    for m in mds:

        for d in m["apps"]:
            dir=m["path"]+"/"+d
            files=os.listdir(dir)
            for file in files:
                if os.path.isfile(dir+"/"+file):
                    mfile=dir+"/"+file
                    mfile=mfile.replace("../","")
                    mfile=mfile.replace(".py","")
                    mfile=mfile.replace("/",".")
                    refile.append(mfile) 
    return refile
def getMods():
    mds=[
        {
            "path":"index",
            "apps":["index","admin"]
        },
        {
            "path":"forum",
            "apps":["index","admin"]
        }
    ]    
    files=getCtrl(mds) 
    return files

