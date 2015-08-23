import tweepy
import threading

#fill out with Twitter account information
consumer_key=''
consumer_secret=''
access_token=''
access_token_secret=''

search_wait_interval = 10
number_of_tweets_per_search = 5
retweet_wait_interval = 5
search_phrase = "RT retweet to win"

# authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# initialize variables
tweets_to_retweet = []
last_tweet_id = 0


# Search for tweets with the search_phrase defined above.
# Append all tweets found to tweets_to_retweet list.
def search_for_tweets():
    global last_tweet_id

    # continue to execute search function after specified interval
    t = threading.Timer(search_wait_interval, search_for_tweets)
    t.start()

    try:
        for tweet in tweepy.Cursor(api.search,
                # search query defined above
                q=search_phrase, 
                # only search for tweets more recent than last tweet found
                since_id=last_tweet_id,
                # max time to wait for a response from Twitter
                timeout=5, 
                # wait for rate limits to replenish
                wait_on_rate_limit=True, 
                # print a notification when waiting for rate limits to replenish
                wait_on_rate_limit_notify=True 
                ).items(number_of_tweets_per_search):

            tweets_to_retweet.append(tweet)

            # keep track of last tweet found
            id = tweet.id
            if id > last_tweet_id:
                last_tweet_id = id;

    except:
        print "***** search has stopped *****"


# Retweet tweets found by search function
# Limits rate of retweeting so Twitter doesn't ban account
def retweet_found_tweets():
    # retweet after specified interval
    t = threading.Timer(retweet_wait_interval, retweet_found_tweets)
    t.start()

    if len(tweets_to_retweet) > 0:
        try:
            next_tweet = tweets_to_retweet[0]
            del tweets_to_retweet[0]
            retweet_to_enter(next_tweet)
            follow_to_enter(next_tweet)
            favorite_to_enter(next_tweet)
            print "#######################################"

        except:
            print "tweet failed to retweet"
            print "#######################################"


# retweet given tweet
def retweet_to_enter(tweet):
    id = tweet.id
    text = tweet.text.encode("utf-8")
    print "#######################################"
    print "id: " + str(id) + "\ntweet: " + text + "\n"
    api.retweet(id)
    print "successfully retweeted"

# check if tweet requires follow 
def follow_to_enter(tweet):
    text = tweet.text.encode("utf-8")
    try:
        if "follow" in text.lower():
            try:
                screen_name = tweet.retweeted_status.user.screen_name
            except:
                screen_name = tweet.user.screen_name
            api.create_friendship(screen_name) # follower tweeter
            print "successfully followed " + str(screen_name)
    except:
        print "failed to follow"

# check if tweet requires favorite
def favorite_to_enter(tweet):
    text = tweet.text.encode("utf-8")
    id = tweet.id
    if "favorite" in text.lower():
        try: 
            api.create_favorite(id) #favorite tweet
            print "successfully favorited tweet"
        except:
            print "failed to favorite tweet"

# start bot
def run_twitter_search_bot():
    search_for_tweets()
    retweet_found_tweets()


run_twitter_search_bot()
