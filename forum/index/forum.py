from typing import Optional
from fastapi import APIRouter,Form
from model import DB
from model import MM
import ext.oos as oos
from ext.userAccess import checkAccess,goLogin
import ext.tool as tool
import time
router = APIRouter(prefix="/forum")
db=DB()
@router.get("/index")
async def index():
    mad=MM("index","ad")
    flashList=mad.limit(4).listByNo("uniapp-forum-index")
    navList=mad.limit(12).listByNo("uniapp-forum-nav")
    adList=mad.limit(3).listByNo("uniapp-forum-ad")
    recList=MM("forum","forum").limit(6).Dselect()
     
    return {
        "error":0,
        "message": "success",       
        "flashList":flashList,
        "navList":navList,        
        "adList":adList,
        "recList":recList
    }
@router.get("/list")
async def list(
    gid:Optional[int]=0,
    catid:Optional[int]=0,
    per_page:Optional[int]=0
):
    start=per_page
    limit=12
    group=MM("forum","forum").where("gid=%s").row([gid])
    w=" status=1 AND gid=%d " %(gid)
    if(catid>0):
        w+=" AND catid=%d " %(catid)
    list=MM("forum","forum").where(w).limit(start,limit).Dselect()
    rscount=MM("forum","forum").where(w).count()
    catList=MM("forum","mod_forum_category").where("gid=%s").all([gid])
    per_page=start+limit
    per_page=0 if per_page>rscount else per_page
    return {
        "error":0,
        "message":"success",
        "list":list,
        "per_page":per_page,
        "rscount":rscount,
        "group":group,
        "catList":catList
    }  

@router.get("/new")
async def new(
    token:Optional[str]="",
    per_page:Optional[int]=0
):
    
    start=per_page
    limit=12
    w=" status=1 " 
    
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
  
    }      
@router.get("/show")
async def show(id: Optional[int] = None):
    if(id==None):
        return {
            "message":"error",
            "error":1
        }
    data=MM("forum","forum").where("id="+str(id)).row()
    data["imgurl"]=oos.images_site(data["imgurl"])
    data["videourl"]=oos.images_site(data["videourl"])
    data["imgsList"]=oos.parseTrueImgList(data["imgsdata"])
    data["timeago"]=data["createtime"].strftime('%Y-%m-%d %H:%M:%S')
    author=MM("index","user").get(data["userid"])
     
    return {"data":data,"author":author}

@router.get("/my")
async def my(
    token:Optional[str]="",
    per_page:Optional[int]=0
):
    ssuserid=checkAccess(token)
    if(ssuserid==0):
        return goLogin()
    start=per_page
    limit=12
    w=" status in(0,1,2) AND userid=%d " %(ssuserid)
    
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
  
    } 
@router.get("/add")
async def add(
    token:Optional[str]="",
    id:Optional[int]=0
):
    ssuserid=checkAccess(token)
    if(ssuserid==0):
        return goLogin()
    data={}
    imgList=[]
    if(id>0):
        data=MM("forum","forum").where("id="+str(id)).row()
        data["content"]=MM("forum","mod_forum_data").where("id="+str(id)).fields("content").one()
        imgList=oos.parseTrueImgList(data["imgsdata"])
    groupList=MM("forum","forumGroup").groupChild();    
    return {
        "data":data,
        "groupList":groupList,
        "imgList":imgList
    }

@router.post("/save")
async def save(
    token:Optional[str]="",
    title:str=Form(...),
    content:str=Form(...),
    imgsdata:str=Form(""),
    gid:int=Form(...),
    catid:int=Form(...),
    id:int=Form(0)
):
    ssuserid=checkAccess(token)
    if(ssuserid==0):
        return goLogin()
    createtime=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    updatetime=createtime
    if(id==0):
        id=MM("forum","forum").insert(
            "userid=%s,title=%s,gid=%s,catid=%s,imgsdata=%s,createtime=%s,updatetime=%s",
            [ssuserid,title,gid,catid,imgsdata,createtime,updatetime]
        )
        MM("forum","mod_forum_data").insert(
            "id=%s,content=%s",
            [id,content]
        )
    else:
        MM("forum","forum").where("id=%d" %(id)).update(
            "userid=%s,title=%s,gid=%s,catid=%s,imgsdata=%s,createtime=%s,updatetime=%s",
            [ssuserid,title,gid,catid,imgsdata,createtime,updatetime]
        )
        MM("forum","mod_forum_data").where("id=%d" %(id)).update(
            "id=%s,content=%s",
            [id,content]
        )  
    MM("forum","forum").commit()      
    return {
        "error":0,
        "message":"success",
        "id":id
    }    

@router.get("/delete")
async def delete(
    token:Optional[str]="",
    id:Optional[int]=0
):
    ssuserid=checkAccess(token)
    if(ssuserid==0):
        return goLogin()
    row=MM("forum","forum").where("id=%s AND userid=%s").row([id,ssuserid])   
    if row==None:
        return {
            "error":1,
            "message":"暂无权限"
        } 
    MM("forum","forum").where("id=%s").update("status=11",[id])
    MM("forum","forum").commit()
    return {
        "error":0,
        "message":"删除成功"
    }

@router.get("/user")
async def user(token:Optional[str]=""):
    ssuserid=checkAccess(token)
    if(ssuserid==0):
        return goLogin()
    user=MM("index","user").get(ssuserid)
    topic_num=MM("forum","forum").where("userid=%s AND status=1").count([ssuserid])
    comment_num=MM("forum","mod_forum_comment").where("userid=%s AND status in(0,1) ").count([ssuserid])
    return {
        "error":0,
        "message":"success",
        "user":user,
        "topic_num":topic_num,
        "comment_num":comment_num
    }    

@router.get("/addclick")
async def addClick(id: Optional[int] = None):
    return {
            "message":"success",
            "error":0
        }
