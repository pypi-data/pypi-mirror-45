# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 22:36:17 2019

@author: 
"""


#模块自动执行，在第一次导入时
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
engine = create_engine('sqlite:///:memory:')
#,echo=False

def SQL(st):
   rr = ('''es.sql_exec(es.get_input_df('''
           + '''"'''
           + st
           + '''"),'''
           + '''[eval(i) for i in es.get_input_df('''
           + '''"'''
           + st
           + '''")],"'''
           + st
           + '''")'''
        )
   return rr

#根据sql语句解析输入df
def get_input_df(sql_str):
    rr = []
    #空格分列
    ll = sql_str.split(' ')
    ll2 = []

    #剔除‘’，只保留正常字母
    for i in np.arange(len(ll)):
        if ll[i] != '':
            ll2.append(ll[i])
    # from 和 join 后的表名
    for i in np.arange(len(ll2)):
        if ll2[i] == 'from' or ll2[i] == 'join':
            rr.append(ll2[i+1])
    
    return rr

#接收df的list，导入sqlite
def df_to_sql(df_list):
    for i in np.arange(len(df_list)):
        df = eval(df_list[i])
        df.to_sql(df_list[i], con=engine,if_exists='replace')

#默认显示数据库的所有表名
#默认导出表名为tmp_esql_tbl,覆盖导出
def sql_exec(df_name_list = [],
        df_list = [],
        sql="select name from sqlite_master where type='table' order by name"):


    #默认语句，取所有表名
    if sql=="select name from sqlite_master where type='table' order by name":
        rr = pd.read_sql_query(sql, engine)
        print(rr)
        return
    else:
        #导入表名,执行sql，输出结果
        for i in np.arange(len(df_list)):
            df_name = df_name_list[i]
            df = df_list[i]
            df.to_sql(df_name, con=engine,if_exists='replace',index=False)

    return pd.read_sql_query(sql,con=engine)
