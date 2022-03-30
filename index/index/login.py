from typing import Optional
from fastapi import APIRouter,Form
from model import DB,MM
import ext.tool as tool
from ext.userAccess import setToken,checkAccess,delToken
import random
import ext.sms as sms
from config.config import baseconfig
import ext.cache as cache
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
    return {
        "error":0,
        "message":"登录成功",
        "data":token
    }  
    

@router.get("/logout")
def logout(
    token:Optional[str]="",
    iRefresh_token:Optional[str]=""
):
    
    delToken(token)
    delToken(iRefresh_token)
    cache.commit()
    return {
        "error":0,
        "message":"success"
    }

@router.get("/findpwd")
def findpwd():
    return {
        "error":0,
        "message":"success"
    }
@router.post("/findpwdsave")
def findpwdsave(
    telephone:str=Form(...),
    password: str=Form(...),
    yzm: str=Form(...),
):
    key="loginyzm"+telephone+yzm
    if cache.cacheGet(key) == None:
        return {
            "error":1,
            "message":"验证码出错"
        }
    userModel=MM("index","user")
    u1=userModel.where("telephone=%s").row([telephone])
    if u1==None:
        return {
            "error":1,
            "message":"用户不存在"
        } 
    salt=random.randint(1000,9999)
    pwd=tool.umd5(password+str(salt)) 
    MM("index","user_password").where("userid=%s").update(
        "password=%s,salt=%s",
        [pwd,salt,u1["userid"]]
    )    
    return {
        "error":0,
        "message":"密码修改成功"
    }

@router.get("/sendsms")
async def sendSms(
    telephone:Optional[str]=""
):
    yzm=random.randint(1000,9999)
    content="您的验证码："+str(yzm)
    key="loginyzm"+telephone+str(yzm)
    cache.cacheSet(key,1,300)
    if baseconfig["smsTest"]==True:
        return {
            "error":1,
            "message":content
        }  
    keyExpire="loginzm_expire"+telephone
    if cache.cacheGet(keyExpire)!=None:
        return {
            "error":1,
            "message":"短信发送太频繁了"
        } 
    cache.cacheSet(keyExpire,1,60) 

    sms.send(telephone,content)
    cache.commit()
    return {
        "error":0,
        "message":"短信发送成功"
    }  