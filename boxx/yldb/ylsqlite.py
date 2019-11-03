# -*- coding: utf-8 -*-

from __future__ import unicode_literals
'''
Todo List:
    1. 使用ORM 映射
'''
import sqlite3,os

class Sqlite():
    def __init__(self, creatSql, dbpath='sqlite3.db'):
        '''
        创建一个sqlite3 管理器
        creatSql: 构建数据库代码
        dbPath: 数据库路径
        '''
        self.creatSql = creatSql
        self.dbpath = dbpath
        self.creatDbIfNot()
    def creatDbIfNot(self):
        '''
        注意：最后一句不能以逗号结尾
        '''
        dbpath = self.dbpath
        if not os.path.isfile(dbpath):
            dirr = os.path.dirname(dbpath)
            if not os.path.isdir(dirr) and dirr:
                os.makedirs(dirr, exist_ok=True)
            self.exe(self.creatSql)
        
    def exe(self, sql, values=None):
        with sqlite3.connect(self.dbpath) as conn:
            cursor = conn.cursor() 
            if values is None :
                cursor.execute(sql)
            else:
                cursor.execute(sql,values)
            cursor.close()
            conn.commit()
    def insert(self, sql, value):
        self.inserts(sql, [value])
    def inserts(self, sql, values):
        '''
        一次性插入多条语句再commit性能好
        '''
        with sqlite3.connect(self.dbpath) as conn:
            cursor = conn.cursor() 
            for value in values:
                if not isinstance(value,(tuple,list)):
                    value = (value,)
                cursor.execute(sql,value)
            cursor.close()
            conn.commit()
    def select(self, sql, values=None):
        '''
        执行select 返回结果
        '''
        dbpath = self.dbpath
        with sqlite3.connect(dbpath) as conn:
            cursor = conn.cursor() 
            conn = sqlite3.connect(dbpath)
            if values is None :
                cursor.execute(sql)
            else:
                cursor.execute(sql,values)
            resoult = cursor.fetchall()
            cursor.close()
        return resoult
        
if __name__ == '__main__':
    import random as rd
    creat = '''CREATE TABLE t(
    no INTEGER PRIMARY KEY ,
    id INTEGER NOT NULL
);'''
    s = Sqlite(creat)
    insert = 'insert into t (id) values (?)'
    v = rd.randint(0,100)
    s.insert(insert,v)
    
    select = 'select * from t'
    r = s.select(select)
    print(v,r)
    
    pass
