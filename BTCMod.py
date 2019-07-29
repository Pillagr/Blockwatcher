import requests
from datetime import datetime, time, date, timedelta
import time
#for BTCKey
import hashlib
import base58
import binascii
from pycoin import ecdsa, encoding
import os
import codecs
from math import floor as fl

GENESIS_BLOCK = "000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f"
BASE_URL = "https://blockchain.info/"

def apiCall(endURL):
    url = BASE_URL + endURL
    try: #Try to get JSON
        response = requests.get(url).json()
    except ValueError: #if str
        response = requests.get(url).content.decode('utf-8')
    except Exception as e:
        response = e
    return handle_response(response)

def handle_response(response):
    if isinstance(response, Exception):
        print(response)
        return response
    else: 
        return response

class BTCStart():
    def getPrice(self):
        url = "https://api.coindesk.com/v1/bpi/currentprice.json"
        response = requests.get(
            url,
            headers={"Accept": "application.json"},
        )
        data = response.json()
        bpi = data['bpi']
        USD = bpi['USD']
        bitcoin_rate = int(USD['rate_float'])
        return bitcoin_rate
    
    def getHeight(self):
        endURL = "latestblock"
        data = apiCall(endURL)
        block_hash = data['hash']
        block_time = data['time']
        block_height = data['height']

        
        return block_height, block_time, block_hash

    def getUpdate(self):
        #Price
        bitcoin_rate = self.getPrice()
        #halving
        today = datetime.now()
        halving = datetime(year = 2020, month = 5, day = 22, hour = 17, minute = 47)
        delta = halving - today
        #Block Height
        block_height = self.getHeight()[0]
        timestamp = self.getHeight()[1]
        ts = int(timestamp)
        block_time = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        #print(block_time)
        block_hash = self.getHeight()[2]
        # print("Time until Halving:", delta) #Halving Data
        # print(f"The Price is currently: ${bitcoin_rate}.00") #Price
        # print(f"The Block Height is {block_height}. The hash was {block_hash}") #Block Height and hash
        
        tx_count = BTCInfo().checkBlock(block_hash)
        #print(f"The most recent block included {tx_count} transactions.")  #TX count
        return block_height, block_time, block_hash

# ------- INFO ------- #
class BTCInfo():
    def checkBlock(self, block_hash):
        endURL = f"rawblock/{block_hash}"
        data = apiCall(endURL)
        ver = data['ver']
        prev_block = data['prev_block']
        tx_list = data['tx']
        tx_count = len(tx_list)
        time = data['time']
        height = data['height']
        nonce = data['nonce']
        return ver, prev_block, tx_count, time, height, nonce  #add tx_list if needed


    def practice(self):             #How do i call n variables without running the function n times?
        ver, prev_block, tx_list = self.checkBlock("000000000000000000168b0d9e2f64bff796a74a44f2efa6095b52eb3bf3e2de")[0]
        print(ver, prev_block, tx_list)



    def checkVer(self, block_hash):                 #Get Version 
        datum = self.checkBlock(block_hash)[0]
        print(datum)
    def checkPrev(self, block_hash):                #Get Previous Hash
        datum = self.checkBlock(block_hash)[1]
        print(datum) 
    def countTX(self, block_hash):                  #Get TX Count 
        datum = self.checkBlock(block_hash)[2]
        print(datum) 
    def checkTime(self, block_hash):                #Get Time
        datum = self.checkBlock(block_hash)[3]
        print(datum)
    def checkHeight(self, block_hash):              #Get Height
        datum = self.checkBlock(block_hash)[4]
        print(datum)
    def checkNonce(self, block_hash):               #Get Nonce
        datum = self.checkBlock(block_hash)[5]
        print(datum)

    def block_crawler(self):            #Look at all blocks in reverse order
        block_hash = BTCStart().getHeight()[2]
        block_height = BTCStart().getHeight()[0]   #Does it hurt to get this from diff class? 
        block_time = BTCStart().getHeight()[1]
        
        block0 = GENESIS_BLOCK
        while block_hash != block0:         
            print(f"Block Height: {block_height}        | Block Time: {block_time}        | Block Hash: {block_hash}")
            prev_block = self.checkBlock(block_hash)[1]
            block_hash = prev_block
            block_time = self.checkBlock(block_hash)[3]
            block_height = self.checkBlock(block_hash)[4]
            
    def checkAddr(self):
        params = self.parameters()
        addr = input("Please type your Address (No Bech32, sorry): ")
        endURL = f"rawaddr/{addr}"
        data = apiCall(endURL)
        recd = data['total_received']
        sent = data['total_sent']
        balance = data['final_balance']
        #tx_list = data['txs']
        #tx_count = len(tx_list)
        n_tx = data['n_tx']

        if "R" in params:
            print("Total Received: ", recd, "sats")
        if  "S" in params:
            print("Total Sent: ", sent, "sats")
        if "B" in params:
            print("Current Balance: ", balance, "sats")
        if "T" in params:
            print("Transaction Count: ", n_tx, "TXs")

    def parameters(self):
        params = []
        for n in range (4):
            par = input("What parameter would you like to see? [R]eceied Amount - [S]ent Amount - [B]alance - [T]X Count: ")       
            params.append(par)
            more = input("Would you like to see another parameter? Y/N:  ")
            if more == "N":
                break         
        return params
        
    def watchAddr(self): 
        addr = input("Please type your Address (No Bech32): ")                             #Could check every block instead? 
        endURL = f"rawaddr/{addr}"                                                 #from getHeight, if block_hash != new_block_hash:
        data = apiCall(endURL)
        balance = data['final_balance']
        wait = 720
        print(f"Current Balance: {balance} sats. Updates every {fl(wait/60)} minutes. Now watching...")
        while True:
            new_balance = data['final_balance']
            if new_balance == balance:
                time.sleep(wait) #12 mins, make 10?
            elif new_balance > balance: 
                delta = new_balance - balance
                print(f"The Address has received a Transaction of {delta}!")
            elif new_balance < balance:
                delta = balance - new_balance
                print(f"The Address has sent a Transaction of {delta}!")

class BTCKeys():    #Don't trust yet. If anything, trust WIF format, not Private Key. 
    def newKeys(self):
        rand = codecs.encode(os.urandom(32), 'hex').decode()
        secret_exponent = int('0x'+rand, 0)
        WIF = encoding.secret_exponent_to_wif(secret_exponent, compressed=False)
        full_encode = base58.b58decode(WIF)
        priv_key_full = binascii.hexlify(full_encode)
        priv_key = str(priv_key_full[2:-8])
       # print("Private Key: ", priv_key)       dont trust
       # print(len(priv_key))                   Should be 52, is 67
        print ('WIF: ' + WIF)
        print(len(WIF))
        public_pair = ecdsa.public_pair_for_secret_exponent(ecdsa.secp256k1.generator_secp256k1, secret_exponent)
        hash160 = encoding.public_pair_to_hash160_sec(public_pair, compressed=True)
        PubKey = encoding.hash160_sec_to_bitcoin_address(hash160)
        print('Bitcoin address: %s' % PubKey )
        print(len(PubKey))

    

if __name__ == "__main__":
    #BTCStart().getUpdate()
    #BTCInfo().checkAddr()
    #BTCInfo().countTX("000000000000000000168b0d9e2f64bff796a74a44f2efa6095b52eb3bf3e2de")
    #BTCInfo().block_crawler()
    #BTCKeys().newKeys()
    #BTCInfo().practice()
    #BTCInfo().watchAddr()
    #BTCStart().getHeight()
    BTCStart().getUpdate()
    pass