#!/usr/bin/env python3
"""
Created on Tue Aug 11 14:50:23 2015

@author: Ben Longbottom-Smith

Prints the list of all the supported currencies 
and their codes in a tabular form, with the names in the 
first column and their respective codes in the second one, 
sorted by their names. The data has to be retrieved using the 
get_currencies function.
"""
import exrates

b = sorted(exrates.get_currencies().items())         # uses 'get_currencies' function

empty_dic = dict()
    
for key, value in b:
    tmp = value
    value = key                # swaps my key and value items over
    key = tmp
    empty_dic[key] = value    
    
good_dic = sorted(empty_dic.items())     # sorted by 'names' now


print("All the supported currencies:\n")
space = 37 - len(str("Name"))
print("Name" + space*" " + " | " + "Code")
print(len(str("Name" + space*" " + " | " + "Code"))*"-")
for key, value in good_dic:
    space = 37 - len(key)
    print("{}".format(key) + space*" " + " | " "{}".format(value))            # create a tabular form :)






