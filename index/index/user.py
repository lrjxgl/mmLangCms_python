from typing import Optional
from fastapi import APIRouter,Form 
from model import MM 
from ext.userAccess import checkAccess,goLogin 
import ext.tool as tool
import ext.sms as sms
import random
from config.config import baseconfig
import ext.cache as cache
from ext.oos import images_site
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
        "data":{
            "user":user
        }
        
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
        "data":{
            "user":user
        }
        
    }         

@router.post("/save")
def save(
    token:Optional[str]="",
    description:str=Form(""),
    nickname:str=Form("")
):
    ssuserid=checkAccess(token)
    if ssuserid==0:
        return goLogin()
    userModel=MM("index","user")
    user=userModel.get(ssuserid)
    upstr=""
    if(user["nickname"]!=nickname):
        u=userModel.where("nickname=%s").row([nickname])
        if(u!=None):
            return {
                "error":1,
                "message":"昵称已存在"
            }
    userModel.where("userid=%d" %(ssuserid)).update("nickname=%s,description=%s",[nickname,description])        
    return {
        "error":0,
        "message":"修改成功"
    }

@router.get("/head")
async def user_head(
    token:Optional[str]=""
):
    ssuserid=checkAccess(token)
    if ssuserid==0:
        return goLogin()
    userModel=MM("index","user")
    user=userModel.where("userid=%s").row([ssuserid])
    user["true_user_head"]=images_site(user["user_head"])
    return {
        "error":0,
        "message":"success",
        "data":{
            "user":user
        }
        
    }


@router.post("/headsave")
async def headSave(
    token:Optional[str]="",
    user_head:str=Form("...")
):
    ssuserid=checkAccess(token)
    if ssuserid==0:
        return goLogin()
    MM("index","user").where("userid=%s").update(
        "user_head=%s",
        [user_head,ssuserid]
    )    
    return {
        "error":0,
        "message":"success"
    }

@router.get("/password")
async def password():
    return {
        "error":0,
        "message":"success"
    }
@router.post("/passwordsave")
async def passwordSave(
    oldpassword:str=Form(...),
    password:str=Form(...),
    password2:str=Form(...),
    token:Optional[str]="",
):
    if password2!=password:
        return {
            "error":1,
            "message":"两次输入密码不一致"
        }
    ssuserid=checkAccess(token)
    if ssuserid==0:
        return goLogin()
    up=MM("index","user_password").where("userid=%s").row([ssuserid])
    op=tool.umd5(oldpassword+str(up["salt"]))
    if(op!=up["password"]):
        return {
            "error":1,
            "message":"旧密码出错"
        }
    password=tool.umd5(password+str(up["salt"])) 
    MM("index","user_password").where("userid=%s").update("password=%s",[password,ssuserid])   
    return {
        "error":0,
        "message":"success"
    }

@router.get("/paypwd")
async def paypwd(
    token:Optional[str]=""
):
    
    return {
        "error":0,
        "message":"success"
    }

@router.post("/paypwdsave")
async def paypwdsave(
    token:Optional[str]="",
    yzm:str=Form(...),
    paypwd:str=Form(...)
):
    ssuserid=checkAccess(token)
    if ssuserid==0:
        return goLogin()
    user=MM("index","user").where("userid=%s").row([ssuserid])
    telephone=user["telephone"]
    key="user.yzm"+telephone+str(yzm)
    if cache.cacheGet(key)==None:
        return {
            "error":1,
            "message":"验证码出错"
        }

    paypwd=tool.umd5(paypwd)
    MM("index","user_password").where("userid=%s").update("paypwd=%s",[paypwd,ssuserid])
    return {
        "error":0,
        "message":"success"
    }


@router.get("/sendsms")
async def sendSms(
    token:Optional[str]=""
):
    ssuserid=checkAccess(token)
    if ssuserid==0:
        return goLogin()
    user=MM("index","user").where("userid=%s").row([ssuserid])
    telephone=user["telephone"]
    yzm=random.randint(1000,9999)
    content="您的验证码："+str(yzm)
    key="user.yzm"+telephone+str(yzm)
    cache.cacheSet(key,1,300)
    if baseconfig["smsTest"]==True:
        return {
            "error":1,
            "message":content
        }  
    keyExpire="user.yzm_expire"+telephone
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