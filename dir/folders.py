# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 09:50:12 2023

@author: Luiz
"""

import os

def make_dir(date, root = ""):
    """Create a new directory by path must be there year and doy"""
    doy_str = date.strftime("%j")
    
    path_to_create = os.path.join(root, doy_str)
    
    
    try:
        os.mkdir(path_to_create)
        
        for subfolder in ["imager", "ionosonde", "tec"]:   
            os.makedirs(os.path.join(path_to_create, subfolder)) 
        
            print(f"Creation of the directory {subfolder} successfully")
        
    except OSError:
        print(f"Creation of the directory {path_to_create} failed")
      
   
    return path_to_create
