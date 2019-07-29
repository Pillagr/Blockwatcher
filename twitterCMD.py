import os
import json
import BTCMod as b
#os.chdir("Downloads/code")
import Twitterbot as tb
from datetime import datetime
import time

#remove MyBTC code from twitterbot and actually import MyBTC



class General:
    def get_text(self, id):
        tweet = tb.api.get_status(id)
        print(tweet.text)

    def send_DM(self, recipID, text):
        tb.api.send_direct_message(recipID, text)

    def delete_post(self, id):
        tb.api.destroy_status(id)

    def post(self, text):
        tb.api.update_status(text)

    def reply(self, reply, id):
        tb.api.update_status(reply, id)

    def search(self, query):
        result = tb.api.search(query)
        data = [s.text.encode('utf-8') for s in result]
        tweet_id = [s.id for s in result]
        print(tweet_id)

class Specific:
    ON = True
    def get_latest_mtGox(self): #Broken
        result = tb.api.user_timeline("MtGox101", count=1)
        pr = json.loads(result)
        print(pr['created_at'])

    def bot_update(self):
        data = b.BTCStart().getUpdate()
        text = f'New Block: {data[0]}\nHash: {data[2]}\nTime: {data[1]}\nSource: Blockstream.info'
        #print(data.block_height)
        # came in at . 
        #     It contained {data.tx_count} TXs and its hash was 


        #     The Price is currently {data.bitcoin_rate}
        #     The Halvening is roughly {data.delta} away. 
        #General().post(text)
        return data, text

    def turn_BW_off(self):
        self.ON = False
        General().post("Blockwatcher is now off.")
        return self.ON
    
    def block_watch(self):
        
        #General().post("Blockwatcher now on. I will now be tweeting every time a block arrives.")
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

    def post_price(self):  #Will Post Price
        while True:
            pass

    def respond_to_request(self):  
        """
        Using General().search() and a post() function, will post information requested by users. 
        """
        pass

if __name__ == "__main__":
    #General.reply("test 2", 1154979739490246657)
    #Specific.get_latest_mtGox()
    #General.get_text(1154982892222713856)
    #Specific().bot_update()
    #Specific().block_watch()
    General().search("@VoltLN give me the $BTC Price please")

    pass