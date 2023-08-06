# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 22:36:17 2019

@author: 
"""

#开发方便pandas 使用的sql库，可以在pandas环境中，方便的调用sql语句进行etl开发
#暂定第一版，先用sqlite的语法，建立内存版的数据库的方式来调用
#第一版：输入，每次识别后，全量导入所需的df，导出生成的df，即全量导入导出
#目标：无需用户的任何操作，只需要写sql即可
#第一版函数体部分：
#   1、识别输入df：以"空格+关键字+空格+tbl+空格(只有一个表，这里可以无空格)" 所识别的tbl
#               关键字列表：from,join
#   2、识别输出df：以"create+空格+table+空格+tbl+空格" 所识别的tbl
#   2、输出作为参数导入；
#   2、输出格式化的sql
#   3、第一次调用时，自动创建内存数据库sqlite
#   4、待考虑，压缩数据库等；先以模块的方式处理

#1、init,创建内存数据库,并随机命名
#2、re识别输入输出，导入sqlite
#3、执行sql

#关于数据表更新，如果是手工导入过的，必须再次手工导入才更新，否则非手工导入-每次取最新(尚未实现)


#模块自动执行，在第一次导入时
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
engine = create_engine('sqlite:///:memory:')
#,echo=False


s=''' '''

#外部函数执行
ss = '''esql.sql(esql.get_input_df(sql),
              [eval(i) for i in esql.get_input_df(sql)],
              sql)'''

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
def sql(df_name_list = [],
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
            df.to_sql(df_name, con=engine,if_exists='replace')

    return pd.read_sql_query(sql,con=engine)
