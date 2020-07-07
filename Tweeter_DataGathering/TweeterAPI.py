import tweepy
import sys

# authorization tokens
consumer_key = "[insert your key here]"
consumer_secret = "[insert your secret here]"
access_key = "[insert your key here]"
access_secret = "[insert your secret here]"


# StreamListener class inherits from tweepy.StreamListener and overrides on_status/on_error methods.
class StreamListener(tweepy.StreamListener):
    def on_status(self, status):
        print(status.id_str)
        # if "retweeted_status" attribute exists, flag this tweet as a retweet.
        is_retweet = hasattr(status, "retweeted_status")

        # check if text has been truncated
        if hasattr(status, "extended_tweet"):
            text = status.extended_tweet["full_text"]
        else:
            text = status.text

        # check if this is a quote tweet.
        is_quote = hasattr(status, "quoted_status")
        quoted_text = ""
        if is_quote:
            # check if quoted tweet's text has been truncated before recording it
            if hasattr(status.quoted_status,"extended_tweet"):
                quoted_text = status.quoted_status.extended_tweet["full_text"]
            else:
                quoted_text = status.quoted_status.text

        # remove characters that might cause problems with csv encoding
        remove_characters = [",", "\n"]
        for c in remove_characters:
            text.replace(c, " ")
            quoted_text.replace(c, " ")

        with open("out.csv", "a", encoding='utf-8') as f:
            f.write("%s,%s,%s,%s,%s,%s\n" % (status.created_at, status.user.screen_name, is_retweet, is_quote, text,
                                             quoted_text))

    def on_error(self, status_code):
        print("Encountered streaming error (", status_code, ")")
        sys.exit()


if __name__ == "__main__":
    # complete authorization and initialize API endpoint
    filepath = "/home/i-sip_iot/s_vv/TweeterAPI.txt"
    keys_list = []
    with open(filepath) as fp:
        line = fp.readline()
        cnt = 1
        while line:
            # print("Line {}: {}".format(cnt, line.strip()))
            keys_list.append(line.strip())
            line = fp.readline()
            cnt += 1
    consumer_key, consumer_secret, access_key, access_secret = [el for el in keys_list]
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    # initialize stream
    streamListener = StreamListener()
    stream = tweepy.Stream(auth=api.auth, listener=streamListener, tweet_mode='extended')
    with open("out.csv", "w", encoding='utf-8') as f:
        f.write("date,user,is_retweet,is_quote,text,quoted_text\n")
    tags = ["hate speech"]
    stream.filter(track=tags)

