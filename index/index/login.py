from typing import Optional
from fastapi import APIRouter,Form
from model import DB,MM
import ext.tool as tool
from ext.userAccess import setToken
router = APIRouter(prefix="/login")
@router.get("/index")
async def index():
    return {
        "error":0,
        "message":"success"
    }
@router.post("/save") 
async def save(
    telephone: str=Form(...),
    password: str=Form(...)
):
    w="telephone=%s " 
    u=MM("index","user").where(w).row([telephone])
    if(u==None):
        return {
            "error":1,
            "message":"用户不存在或者密码出错"
        }
    p=MM("index","user_password").where("userid=%d" %(u["userid"])).row()
    pwd=tool.umd5(password + str(p["salt"]) )
    if(pwd!=p["password"]):
        return {
            "error":1,
            "message":"用户不存在或者密码出错",
        }
    #登录成功 
    token=setToken(u["userid"],p["password"])
    token["error"]=0
    token["message"]="登录成功"   
    return token

@router.get("/logout")
def logout():
    
    return {
        "error":0,
        "message":"success"
    }


