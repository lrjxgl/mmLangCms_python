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
    def setDb(self,conn):
        self.conn=conn
    def query(self,sql,params=()):
        cursor=self.conn.cursor()
        cursor.execute(sql,params)
        self.conn.commit()
    def getAll(self,sql,params=()):
        cursor = self.conn.cursor(cursor = pymysql.cursors.DictCursor)
        cursor.execute(sql,params)
        lists=cursor.fetchall()
        return lists
    def getCols(self,sql,params=()):
        cursor = self.conn.cursor()
        cursor.execute(sql,params)
        lists=cursor.fetchall()
        res=[]
        if lists:
            for item in lists:
                res.append(item[0])
            return res       
    def getRow(self,sql,params=()):
        cursor = self.conn.cursor(cursor = pymysql.cursors.DictCursor)
        cursor.execute(sql,params)
        lists=cursor.fetchone()
        return lists
    def getOne(self,sql,params=()):
        cursor = self.conn.cursor()
        cursor.execute(sql,params)
        row=cursor.fetchone()
        if row:
            return row[0]     
    def insert(self,sql,params=()):
        cursor=self.conn.cursor()
        cursor.execute(sql,params)
        id=cursor.lastrowid
        self.conn.commit()
        return id
    def update(self,sql,params=()):
        cursor=self.conn.cursor()
        cursor.execute(sql,params)
        self.conn.commit()
    def delete(self,sql,params=()):
        cursor=self.conn.cursor()
        cursor.execute(sql,params)
        self.conn.commit()    

    def close(self):
        self.conn.close()
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
    def all(self):
        sql=self.initSql()
        return self.getAll(sql)
    def row(self):
        sql=self.initSql() 
        return self.getRow(sql)
    def one(self):
        sql=self.initSql() 
        return self.getOne(sql)
    def cols(self):
        sql=self.initSql()
        return self.getCols(sql) 

    
