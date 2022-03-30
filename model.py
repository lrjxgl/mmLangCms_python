#!/usr/bin/python3
import pymysql
import importlib
from config.database import dbconfig
 
conn = pymysql.connect(
    host=dbconfig["host"],
    user=dbconfig["user"], 
    password=dbconfig["password"], 
    database=dbconfig["database"], 
    charset=dbconfig['charset']
)
def DB():
    db=Model()
    db.setDb(conn)
    return db
def MM(mod,table):
    ##动态加载
    module_name=mod+".model."+table+"Model"
    
    spec = importlib.util.find_spec(module_name)
    if spec is not None:
        #模型已定义
        metaclass=importlib.import_module(module_name)
        c = getattr(metaclass, firstUp(table)+"Model") 
        db=c()
        db.table(db.ntable)
        db.setDb(conn)
        return db
    else:  
        #模型未定义   
        db=Model()
        db.setDb(conn)
        db.table(table)
        return db
      
def firstUp(title):
    new_str = '{}{}'.format(title[0].upper(), title[1:])
    return new_str 
class Model:
    sfield="*";swhere="";sorder=""
    sstart=0;slimit=1
    stable=""
    stable_pre=dbconfig["table_pre"]
    conn=None
    def connect(self):
        self.conn = pymysql.connect(
            host=dbconfig["host"],
            user=dbconfig["user"], 
            password=dbconfig["password"], 
            database=dbconfig["database"], 
            charset=dbconfig['charset']
        )
    def setDb(self,conn):
        self.conn=conn
    def query(self,sql,params=()):
        cursor=self.conn.cursor()
        cursor.execute(sql,params)
    def reQuery(self,cursorType,sql,params):
        try:
            self.conn.ping(reconnect=True)
            cursor = self.conn.cursor(cursor=cursorType)
            cursor.execute(sql,params)
        except pymysql.OperationalError:
            self.connect()
            cursor = self.conn.cursor(cursor=cursorType)
            cursor.execute(sql,params)
        return cursor    

    def getAll(self,sql,params=()):
        #cursor = self.conn.cursor(cursor = pymysql.cursors.DictCursor)
        #cursor.execute(sql,params)
        cursor=self.reQuery(pymysql.cursors.DictCursor,sql,params)
        lists=cursor.fetchall()
        return lists
    def getCols(self,sql,params=()):
        #cursor = self.conn.cursor()
        # cursor.execute(sql,params)
        cursor=self.reQuery(None,sql,params)
        lists=cursor.fetchall()
        res=[]
        if lists:
            for item in lists:
                res.append(item[0])
            return res       
    def getRow(self,sql,params=()):
  
        cursor=self.reQuery( pymysql.cursors.DictCursor,sql,params)
        lists=cursor.fetchone()
        return lists
    def getOne(self,sql,params=()):

        cursor=self.reQuery(None,sql,params)
        row=cursor.fetchone()
        if row:
            return row[0]     
        
    def commit(self):
        self.conn.commit()
    def rollback(self):
        self.conn.rollback()    
    def close(self):
        self.conn.close()
    #链式操作开始    
    def initParam(self):
        self.sfield="*";self.swhere="";self.sorder=""
        self.sstart=0;self.slimit=1
    def table(self,w):
        self.stable=self.stable_pre+w
        return self
    def fields(self,w):
        self.sfield=w
        return self
    def where(self,w):
        self.swhere=w
        return self;  
    def order(self,w):
        self.sorder=w
        return self
    def limit(self,*ops):
        if(len(ops)==1):
            self.slimit=ops[0]
        else:
            self.sstart=ops[0]
            self.slimit=ops[1]
        return self
    def initSql(self):
        sql="select "+self.sfield+" from "+self.stable
        if(self.swhere!=""):
            sql+=" where "+self.swhere
        if(self.sorder!=""):
            sql+=" order by "+self.sorder
        sql+=" limit "+str(self.sstart)+","+str(self.slimit)  
        self.initParam()  
        return sql      
    def all(self,params=()):
        sql=self.initSql()
        return self.getAll(sql,params)
    def row(self,params=()):
        sql=self.initSql() 
        return self.getRow(sql,params)
    def one(self,params=()):
        sql=self.initSql() 
        return self.getOne(sql,params)
    def cols(self,params=()):
        sql=self.initSql()
        return self.getCols(sql,params)
    def count(self,params=()):
        self.sfield=" count(*) as ct "
        sql=self.initSql()
        return self.getOne(sql,params)    
    def insert(self,data,params=()):
        sql="insert into "+self.stable+" set "+data 
        cursor=self.reQuery(None,sql,params)
        id=cursor.lastrowid
        
        return id
    def update(self,data,params=()):
        sql="update  "+self.stable+" set "+data 
        if(self.swhere!=""):
            sql+=" where "+self.swhere
        else:
            return False 
        self.initParam()    
        cursor=self.reQuery(None,sql,params)
    def delete(self,params=()):
        sql="delete  from "+self.stable
        if(self.swhere!=""):
            sql+=" where "+self.swhere
        self.initParam() 
        cursor=self.reQuery(None,sql,params) 

    
