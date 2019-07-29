import os
import json
import BTCMod as b
import Twitterbot as tb
from datetime import datetime
import time


class General:
    def get_text(self, tweet_id):
        tweet = tb.api.get_status(tweet_id)
        return tweet.text

    def send_DM(self, recipID, text):
        tb.api.send_direct_message(recipID, text)

    def delete_post(self, tweet_id):
        tb.api.destroy_status(tweet_id)
        print("deleted.")

    def post(self, text):
        post = tb.api.update_status(text)
        return post.id

    def reply(self, reply, tweet_id):
        reply = tb.api.update_status(reply, tweet_id)
        return reply.id

    def search(self, query):
        result = tb.api.search(query)
        data = [s.text.encode('utf-8') for s in result]
        tweet_id = [s.id for s in result]
        print(tweet_id)
        return data, result

class Specific:
    ON = True
    def get_latest_mtGox(self): #Broken
        result = tb.api.user_timeline("MtGox101", count=1)
        pr = result['created_at']
        print(pr)

    def bot_update(self):
        """
        Pulls most recent Block via Blockstream API call. 
        Populates Thread: 
        Head: (text), block hash, timestamp, and height. 
        Reply1: TX count, total fees (maybe AVG fees too)

        
        """
        data1 = b.BTCStart().getUpdate()    #possibly merge data1 and data2 into a list, subscript in outputs
        data2 = None                        # FIX get TXCOunt from BTCMod etc. 
        text = f'New Block: {data1[0]}\nHash: {data1[2]}\nTime: {data1[1]}\nSource: Blockstream.info'
        
        
        reply1 = f'It contained {data2} TXs'


        
        #General().thread(text, reply1)
        return data1, data2, text

    def turn_BW_off(self):  # make this reply to the previous post and possibly retweet itself? 
        """
        Used to Turn off block_watch(). 
        """
        self.ON = False
        General().post("Blockwatcher is now off.")
        return self.ON
    
    def block_watch(self):
        """
        Checks for new blocks from the Blockstream API every 15 seconds. 
        Tweets out the Hash, Timestamp, and Height of each new block. 
        """
        General().post("Blockwatcher now on. I will now be tweeting every time a block arrives.")
        tip = self.bot_update()[0][0]
        print(tip)
        nonce = 0
        while self.ON: 
            time.sleep(15)
            new_block_height = self.bot_update()[0][0]
            if new_block_height != tip:
                txt = self.bot_update()[1]
                print(txt)
                General().post(txt)
                new_block_height = tip
                time.sleep(30)
            else:
                nonce += 1
                print(f"Next block hasnt arrived. {nonce}") 

    def post_price(self):  
        """
        Use basic Coindesk API call to give price.  
        """
        

    def respond_to_request(self):  
        """
        Using General().search() and a post() function, will post information requested by users. 
        """

        pass


    def thread(self, text1, text2, *args): 
        """
        Allows posting a thread of an unlimited number of tweets. 
        """
        head = General().post(text1)
        reply1 = General().reply(text2, head)
        for x in args:
            reply2 = General().reply(x, reply1)
            reply1 = reply2


if __name__ == "__main__":
    #General().reply("test 2", 1154979739490246657)
    Specific().get_latest_mtGox()
    #General().get_text(1154982892222713856)
    #Specific().bot_update()
    #Specific().block_watch()
    #General().search("@VoltLN give me the $BTC Price please")
    #General().post("testing.")
    #Specific().thread("Starting a second thread. See below. \n$BTC", "Replying to a second thread. See above.", "Third post", "fourt pos", "fif po", "si p", "s")
    pass