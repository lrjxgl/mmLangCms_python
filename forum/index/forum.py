from typing import Optional
from fastapi import APIRouter
from model import DB
from model import MM
import ext.oos as oos
router = APIRouter(prefix="/forum")
db=DB()
@router.get("/index")
async def index():
    mad=MM("index","ad")
    flashList=mad.limit(4).listByNo("uniapp-forum-index")
    navList=mad.limit(12).listByNo("uniapp-forum-nav")
    adList=mad.limit(3).listByNo("uniapp-forum-ad")
    recList=MM("forum","forum").limit(6).Dselect()
     
    return {
        "error":0,
        "message": "success",       
        "flashList":flashList,
        "navList":navList,        
        "adList":adList,
        "recList":recList
    }
@router.get("/show")
async def show(id: Optional[int] = None):
    if(id==None):
        return {
            "message":"error",
            "error":1
        }
    data=MM("forum","forum").where("id="+str(id)).row()
    data["imgurl"]=oos.images_site(data["imgurl"])
    data["videourl"]=oos.images_site(data["videourl"])
    data["imgsList"]=oos.parseTrueImgList(data["imgsdata"])
    author=MM("index","user").get(data["userid"])
     
    return {"data":data,"author":author}

@router.get("/addclick")
async def addClick(id: Optional[int] = None):
    return {
            "message":"success",
            "error":0
        }
