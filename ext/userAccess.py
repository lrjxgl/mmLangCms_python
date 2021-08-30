import hashlib
import ext.cache as cache
def setToken(userid,password):
    p1=password[0:16]
    p1m=hashlib.md5(p1.encode(encoding='utf-8')).hexdigest()
    token=str(userid)+".user."+p1m[0:16]
    token_expire=3600 * 24 * 3
    rpm=hashlib.md5(password.encode(encoding='utf-8')).hexdigest()
    refresh_token=str(userid)+".reuser."+rpm[0:16]
    refresh_token_expire=3600 * 24 * 14
    cache.cacheSet(token,userid,token_expire)
    cache.cacheSet(refresh_token,userid,refresh_token_expire)
    return {
        "token":token,
        "token_expire":token_expire,
        "refresh_token":refresh_token,
        "refresh_token_expire":refresh_token_expire
    }
def checkAccess(token):
    row=cache.cacheGet(token)
    if(row==None):
        return 0

    return int(row)
def goLogin():
    return {
        "error":1000,
        "message":"请先登录"

    }    