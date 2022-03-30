from typing import Optional
from fastapi import APIRouter
from model import MM
import ext.oos as oos
from ext.userAccess import checkAccess
router = APIRouter(prefix="/forum_feeds")
@router.get("/index")
async def index(
    token:Optional[str]="",
    per_page:Optional[int]=0
):
    ssuserid=checkAccess(token)
    if(ssuserid==0):
        return goLogin()
    start=per_page
    limit=12
    w=" status=1 AND userid=%d " %(ssuserid)
    
    list=MM("forum","forum").where(w).limit(start,limit).Dselect()
    rscount=MM("forum","forum").where(w).count()
    per_page=start+limit
    per_page=0 if per_page>rscount else per_page
    return {
        "error":0,
        "message":"success",
        "data":{
            "list":list,
            "per_page":per_page,
            "rscount":rscount,
        }
        
  
    } 