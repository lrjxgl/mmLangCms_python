from typing import Optional
from fastapi import APIRouter,Form 
from model import MM 
from ext.userAccess import checkAccess,goLogin 
router = APIRouter(prefix="/user")
@router.get("/index")
def index(
    token:Optional[str]=""
):
    ssuserid=checkAccess(token)
    if ssuserid==0:
        return goLogin()
    user=MM("index","user").get(ssuserid)
    return {
        "error":0,
        "message":"success",
        "user":user
    }
@router.get("/set")
def index(
    token:Optional[str]=""
):
    ssuserid=checkAccess(token)
    if ssuserid==0:
        return goLogin()
    user=MM("index","user").get(ssuserid)
    return {
        "error":0,
        "message":"success",
        "user":user
    } 
@router.get("/info")
def info(
    token:Optional[str]=""
):
    ssuserid=checkAccess(token)
    if ssuserid==0:
        return goLogin()
    user=MM("index","user").get(ssuserid)
    return {
        "error":0,
        "message":"success",
        "user":user
    }         