import unittest
from mock import MagicMock as Mock
from TweetSource import MongoTweetSource

class TestMongoTweetSource(unittest.TestCase):
    def setUp(self):
        self.db = Mock()
        self.mts = MongoTweetSource(self.db)

    def test_it_should_fetch_some_tweets_from_mongo(self):
        self.mts.getNewTweets()
        assert self.db.tweets.find.call_count == 1

    def test_it_should_save_tweets_to_mongo(self):
        self.mts.saveTweets([{ 'user': 'grob' }])
        assert self.db.tweets.insert.call_count == 1
