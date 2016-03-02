#!/usr/bin/env python3
"""
Created on Thu Aug 13 19:41:08 2015

@author: Ben Longbottom-Smith

Inputs a date, an amount, and codes of two currencies (allow them to 
be given as lower or upper case strings). It then prints the amount 
converted between those currencies, in both directions, i.e., conversion 
of amount from the first currency to the second one and from the second one 
to the first one (so, two lines should be printed), using the exchange rates 
on the given date.
"""
import time
import exrates
from datetime import timedelta, datetime
date_format = "%Y-%m-%d"

c = True
while True:
    try:
        # Convert from string to an actual date
        some_date = str(input("Type a date in YYYY-MM-DD format (blank for today's date): "))    # only lets you get a correct date type
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
            # print(some_date)
            break
        else:
            print("Not a valid date! Enter another :) \n")
            pass
print()
a = input("First currency code: ")      # eur
a = a.upper()
b = input("Second currency code: ")       # gbP
b = b.upper()
amount = input("Amount to convert: ")
print()

print("Currency Converter for " + str(some_date) + ":\n")

d = exrates.convert(amount, a, b, some_date)

print("(" + str(amount) + ") " + str(a) + " -> " + str(b) + ": " + str(d))
print("{:20.2f} (rounded to 2 d.p.)".format(float(d)))
print()

e = exrates.convert(amount, b, a, some_date)

print("(" + str(amount) + ") " + str(b) + " -> " + str(a) + ": " + str(e))
print("{:20.2f} (rounded to 2 d.p.)".format(float(e)))

