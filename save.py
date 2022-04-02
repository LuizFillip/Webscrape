# -*- coding: utf-8 -*-
"""
Created on Fri Sep 17 17:53:14 2021

@author: LuizF
"""

import pandas as pd




def save(path_out, df):
    
    df.to_csv(path_out, index = True, sep = ';')