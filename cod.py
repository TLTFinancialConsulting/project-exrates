#!/usr/bin/env python3
"""
Created on Tue Aug 11 14:50:23 2015

@author: Ben Longbottom-Smith

(which stands for Currencies On a Date), that inputs a date 
and prints the list of currencies for which there is a data 
on that date (i.e., the keys for the exchange rates dictionary 
on that date). The currencies should be printed in the format 
"Name (code)", one per line, sorted by their code.

Of course, the names are obtained from the currencies list. 
However, some may be missing there (for the currencies that 
don't exist anymore, like SIT that existed in the database 
between 2003-06-02 and 2006-12-22). Those should be printed 
as "<unknonwn> (code)".
"""
import time
import exrates
from datetime import timedelta, datetime
date_format = "%Y-%m-%d"


while True:
    try:
        some_date = input("Type a date in YYYY-MM-DD format (blank for today's date): ")    # only lets you get a correct date type
        real_date = datetime.strptime(some_date, date_format)
        dt = time.strftime("%Y-%m-%d")   #  current date
        present_date = datetime.strptime(dt, date_format)        
        if real_date <= present_date:            
            break
        else:
            print("Date must not be in the future! :) Time travel is impossible \n" )
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

print("Currencies on " + str(some_date) + ":\n")

print("Name (code)") 
print(40*"-")
for key, value in a:     # loop exchange
    cnt = 0
    for k_curr, v_curr in b:     # check all currencies if in exch rates data for that date
        if key == k_curr:      # currency code still exists in the past
            # space = 37 - len(v_curr)
            cnt += 1
            print(str(v_curr) + " " + "(" + str(k_curr) + ")")
    if cnt == 0:     # currency code not in the past
        print("<unknown>" + " " + "(" + str(key) + ")")
        
















