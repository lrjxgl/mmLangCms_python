from typing import Optional
from fastapi import APIRouter,Form
from model import DB,MM

router = APIRouter(prefix="")
@router.get("/")
def index():
    return {
        "error":0,
        "message":"首页"
    }
@router.get("/test")
def test():
    
    id= MM("index","love").insert("tablename='test',objectid=1, userid=1 ")  
    MM("index","love").commit()
    fid= MM("index","fav").insert("tablename='test',objectid=1 , userid=1 ")  
    MM("index","fav").commit()
    return {
        id:id,
        fid:fid
    }