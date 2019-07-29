#Twitterbot
"""
A Twitter Bot to post data about the Bitcoin Blockchain. Other commands also available. 
"""
import tweepy as tp
import keyring as k


#Determiner
consumer_key = k.VOLTconsumer_key
consumer_secret = k.VOLTconsumer_secret
access_token = k.VOLTaccess_token
access_secret = k.VOLTaccess_secret

def check_sum():
    checksumCK = k.VOLT_CHECK_SUM_CK
    checksumCS = k.VOLT_CHECK_SUM_CS
    checksumAT = k.VOLT_CHECK_SUM_AT
    checksumAS = k.VOLT_CHECK_SUM_AS
    #print(checksumAS, checksumAT, checksumCK, checksumCS)
    if checksumCK == k.VOLT_CHECK_SUM_CK and checksumCS == k.VOLT_CHECK_SUM_CS and checksumAT == k.VOLT_CHECK_SUM_AT and checksumAS == k.VOLT_CHECK_SUM_AS:
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
