import Twitterbot as tb
import twitterCMD as tc
import json
import requests


#users
MtGox = '1082140986476847104'
VoltLN = '1098049443151134722'
#commands
PRICE_TXT = '@VoltLN bot give me the Price please'
UPDATE_TXT = '@VoltLN bot update me!'
BLOCKWATCH_TXT ='@VoltLN bot DM me all new blocks'
GETCONF_TXT = '@VoltLN bot tell me when this tx has 1 conf: '



class MyStreamListener(tb.tp.StreamListener):
    def on_status(self, status):
        tweet_id = status.id
        if status.text == PRICE_TXT:
            tc.Specific().reply_price(tweet_id)
        if status.text == UPDATE_TXT:
            tc.Specific().reply_update(tweet_id)
        if status.text == BLOCKWATCH_TXT:
            tc.Specific().dm_block_data(status.user.id)
        #add GETCONF fucntion. 
        
        
    def on_error(self, status_code):
        if status_code == 420:
            return False
        


tracklist = [PRICE_TXT, UPDATE_TXT, BLOCKWATCH_TXT, GETCONF_TXT]      
followlist = [VoltLN]

MSL = MyStreamListener()
myStream = tb.tp.Stream(auth = tb.auth, listener=MSL)
myStream.filter(follow=followlist, track=tracklist)


#myStream.filter(follow=['1082140986476847104'])