from typing import Optional
from fastapi import APIRouter
from model import MM
router = APIRouter(prefix="/forum_group")

@router.get("/index")
async def index():
    list=MM("forum","forumGroup").all()
    
    rscount=MM("forum","forumGroup").fields("count(*)").one()
    return {"list":list,"rscount":rscount}
@router.get("/show")
async def show(id: Optional[int] = None):
    msg  ="forum show"+str(id)
    return {"message":msg,"id":id}