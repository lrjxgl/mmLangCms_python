from typing import Optional
from fastapi import APIRouter,Form,File, UploadFile
from pathlib import Path
from model import MM
from PIL import Image
import time
import os
import ext.oos as oos
router = APIRouter(prefix="/upload")
@router.post("/img")
async def img(upimg: UploadFile = File(...),thumb:Optional[str]=""):
    res = await upimg.read()
    maxid=MM("index","maxid").get()
    dir="attach/"+time.strftime("%Y/%m/%d",time.localtime())
    if Path(dir).exists()==False :
        os.makedirs(dir,0o777)

    filename=dir+"/"+str(maxid)+upimg.filename.replace("/","")

    with open(filename, "wb") as f:
            f.write(res)
    #生成缩略图
    im = Image.open(filename)
    oos.upload(filename)  
    im2=im.resize((100,100),1)
    im2.save(filename+".100x100.png","png") 
    oos.upload(filename+".100x100.png")   
    if thumb=="": 
        im3=im.resize((480,480))
        im3.save(filename+".small.png","png")
        oos.upload(filename+".small.png")   
        im4=im.resize((750,750))
        im4.save(filename+".middle.png","png")  
        oos.upload(filename+".middle.png")       
    return {
        "error":0,
        "message":"success",
        "data":{
            "imgurl":filename,
            "trueimgurl":oos.images_site(filename)
        }
        
    }