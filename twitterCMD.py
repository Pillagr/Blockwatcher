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

    def search(self, query, geocode=None, lang=None, locale=None, result=None, count=None, until=None, since_id=None, max_id=None):
        result = tb.api.search(query, geocode=geocode, lang=lang, result_type=result, count=count, since_id=since_id, max_id=max_id)
        data = [s.text.encode('utf-8') for s in result]
        tweet_id = [s.id for s in result]
        print(result)
        return data, result, tweet_id


class Switch:
    def __init__(self):
        self.ON = True

    def turn_off(self):
        self.ON = False

class Specific:
    
    def get_latest_mtGox(self): #Broken
        result = tb.api.user_timeline("MtGox101", count=1)
        pr = result['created_at']
        print(pr)

    def find_block_fees(self, block_hash):
        txs = b.get_transaction_ids(block_hash)
        fee_sum = 0
        for tx in txs:
            tx_fee = b.get_transaction(tx).fee
            fee_sum += tx_fee
            print(fee_sum)
        return fee_sum

    def get_update(self):
        """
        Pulls the most recent data: 
        block height, hash, and timestamp, tx count, fees
        Used for post_block_data()
        """
        tip = b.get_last_block_hash()
        update = b.get_block_by_hash(tip)
        return update
    
    def post_update(self):
        """Pubishes data on the most recent block."""
        data = self.get_update()
        form = self.format_block_data(data)
        self.thread(form[0], form[1])
    
    def reply_update(self, tweet_id):
        """replies to a request for update"""
        data = self.get_update()
        form = self.format_block_data(data)
        first = General().reply(form[0], tweet_id)
        General().reply(form[1], first)
    
    def format_block_data(self, data):
        """
        Pulls most recent Block via Blockstream API call. 
        Populates Thread: 
        Head: (text), block hash, timestamp, and height. 
        Reply1: TX count, total fees (maybe AVG fees too)
        """
        text = f'New Block: {data.height}\nHash: {data.id}\nTime: {data.timestamp}\nSource: Blockstream.info'
        reply = f'It contained {data.tx_count} TXs and weighed {data.weight} weight units.'
        return text, reply

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
        #General().post("Blockwatcher now on. I will now be tweeting every time a block arrives.")
        tip = self.get_update().id
        
        blockcount = 0
        Switch = Switch()
        while Switch.ON: 
            time.sleep(15)
            new_block_id = self.get_update().id
            if new_block_id != tip:
                data = b.get_block_by_hash(new_block_id)
                new_block_id = tip
                blockcount +=1
            return data
    def post_price(self):
        """
        Use basic Coindesk API call to give price.  
        """
        prix = b.getPrice()
        txt = f'The Current Price of $BTC is \nUSD: ${prix.USD}\nGBP: £{prix.GBP}\nEUR: €{prix.EUR}\nTime: {prix.time} \nSource: Coindesk.com'
        General().post(txt)
        
    def reply_price(self, tweet_id):
        """
        Use basic Coindesk API call to give price.  
        """
        prix = b.getPrice()
        txt = f'The Current Price of $BTC is \nUSD: ${prix.USD}\nGBP: £{prix.GBP}\nEUR: €{prix.EUR}\nTime: {prix.time} \nSource: Coindesk.com'
        General().reply(txt, tweet_id)

    def thread(self, text1, text2, *args): 
        """
        Allows posting a thread of an unlimited number of tweets. 
        """
        head = General().post(text1)
        reply1 = General().reply(text2, head)
        for x in args:
            reply2 = General().reply(x, reply1)
            reply1 = reply2

    def dm_block_data(self, recipID):
        tip = self.get_update().id
        blockcount = 0
        Switch = Switch()
        while Switch.ON: 
            time.sleep(15)
            new_block_id = self.get_update().id
            if new_block_id != tip:
                data = b.get_block_by_hash(new_block_id)
                new_block_id = tip
                text = self.format_block_data(data)
                General().send_DM(recipID, (text[0]+text[1]))
                blockcount +=1


    


if __name__ == "__main__":
    #Specific().post_price()
    #Specific().find_tx_fee("f02aa136a95fb47c06546b6b71bc40f7260928d3c6e11cb140ee9742289c62fd")
    #results = General().search("Bitcoin will never go to zero", count=1)[1]
    
    #printasd()
    pass