#!/usr/bin/env python3
"""
Created on Thu Aug 13 22:05:33 2015

@author: Ben Longbottom-Smith

(stands for History), that inputs two dates, a comma-separated list 
of currency codes (for example, "GBP,eur,cAd"), and a file name. It 
then saves the exchange rates relative to the USD between those two 
dates for the given currencies in CSV file of the given name (in the 
current directory if no path is given).

Each date between the two given dates (including both of them) has to 
go in its own row, the first column must contain the date of that row, 
and each of the currencies must be in its own column.

Only the currencies contained in the currencies list are taken into 
account (the rest are ignored; if there are no valid currencies, the
input is considered invalid). If the value for a certain currency doesn't 
exist on some of the dates, save "-" as its value.

The two input dates may be given in any order. If the first one is older, 
than the dates in the file must go in the chronological order. If the first 
one is newer, you are free to choose the order of the dates in the output 
file.

Be careful when testing this program: each date's data has to be fetched, 
so you should avoid too big date spans as your access might be revoked if 
you clog the server! 
"""
import time
# import exrates
from datetime import timedelta, datetime
date_format = "%Y-%m-%d"
import exrates
import sys


while True:
    try:
        # Convert from string to an actual date
        some_date = input("First date in YYYY-MM-DD format (blank for today's date): ")    # only lets you get a correct date type
        real_date1 = datetime.strptime(some_date, date_format)
        dt = time.strftime("%Y-%m-%d")   #  current date      
        present_date = datetime.strptime(dt, date_format)        
        if real_date1 <= present_date:                 # checks if date is in the future
           break
        else:
            print("Date must not be in the future! Time travel is impossible :) \n" )
            pass
    except ValueError:
        if some_date == "":
            some_date = time.strftime("%Y-%m-%d")   #  current date
            real_date1 = datetime.strptime(some_date, date_format)
            break
        else:
            print("Not a valid date! Enter another :) \n")
        pass

print()
 
while True:
    try:
        # Convert from string to an actual date
        some_date = input("Second date in YYYY-MM-DD format (blank for today's date): ")    # only lets you get a correct date type
        real_date2 = datetime.strptime(some_date, date_format)
        dt = time.strftime("%Y-%m-%d")   #  current date      
        present_date = datetime.strptime(dt, date_format)        
        if real_date2 <= present_date:                 # checks if date is in the future
           break
        else:
            print("Date must not be in the future! Time travel is impossible :) \n" )
            pass
    except ValueError:
        if some_date == "":
            some_date = time.strftime("%Y-%m-%d")   #  current date
            real_date2 = datetime.strptime(some_date, date_format)
            break
        else:
            print("Not a valid date! Enter another :) \n")
        pass

string = input("\n Enter a list of currency codes with no spaces e.g. (GBP,eur,cAd): ")    # makes sure it is a string

list_ = string.split(",")
L = list()
for i in list_:
    i = i.upper()
    L.append(i)

b = sorted(exrates.get_currencies().items())      # imports the currency list, only these currencies will be saved
new_list = list()
cnt = 0
for code in L:                             # e.g. 'GBP', 'EUR', 'CAD'
    for key, value in b:
        if key == code:
            cnt += 1
            new_list.append(code)
if cnt == 0:
    sys.stderr.write("Error! The input is invalid, please choose at least one valid currency code")
    sys.exit(1)       # stops program         
            
file_name = input("\n Enter a file name e.g. (including '.csv'): ")
with open(file_name, mode="wt", encoding="utf8") as g:               # need to save file
    g.write("Date,")
    cnt = 0
    for i in new_list:
        cnt += 1
        if len(new_list) == cnt:
            g.write(i + "\n")       
        else: 
            g.write(i + ",")                           # creates the first line  Date,GBP,EUR,RSD        

if real_date2 < real_date1:
    tmp = real_date1
    real_date1 = real_date2                    # dates made so that real_date1 is always earlier
    real_date2 = tmp

day = (real_date2 - real_date1).days             # works out how many days in between
days_between = day - 1


str_rd1 = real_date1.strftime(date_format)                # e.g. converts date back to a string 2008-04-05

with open(file_name, mode="rt", encoding="utf8") as g, \
     open(file_name, mode="at", encoding="utf8") as f: 
    f.write(str(str_rd1) + ",")
    cnt = 0
    code_cnt = 0
    for code in new_list:                             # 'GBP', 'EUR', 'CAD'
        cnt += 1
        for key, value in sorted(exrates.get_exrates(str_rd1).items()):
            if key == code:                      # write the rate
                code_cnt += 1
                if len(new_list) == cnt:
                    f.write(str(value) + "\n") 
                else: 
                    f.write(str(value) + ",")
                    
        if code_cnt == 0:                             # if no ex rate for code on the date given
            if len(new_list) == cnt:
                f.write("-" + "\n")        # writes '-' on the file
            else: 
                f.write("-,")


for i in range(days_between):
    count = i + 1
    day = real_date1 + timedelta(days=count)            # we now have all the dates (including first and last)
    str_day = day.strftime(date_format)
    
    with open(file_name, mode="rt", encoding="utf8") as g, \
         open(file_name, mode="at", encoding="utf8") as f: 
        f.write(str(str_day) + ",")
        cnt = 0
        code_cnt = 0
        for code in new_list:                             # 'GBP', 'EUR', 'CAD'
            cnt += 1
            for key, value in sorted(exrates.get_exrates(str_day).items()):
                if key == code:                      # write the rate
                   code_cnt += 1
                   if len(new_list) == cnt:
                       f.write(str(value) + "\n") 
                   else: 
                       f.write(str(value) + ",")
                    
            if code_cnt == 0:                   # if no ex rate for code on the date given
                if len(new_list) == cnt:
                    f.write("-" + "\n")        # writes '-' on the file
                else: 
                    f.write("-,")

if real_date1 != real_date2:                    # prevents duplicating data if both dates are the same date
    str_rd2 = real_date2.strftime(date_format)              # e.g. 2008-04-12

    with open(file_name, mode="rt", encoding="utf8") as g, \
         open(file_name, mode="at", encoding="utf8") as f: 
        f.write(str(str_rd2) + ",")
        cnt = 0
        code_cnt = 0
        for code in new_list:                             # 'GBP', 'EUR', 'CAD'
            cnt += 1
            for key, value in sorted(exrates.get_exrates(str_rd2).items()):
                if key == code:                      # write the rate
                    code_cnt += 1
                    if len(new_list) == cnt:
                        f.write(str(value) + "\n") 
                    else: 
                        f.write(str(value) + ",")
                    
            if code_cnt == 0:
                if len(new_list) == cnt:
                    f.write("-" + "\n")        # write '-'
                else: 
                    f.write("-,")

