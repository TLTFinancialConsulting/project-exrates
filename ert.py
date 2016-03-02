#!/usr/bin/env python3
"""
Created on Thu Aug 13 17:03:38 2015

@author: Ben Longbottom-Smith

(which stands for Exchange Rates Table), that inputs a date 
and prints the exchange rates for that date in a tabular form, 
sorted by the currencies names, with the first column containing 
the string in the form "Name (code)" and the second one containing 
the exchange rate relative to the USD, aligned to the right and written 
to the 5 digits precision. The data has to be retrieved using the 
get_exrates function. 
"""
import time
from pprint import pprint
import exrates
from datetime import timedelta, datetime
date_format = "%Y-%m-%d"
from math import log10, floor

def round_sig(x, sig=2):            # 5 dig. prec. function
    return round(x, sig-int(floor(log10(x)))-1)

c = True
while True:
    try:
        # Convert from string to an actual date
        some_date = input("Type a date in YYYY-MM-DD format (blank for today's date): ")    # only lets you get a correct date type
        real_date = datetime.strptime(some_date, date_format)
        dt = time.strftime("%Y-%m-%d")   #  current date      
        present_date = datetime.strptime(dt, date_format)        
        if real_date <= present_date:                 # checks if date is in the future
            break
        else:
            print("Date must not be in the future! Time travel is impossible :) \n" )
            pass
    except ValueError:
        if some_date == "":
            some_date = time.strftime("%Y-%m-%d")   #  current date
            break
        else:
            print("Not a valid date! Enter another :) \n")
        pass

print()

b = sorted(exrates.get_currencies().items())

a = sorted(exrates.get_exrates(some_date).items())

curr_dic = dict()

for key, value in b:
    tmp = value
    value = key                # swaps my currency key and value items over
    key = tmp
    curr_dic[key] = value    
    
curr_dic = sorted(curr_dic.items())     # sorted by name 

empty_dic = dict()
for key, value in curr_dic:
    k_curr = key
    v_curr = value                # assigns new names for currency

new_dic = dict()
print("Exchange rates on " + str(some_date) + ":\n")

space = 45 - len(str("Name (code)"))
print("Name (code)" + space*" " + "| Exchange rate to USD (5 d.p.) |") 
print(len("Name (code)" + space*" " + "| Exchange rate to USD (5 d.p.) |")*"-")
for key, value in a:     # loop exchange rates
    cnt = 0
    for k_curr, v_curr in sorted(curr_dic):     # check all currencies if in exch rates
        if key == v_curr:      # currency code still exists on the date
            space = 45 - len(str(v_curr) + str(k_curr))
            cnt += 1
            key_new = str(k_curr) + " " + "(" + str(v_curr) + ")"
            new_dic[key_new] = value
    if cnt == 0:     # currency code not in the date
        space = 45 - len("<unknown>")
        key_new = str("<unknown>" + " " + "(" + str(key) + ")")
        value_new = value
        value_new = float(value_new)
        new_dic[key_new] = value_new

for key_new, value_new in sorted(new_dic.items()):
    space = 45 - len(key_new)  
    space = space*" "
    print("{}{}| {:>30}|".format(str(key_new), space, round_sig(float(value_new), 5)))  # 5 dig. prec. and ex_rate aligned to right






