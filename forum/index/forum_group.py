from typing import Optional
from fastapi import APIRouter
from model import MM
import ext.oos as oos
router = APIRouter(prefix="/forum_group")

@router.get("/index")
async def index():
    list=MM("forum","forumGroup").where("status=1").order("orderindex ASC").limit(123).all()
    for i in range(len(list)):
        list[i]["imgurl"]=oos.images_site(list[i]["imgurl"])
    rscount=MM("forum","forumGroup").fields("count(*)").one()
    return {"list":list,"rscount":rscount}
@router.get("/show")
async def show(id: Optional[int] = None):
    msg  ="forum show"+str(id)
    return {"message":msg,"id":id}