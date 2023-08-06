# -*- coding: utf-8 -*-
"""
Created on Fri May  3 14:58:59 2019

@author: sunhaibo1
"""

import esqlk as es

import pandas as pd
import numpy as np
#import easysql2pd as es

aa = pd.DataFrame(np.arange(3))


bb = eval(es.SQL("select * from aa"))


print(bb)