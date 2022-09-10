from operator import truediv
import os
import smtplib
import imghdr
import time
from email.message import EmailMessage

import yfinance as yf
import datetime as dt
import pandas as pd
from pandas_datareader import data as pdr

email_address = "parth082006@gmail.com"
email_password = "oenhlfpcckuonlfq"

msg = EmailMessage()

yf.pdr_override() #to access the stock data

#identifying the start and end date for the data that we want
start = dt.datetime(2022,9,1) 
now = dt.datetime.now()

#identifying the stock and when to be notified
stock = "QQQ"
targetprice = 180

msg["subject"] = "Alert on" + stock
msg['from'] = email_address
msg["to"] = "parth082006@gmail.com"

alerted = False

#getting the stock market data
while True:
    df = pdr.get_data_yahoo(stock, start, now)
    print(df)
    currentclose = df["Adj Close"][-1]
    
    condition = currentclose>targetprice

    if(condition and alerted == False):
        alerted = True
        message = stock + " has activated the alert price of " + str(targetprice) +\
            "\nCurrent Price: " + str(currentclose)
        msg.set_content(message)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(email_address,email_password)
            smtp.send_message(msg)
    
    else:
        print("no new alerts")
    time.sleep(60)