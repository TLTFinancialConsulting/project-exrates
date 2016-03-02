#!/usr/bin/env python3
""
Created on Fri Aug 14 12:24:33 2015

@author: Ben Longbottom-Smith

creates an 'app.id' file and write my 'app id' into it. 
"""
app_id = str("") #insert your personal and unique app.id inside the "" brackets


with open("app.id", mode="wt", encoding="utf8") as d:
   d.write(app_id)
   
