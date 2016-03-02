#!/usr/bin/env python3
#-*- coding: utf-8 -*-
"""
Created on Mon Aug 10 13:19:41 2015

@author: Ben Longbottom-Smith

COME ON YOU CAN DO IT!!! 

App ID: 2a85cc08c277438ebbaf4ba4d656558c 

To use your App ID, append it to the API URL, eg:

https://openexchangerates.org/api/latest.json?app_id=2a85cc08c277438ebbaf4ba4d656558c #{} .format(app_id, date or else)

Write a module exrates that implements fetching, saving, and analysis of the historical 
exchange rates. The module has to provide the following functions:
"""
from pprint import pprint
import time
from datetime import timedelta, datetime
date_format = "%Y-%m_%d"
import sys
import os
import json
import csv
import urllib.request    # need for fetching

odir = "data"     # where both files are stored
curname = "currencies.csv"

currencies_url = 'http://openexchangerates.org/api/currencies.json'



ex_url = "http://openexchangerates.org/api/historical/{}.json?app_id={}"
    
try:
    with open("app.id", mode="rt", encoding="utf8") as g:
            app_id = g.readline()     # this is the app id being read 
            if app_id == "":
                sys.stderr.write("There is no App ID! But there is a file 'app.id' in the current directory. ")
                sys.exit(-17)
            app_id = app_id.strip()            # strips the whitespace         
                
except Exception:
    sys.stderr.write("There is no file 'app.id' in the current directory, please create one :)")   # creates an error message and stops the module
    sys.exit(-17)

def _fetch_currencies():
    """
    Fetches the currencies list from here and returns it as a dictionary (see 
    the description of the format below).
    """
    global currencies_url
    try:
        f = urllib.request.urlopen(currencies_url)
        charaset = f.info().get_param("charset", "utf8")
        data = f.read()
        formatted = json.loads(data.decode(charaset))   # formatting data from the URL
        return formatted
    except Exception:
        sys.stderr.write("Please check if your Wifi is working! Cannot connect to the internet for data fetching (currency list) or URL has no valid data. Choose a different date if Wifi is working  :( \n")
        sys.exit(1)   
 
def _save_currencies(currencies):
    """    
    Saves the dictionary currencies in the currencies file
    """
    global odir
    sorted_currencies = sorted(currencies.items())
    curname = "currencies.csv"
    if not os.path.exists(odir):
        os.mkdir(odir) 
    cur_file = os.path.join(odir, curname)
    with open(cur_file, 'w', encoding="utf8") as f:
        f.write("Code,Name \n")
        for key, value in sorted_currencies:      # like a list
            if key != str("ZWL"):
                f.write(str(key) + ',' + str(value) + '\n')
            else:
                f.write(str(key) + ',' + str(value))        

def _load_currencies():
    """
    Returns the currencies loaded from the currencies file.
    """
    global odir
    curname = "currencies.csv"
    if not os.path.exists(odir):
        os.mkdir(odir)
    cur_file = os.path.join(odir, curname)
    with open(cur_file, mode="rt", encoding="utf8") as f:     
        f.readline()                     # skip first line
        empty_dic = dict()
        cnt = 0
        for line in f: 
            cnt += 1
            if cnt == 144:
                key = "TOP"                        # add 'TOP' to dictionary here, as it has an unusual character 
                value = "Tongan Pa anga"        
                empty_dic[key] = value 
            else:    
                a = line.split(",")
                a[0] = a[0].strip()
                a[1] = a[1].strip()
                key = a[0]
                value = a[1]
                empty_dic[key] = value
                
    return empty_dic
                

def get_currencies():
    """
    returns the currencies loaded from the currencies file, as a dictionary. 
    If the currencies file doesn't exists, the function fetches the data from the 
    internet, saves it to the currencies file and then returns it.
    """
    global odir
    try: 
        _load_currencies()
        return _load_currencies()
    except Exception:
        odir = "data"     # where both files are stored
        curname = "currencies.csv"
        if not os.path.exists(odir):
            os.mkdir(odir) 
        curname = os.path.join(odir, curname)    # Currency File doesnt exist, I will create another one!      
        _save_currencies(_fetch_currencies())      # we must fetch data from internet, save it then return it
        return _load_currencies()

def _fetch_exrates(date):
    """
    Fetches the exchange rates for the date 'date' from the Open Exchange Rates website
    and return it as a dictionary.
    """
    global ex_url
    global app_id
    new_ex_url = ex_url.format(date, app_id)
    try:
        f = urllib.request.urlopen(new_ex_url)
        charaset = f.info().get_param('charset', 'utf8')
        data = f.read()
        formatted = json.loads(data.decode(charaset)) 
        return formatted  
    except urllib.error.URLError:
        sys.stderr.write("Please check if your Wifi is working! Cannot connect to the internet for data fetching (exchange rates) or URL has no valid data. Choose a different date if Wifi is working :( \n")
        sys.exit(1)               
    
