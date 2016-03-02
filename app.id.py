#!/usr/bin/env python3
"""
Created on Fri Aug 14 12:24:33 2015

@author: Ben Longbottom-Smith

creates an 'app.id' file and write my 'app id' into it. 
"""
app_id = str("2a85cc08c277438ebbaf4ba4d656558c")


with open("app.id", mode="wt", encoding="utf8") as d:
   d.write(app_id)
   