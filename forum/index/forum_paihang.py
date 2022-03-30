from typing import Optional
from fastapi import APIRouter
from model import MM
import ext.oos as oos
router = APIRouter(prefix="/forum_paihang")
@router.get("/index")
def index():
    fsList=MM("index","user").where("status=1").order("followed_num DESC").limit(24).Dselect()
    wzList=MM("forum","forum").where("status=1").order("love_num DESC").limit(24).Dselect()
    return {
        "error":0,
        "message":"success",
        "data":{
            "wzList":wzList,
            "fsList":fsList
        }
        
    }
