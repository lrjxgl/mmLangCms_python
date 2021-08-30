from fastapi import APIRouter
from typing import Optional
from model import MM
import ext.oos as oos
from ext.userAccess import checkAccess
router = APIRouter(prefix="/forum_home")
@router.get("/index")
async def index(
    token:Optional[str]="",
    userid:Optional[int]=0,
    per_page:Optional[int]=0
):
    ssuserid=checkAccess(token)
    user=MM("index","user").get(userid)
    start=per_page
    limit=12
    w=" status in(0,1,2) AND userid=%d " %(userid)
    
    list=MM("forum","forum").where(w).limit(start,limit).Dselect()
    rscount=MM("forum","forum").where(w).count()
    per_page=start+limit
    per_page=0 if per_page>rscount else per_page
    return {
        "error":0,
        "message":"success",
        "list":list,
        "per_page":per_page,
        "rscount":rscount,
        "user":user
  
    } 