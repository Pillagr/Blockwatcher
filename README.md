# Blockwatcher
Python Resources for a BTC/LN-focused TwitterBot for @VoltLN. 
Licensed under MIT License (see LICENSE file). 

Feel free to fork the code, but if you improve upon the bot, all I'd ask is DM @VoltLN or open a PR so I can improve my own implementation. 

NOTE: my notes and issues will be comments in the modules. not issues on GitHub

The goal of this project is to build a fully functioning Twitter bot that will do several things: 

1. Post alerts when new Blocks are found on the BTC network. 
    At first, I will use the Blockstream.info API to check for new blocks, but I hope to learn enough to check my own Node in the future. 
2. Respond to mentions that ask for other data, such as fee rates, mempool size, and the Bitcoin Price (using Coindesk's API). 
    Again, reliance will hopefully be shifted away from APIs and to my own Node in the future. 
3. Post Lightning Network data. This is a distant hope for now, as I can't even get my LN node working (RasPi). 

The organization of this project needs work. But here's how it's supposed to look: 

-The BTCMod.py module contains the classes and functions for  Blockstream, Coindesk, and other API calls. 

-The Twitterbot.py module is used solely for accessing the Twitter API. Possibly, it could also be used to store all the imports

-The twitterCMD.py file is where all the useable functions are actually defined. I broke them up into General and Specific classes (this may be an improper use of classes?). The Specific functions may later be moved to a new script unique to each bot functionality. 
