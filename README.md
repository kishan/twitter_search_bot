# Twitter-search-bot

Twitter bot that searches for contests on Twitter and automatically enters into them by retweeting. Twitter bot also favorites tweet and follows tweeter if needed to enter into contest.

##Prerequisites
- Tweepy
- Python 2.7

Installation
------------
From the command line:

	pip install tweepy

##Configuring the bot
Before running the bot, you must first set it up so it can connect to the Twitter API. Change setting variables in `main.py`
* `key`: Twitter user key
* `secret`: Twitter user secret
* `consumer-key`: Twitter application consumer key
* `consumer-secret`: Twitter application consumer secret

Running the bot
------------
Run:

	python main.py
