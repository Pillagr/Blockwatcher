import Twitterbot as tb
import twitterCMD as tc
import json
import requests


MtGox = '1082140986476847104'
VoltLN = '1098049443151134722'

class MyStreamListener(tb.tp.StreamListener):
    def on_status(self, status):
        tweet_id = status.id
        if status.text == '@VoltLN bot give me the Price please':
            tc.Specific().reply_price(tweet_id)
        if status.text == '@VoltLN bot update me!':
            tc.Specific().reply_update(tweet_id)
        if status.text == '@VoltLN bot DM me all new blocks':
            tc.Specific().dm_block_data(status.user.id)
        
        
        
    def on_error(self, status_code):
        if status_code == 420:
            return False
        


tracklist = ['@VoltLN bot give me the Price please', '@VoltLN bot update me!']      
followlist = [VoltLN]

MSL = MyStreamListener()
myStream = tb.tp.Stream(auth = tb.auth, listener=MSL)
myStream.filter(follow=followlist, track=tracklist)


#myStream.filter(follow=['1082140986476847104'])