# JT

#example

import easysql2pd as esql

import pandas as pd

import numpy as np



aa = pd.DataFrame(np.arange(2))

xx = pd.DataFrame(np.arange(3))

sql = '''select 'aa' as tbl ,count(*) as cnt from aa 
        union all 
        select 'xx' as tbl, count(*) as cnt from xx '''


bb = eval(esql.esql_sql)

print(bb)
