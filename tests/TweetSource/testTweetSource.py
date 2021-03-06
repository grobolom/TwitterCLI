import unittest
from mock import MagicMock as Mock

from TweetSource import TwitterWrapper

class TestTwitterWrapper(unittest.TestCase):
    """
    these tests seem bad to me right now because we are testing the private
    api instead of the public
    """
    def setUp(self):
        self.twitter = Mock()
        self.mongodb = Mock()
        self.config = { 'user' : 'grob' }
        self.ts = TwitterWrapper(self.config, self.twitter)

    def test_it_should_fetch_latest_tweets_from_twitter(self):
        self.ts.getNewTweets(since=800)
        self.twitter.statuses.user_timeline.assert_called_once_with(
            screen_name = 'grob',
            count = 200,
            include_rts = False,
            since = 800
        )
    def test_it_should_fetch_some_tweets_from_twitter(self):
        self.ts.getNewTweets()
        self.twitter.statuses.user_timeline.assert_called_once_with(
            screen_name = 'grob',
            count = 200,
            include_rts = False
        )

    def test_it_should_fetch_a_list_from_twitter(self):
        self.ts.getListTweets('friends')
        self.twitter.lists.statuses.assert_called_once_with(
            slug = 'friends',
            owner_screen_name = 'grob',
            count = 200,
            include_rts = False
        )

    def test_it_should_fetch_users_list_names(self):
        self.ts.getLists()
        self.twitter.lists.list.assert_called_once_with(
            screen_name = 'grob'
        )

    def test_it_should_fetch_home_timeline(self):
        self.ts.getHomeTimeline()
        self.twitter.statuses.home_timeline.assert_called_once_with(
            count = 200
        )
