from TwitterCLI.TweetBuilder import TweetBuilder
import json

class TweetFetcher:
    def __init__(self, source):
        self.source = source
        self.builder = TweetBuilder()

    def getTweets(self):
        tweets = self.source.getNewTweets()
        return self.builder.buildTweets(tweets)

    def getLists(self):
        lists = self.source.getLists()
        return [ e['name'] for e in lists ]

    def getListTweets(self, list_name):
        tweets = self.source.getListTweets(list_name)
        return self.builder.buildTweets(tweets)

    def getHomeTimeline(self):
        tweets = self.source.getHomeTimeline()
        return self.builder.buildTweets(tweets)