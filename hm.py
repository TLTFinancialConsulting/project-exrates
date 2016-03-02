#!/usr/bin/env python3
"""
Created on Sat Aug 15 16:00:27 2015

@author: Ben Longbottom-Smith

(which stands for History of one Month), that inputs two 
integers, year and month, a comma-separated list of currency codes 
(for example, "GBP,eur,cAd"), and a file name. It then saves the 
exchange rates relative to the USD for the given month and year, 
exactly like hist.
"""
import time
# import exrates
from datetime import timedelta, datetime
date_format = "%Y-%m-%d"
import exrates
import sys

cnt = 0        # check if present year is picked

doc = 0       # check if present month is picked, with present year

dt = time.strftime("%Y-%m-%d")   #  current date      
present_date = datetime.strptime(dt, date_format) 
w = str(present_date)

pres_day = int(w[8:10])      # present day in the present month, as an integer

while True:
    try:
        year = int(input("Enter a Year e.g. (1999): "))
        pres_yr = int(w[:4])
        if year <= pres_yr:
            break
        else:
            print("Year must not be in the future! Time travel is impossible :) \n" )
            pass
    except ValueError:
        print("Value is not an integer! \n")
        pass

if year == pres_yr:
    cnt = 1                # shows that we are finding current year data
    
while True:
    try:
        month = int(input("Enter a Month e.g. (2): "))
        pres_mth = int(w[5:7])
        if cnt == 1:            # present year
            if 1 <= month <= pres_mth:
                if month == pres_mth:             # month is last month you could possibly pick
                    doc = 1
                break
            else:
                print("Month must not be in the future! Time travel is impossible :) \n" ) 
                pass
        else:
            if 1 <= month <= 12:
                break
            else:
                pass
    except ValueError:
        print("Value is not an integer! \n")
        pass    
    
if month < 10:
    first_date = (str(year) + "-0" + str(month) + "-01")
else:
    first_date = (str(year) + "-" + str(month) + "-01") 

real_date1 = datetime.strptime(first_date, date_format)

print()

if month == 12:
    nxt_year = year + 1
    nxt_mth = 1

else:    
    nxt_mth = month+1
    nxt_year = year

if nxt_mth < 10:
    sec_date = (str(nxt_year) + "-0" + str(nxt_mth) + "-01")
else:
    sec_date = (str(nxt_year) + "-" + str(nxt_mth) + "-01") 

sec_realdate = datetime.strptime(sec_date, date_format)

day_difference = (sec_realdate - real_date1).days

string = input("Enter a list of currency codes with no spaces e.g. (GBP,eur,cAd): ")     # makes sure it is a string
    
list_ = string.split(",")
L = list()
for i in list_:
    i = i.upper()
    L.append(i)

b = sorted(exrates.get_currencies().items())      # imports the currency list, only these currencies will be saved
new_list = list()
cnt = 0
for code in L:                             # 'GBP', 'EUR', 'CAD'
    for key, value in b:
        if key == code:
            cnt += 1
            new_list.append(code)
if cnt == 0:
    sys.stderr.write("Error! The input is invalid, please choose at least one valid currency code")
    sys.exit(1)       # stops program         
            
print()

file_name = input("Enter a file name e.g. (including '.csv'): ")
with open(file_name, mode="wt", encoding="utf8") as g:               # need to re-save old data, then write more
    g.write("Date,")
    cnt = 0
    for i in new_list:
        cnt += 1
        if len(new_list) == cnt:
            g.write(i + "\n")       
        else: 
            g.write(i + ",")                           # creates the first line  Date, GBP, EUR, RSD        


if doc == 1:                     # if we have chosen the furthest month forward available, e.g. present month.
    day_difference = pres_day     # so file only prints up to , and including, current date
    
    print("\n\nSince you have picked the present year and month, the file will only print up to today's date :)")

for i in range(day_difference):
    count = i
    day = real_date1 + timedelta(days=count)   # we now have all the dates of month
    str_day = day.strftime(date_format)
    
    with open(file_name, mode="rt", encoding="utf8") as g, \
         open(file_name, mode="at", encoding="utf8") as f: 
        f.write(str(str_day) + ",")
        cnt = 0
        code_cnt = 0
        for code in new_list:                             # 'GBP','EUR','CAD'
            cnt += 1
            for key, value in sorted(exrates.get_exrates(str_day).items()):
                if key == code:                      # writes the rate on file
                    code_cnt += 1
                    if len(new_list) == cnt:
                        f.write(str(value) + "\n") 
                    else: 
                        f.write(str(value) + ",")           
           
            if code_cnt == 0:
                if len(new_list) == cnt:
                    f.write("-" + "\n")        # writes '-' on file

                else: 
                    f.write("-,")




















