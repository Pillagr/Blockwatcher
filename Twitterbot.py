#Twitterbot
"""
A Twitter Bot to post data about the Bitcoin Blockchain. Other commands also available. 
"""
import tweepy as tp
import time
import os
import requests
from datetime import datetime, time, date, timedelta

#credentials-MtGox
GOXconsumer_key = "vEjBw8lg6vW2UqMdSGtGqs7tU"
GOXconsumer_secret = "7eJ0dZPs1REjDBTOxXXaioF7z1e9IHy7lEtMXhBYllpIecfMHu"
GOXaccess_token = "1082140986476847104-qEreVG3EPyG5NZp6CksJD5REL7GywQ"
GOXaccess_secret = "RMttQqcjstmFWCfBHkEZazwb8mY1QkausacUEndo85kw2"

#credentials-VoltLN 
VOLTconsumer_key = "Bsn4AjPYl1FQpnndLnEqBP5hu"
VOLTconsumer_secret = "7JlYJh6LElgnPjcS5QYoREupmH3i1dm1l6TFAeOk22sGygmWAx"
VOLTaccess_token = "1098049443151134722-iRnz2XYDq3aVaJENb3vTT9dv06O71h"
VOLTaccess_secret = "xaUWypBIn1YUxB8TCxrnkL2vHiaqEfTzkY5mJ6ObJbUGQ"
#CheckSums
VOLT_CHECK_SUM_CK = "4lnPhu"
VOLT_CHECK_SUM_CS = "YEjEpm"
VOLT_CHECK_SUM_AT = "841Rz2"
VOLT_CHECK_SUM_AS = "WnBLvH"
#Determiner
consumer_key = VOLTconsumer_key
consumer_secret = VOLTconsumer_secret
access_token = VOLTaccess_token
access_secret = VOLTaccess_secret

def check_sum():
    checksumCK = consumer_key[3]+consumer_key[8]+consumer_key[13]+consumer_key[21]+consumer_key[23]+consumer_key[24]
    checksumCS = consumer_secret[3]+consumer_secret[8]+consumer_secret[13]+consumer_secret[21]+consumer_secret[23]+consumer_secret[24]
    checksumAT = access_token[3]+access_token[8]+access_token[13]+access_token[21]+access_token[23]+access_token[24]
    checksumAS = access_secret[3]+access_secret[8]+access_secret[13]+access_secret[21]+access_secret[23]+access_secret[24]
    #print(checksumAS, checksumAT, checksumCK, checksumCS)
    if checksumCK == VOLT_CHECK_SUM_CK and checksumCS == VOLT_CHECK_SUM_CS and checksumAT == VOLT_CHECK_SUM_AT and checksumAS == VOLT_CHECK_SUM_AS:
        return True
    else: 
        return False

if not check_sum():
    print("Error: API Keys may be incorrect. Checksums do not match.")
    
#login
auth = tp.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tp.API(auth)
# if not api.test():                                     # FIX???
#     print ("Twitter API test failed.")


if __name__ == "__main__":
    #api.update_status("Testing a Bot!")
    #api.update_status("success!", 1154978447145480192)
    #print(api.get_status(1154978447145480192))
    
    pass