def _save_exrates(date, rates):
    """
    saves the exchange rates data for date 'date' in the appropriate exchange rates file    
    """
    global odir  
    sorted_rates = sorted(rates.items()) 
    exname = "rates-" + str(date) + ".csv"
    if not os.path.exists(odir):
        os.mkdir(odir)
    ex_file = os.path.join(odir, exname)
    with open(ex_file, 'w', encoding="utf8") as f:
        for x in sorted_rates:
            if str("rates") in x:    # found the list
                empty_dic = dict()
                c= str(x).split(",")
                for i in c:
                    split = str(i).split(":")
                    new_split = split
                    cnt = 0
                    if i != c[0]:   # b is a two item thing
                        if "{" in new_split[0]:
                            new_split[0] = new_split[0].replace("{", "")
                        if '"' in new_split[0]:
                            new_split[0] = new_split[0].replace('"', "") 
                        if "'" in new_split[0]:
                            new_split[0] = new_split[0].replace("'", "") 
                        new_split[0] = new_split[0].strip()    
                        key = new_split[0]       
                        if '"' in new_split[1]:
                            new_split[1] = new_split[1].replace('"', "")
                        new_split[1] = new_split[1].replace("})", "")  
                        new_split[1] = new_split[1].strip()  
                        value = new_split[1]
                        empty_dic[key] = value  
                        
                sort_dic = sorted(empty_dic.items()) 
                f.write("Code,Rate \n")
                for key, value in sort_dic:
                    f.write(str(key) + "," + str(value) + "\n")                    

def _load_exrates(date):
    """
    Returns the exchange rates data for date date loaded from the appropriate 
    exchange rates file.
    """
    global odir
    exname = "rates-" + str(date) + ".csv"
    if not os.path.exists(odir):
        os.mkdir(odir)
    ex_file = os.path.join(odir, exname)
    with open(ex_file, mode="rt", encoding="utf8") as f:   
        f.readline()                     # skip first line
        empty_dic = dict()
        for line in f:          
            a = line.split(",")
            a[0] = a[0].strip()
            a[0] = a[0].replace('"', "")
            a[1] = a[1].strip()
            a[1] = a[1].replace(str("\n"), "")
            a[1] = a[1].replace('"', "")
            key = a[0]
            value = a[1]
            empty_dic[key] = value

    return empty_dic       
    
def get_exrates(date):
    """
    Returns the exchange rates data for date date loaded from the appropriate 
    exchange rates file. If that file doesn't exists, the function fetches the 
    data from the internet, saves it to the file, and then returns it.  
    """
    try: 
        _load_exrates(date)
        return _load_exrates(date)                   # if file has already been created of that date!
    except Exception:
        odir = "data"     # where both files are stored
        exname = "rates-" + str(date) + ".csv"
        if not os.path.exists(odir):
            os.mkdir(odir)      
        ex_file = os.path.join("data", exname)   # Exchange File doesnt exist on this date, I will create another one!                  
        _save_exrates(date, _fetch_exrates(date))       # we must fetch data from internet, save it then return it
        
        return _load_exrates(date)

class CurrencyDoesntExistError(Exception):
    """
    exchange rate for either of the currency codes doesn't exist on the date
    I will show an appropriate message.
    """
    pass
            
def convert(amount, from_curr, to_curr, date=time.strftime("%Y-%m-%d") ):
    """
    returns the value obtained by converting the amount amount of the currency from_curr 
    to the currency to_curr on date date. If date is not given, it defaults the current date 
    (you can represent "today" as an empty string).
    
    The formula is amount * to_value / from_value, where to_value and from_value represent the 
    values of the currencies to_curr and from_curr, respectively, on the date date.
    If the exchange rate for either of the currency codes from_curr and to_curr does not exist on 
    the date date, the function must raise a custom exception CurrencyDoesntExistError with an 
    appropriate message.
    """    
    a = sorted(get_exrates(date).items())
    cnt = 0
    for key, value in a:
        if key == from_curr:    # first currency
            cnt += 1
            from_value = float(value)     
        if key == to_curr:      # second currency
            cnt += 1
            to_value = float(value)
    if cnt <= 1:
        raise CurrencyDoesntExistError("At least one of the exchange rates chosen doesn't exist on the date entered")  
        print("\n")
    amount = float(amount)      
    end = amount * to_value / from_value
    return amount * to_value / from_value  







