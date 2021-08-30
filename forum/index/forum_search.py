from typing import Optional
from fastapi import APIRouter
from model import MM
import ext.oos as oos
import ext.tool as tool
router = APIRouter(prefix="/forum_search")
 
@router.get("/index")
async def index(
    per_page:Optional[int]=0,
    keyword:Optional[str]=""
):
    start=per_page
    limit=12
    if(keyword==""):
        recList=MM("forum","forum").where("status=1 AND isrecommend=1").limit(12).Dselect()
        return {
            "error":0,
            "message":"success",
            "list":recList 
        }
    w=" title like %s AND status=1 "    
    list=MM("forum","forum").where(w).limit(start,limit).Dselect('%'+keyword+'%')
    rscount=MM("forum","forumGroup").where(w).count('%'+keyword+'%')
   
    return {
        "error":0,
        "message":"success",
        "list":list,
        "rscount":rscount,
        "per_page":per_page
        
    }
 