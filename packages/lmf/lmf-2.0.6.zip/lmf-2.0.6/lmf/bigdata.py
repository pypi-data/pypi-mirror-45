import pandas as pd 
from sqlalchemy import create_engine,types
from sqlalchemy.dialects.postgresql import TEXT 
import pymssql
import cx_Oracle
import psycopg2 
import MySQLdb
import datetime
import re
import sqlite3
import os 


#postgresql 查询结果输出csv文件
def pg2csv(sql,conp,path,chunksize,f=None,**krg):
    #sql="select * from hefei.gg limit 100"
    #conp=["postgres",'since2015','192.168.4.175','anhui','hefei']
    #path="d:\\test.csv"
    con=create_engine("postgresql://%s:%s@%s/%s"%(conp[0],conp[1],conp[2],conp[3]),encoding='utf-8',execution_options=dict(stream_results=True))
    dfs=pd.read_sql(sql,con,chunksize=chunksize)
    count=1
    for df in dfs:
        total=count*chunksize
        print('第%d行写入中'%total)
        if f is not None:
            df=f(df)
        if count==1:
            df.to_csv(path,index=False,**krg)
        else:
            krg['header']=False
            df.to_csv(path,mode='a+',index=False,**krg)
        count+=1


# sql="select * from hefei.gg limit 100"
# conp=["postgres",'since2015','192.168.4.175','anhui','hefei']
# path="d:\\test.csv"

# def f1(df):
#     df['name']='xx'
#     return df 
# pg2csv(sql,conp,path,10,f1,sep='\001')