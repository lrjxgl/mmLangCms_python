imgHost="http://oos.mmlang.com/"
def images_site(imgurl):
    if imgurl=="" :
        return ""
    return imgHost+imgurl

def parseImgList(ss):
    arr=ss.split(",")
    mlen=len(arr)
    for i in range(mlen):
        arr[i]=images_site(arr[i])
    return arr
def parseTrueImgList(ss):
    arr=ss.split(",")
    list=[]
    mlen=len(arr)
    for i in range(mlen):
        list.append({
            "imgurl":arr[i],
            "trueimgurl":images_site(arr[i])
        })
    return list    