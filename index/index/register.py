from typing import Optional
from fastapi import APIRouter,Form
from model import DB,MM
import ext.tool as tool
from ext.userAccess import setToken
import ext.sms as sms
import random
from config.config import baseconfig
import ext.cache as cache
router = APIRouter(prefix="/register")
@router.get("/index")
async def index():
    return {
        "error":0,
        "message":"success"
    }
@router.post("/save")
async def save(
    telephone:str=Form(...),
    password: str=Form(...),
    password2: str=Form(...),
    yzm: str=Form(...),
    nickname:str=Form(...)
):
    if password!=password2 :
        return {
            "error":1,
            "message":"两次输入密码不一致"
        }  
    key="regyzm"+telephone+yzm
    if cache.cacheGet(key) == None:
        return {
            "error":1,
            "message":"验证码出错"
        }
    userModel=MM("index","user")
    u1=userModel.where("telephone=%s").row([telephone])
    if u1!=None:
        return {
            "error":1,
            "message":"手机已存在"
        } 
    u1=userModel.where("nickname=%s or username=%s").row([nickname,nickname])
    if u1!=None:
        return {
            "error":1,
            "message":"昵称已存在"
        } 
    userid=userModel.insert(
        "nickname=%s,username=%s,telephone=%s",
        [nickname,nickname,telephone]
    ) 
    salt=random.randint(1000,9999)
    pwd=tool.umd5(password+str(salt)) 
    MM("index","user_password").insert(
        "userid=%s,password=%s,salt=%s",
        [userid,pwd,salt]
    )
    token=setToken(userid,pwd)  
    userModel.commit()
    token["error"]=0
    token["message"]="success"
    return token
@router.get("/sendsms")
async def sendSms(
    telephone:Optional[str]=""
):
    yzm=random.randint(1000,9999)
    content="您的验证码："+str(yzm)
    key="regyzm"+telephone+str(yzm)
    cache.cacheSet(key,1,300)
    if baseconfig["smsTest"]==True:
        return {
            "error":1,
            "message":content
        }  
    keyExpire="regyzm_expire"+telephone
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
        "message":"success"
    }  
