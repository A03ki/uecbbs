import numpy as np
import unittest
from unittest.mock import Mock, patch

from twissify.api import (has_media, is_photo, is_retweet,
                          filter_myretweeted_tweets, filter_retweets,
                          filter_protected_tweets, extract_photo_tweets,
                          extract_tweet_ids, extract_photos_urls,
                          extract_photo_urls, extract_retweets_origin)


class TestAPI(unittest.TestCase):
    def test_has_media(self):
        response = [{"user": None, "media": None}, {"user": None}]
        expectations = [True, False]
        for expectation, status in zip(expectations, response):
            tweet = Mock(entities=status)
            actual = has_media(tweet)
            self.assertEqual(expectation, actual)

    @patch("twissify.api.has_media", side_effect=[True, True, False])
    def test_is_photo(self, _):
        expectations = [True, False, False]
        media_types = ["photo", "movie", "photo"]
        for expectation, media_type in zip(expectations, media_types):
            tweet = Mock(extended_entities={"media": [{"type": media_type}]})
            actual = is_photo(tweet)
            self.assertEqual(expectation, actual)

    def test_is_retweet(self):
        expectations = [True, False]
        for expectation in expectations:
            tweet = Mock(retweeted_status=None)
            if not expectation:
                del tweet.retweeted_status
            actual = is_retweet(tweet)
            self.assertEqual(expectation, actual)

    def test_filter_myretweeted_tweets(self):
        bools = [True, False, True, False, False]
        tweets = [Mock(retweeted=bool) for bool in bools]
        actuals = filter_myretweeted_tweets(tweets)
        expectations = [tweet for tweet, bool in zip(tweets, bools)
                        if not bool]
        np.testing.assert_array_equal(expectations, actuals)

    @patch("twissify.api.is_retweet",
           side_effect=[True, False, True, False, False])
    def test_filter_retweets(self, _):
        bools = [True, False, True, False, False]
        tweets = [Mock() for _ in bools]
        actuals = filter_retweets(tweets)
        expectations = [tweet for tweet, bool in zip(tweets, bools)
                        if not bool]
        np.testing.assert_array_equal(expectations, actuals)

    def test_filter_protected_tweets(self):
        bools = [True, False, True, False, False]
        tweets = [Mock(**{"user.protected": bool}) for bool in bools]
        actuals = filter_protected_tweets(tweets)
        expectations = [tweet for tweet, bool in zip(tweets, bools)
                        if not bool]
        np.testing.assert_array_equal(expectations, actuals)

    @patch("twissify.api.is_photo",
           side_effect=[True, False, True, False, False])
    def test_extract_photo_tweets(self, _):
        bools = [True, False, True, False, False]
        tweets = [Mock() for _ in bools]
        actuals = extract_photo_tweets(tweets)
        expectations = [tweet for tweet, bool in zip(tweets, bools) if bool]
        np.testing.assert_array_equal(expectations, actuals)

    def test_extract_tweet_ids(self):
        expectations = [True, False, True, False, False]
        tweets = [Mock(id=bool) for bool in expectations]
        actuals = extract_tweet_ids(tweets)
        np.testing.assert_array_equal(expectations, actuals)

    @patch("twissify.api.extract_photo_urls", side_effect=lambda x: x)
    @patch("twissify.api.is_photo",
           side_effect=[True, True, False, False, True])
    def test_extract_photos_urls(self, is_photo, extract_photo_urls):
        tweets = [1, 2, 3, 4, 5]
        actuals = extract_photos_urls(tweets)
        expectations = [1, 2, 5]
        self.assertEqual(5, is_photo.call_count)
        self.assertEqual(3, extract_photo_urls.call_count)
        np.testing.assert_array_equal(expectations, actuals)

    def test_extract_photo_urls(self):
        expectations = [3, 5, 7]
        tweet = Mock(extended_entities={"media": [{"media_url": i}
                                                  for i in expectations]})
        actuals = extract_photo_urls(tweet)
        np.testing.assert_array_equal(expectations, actuals)

    @patch("twissify.api.is_retweet",
           side_effect=[True, False, False, True, True])
    def test_extract_retweets_origin(self, is_retweet):
        bools = [True, False, False, True, True]
        statuses = list(range(0, len(bools)))
        tweets = [Mock(retweeted_status=status) for status in statuses]
        actuals = extract_retweets_origin(tweets)
        expectations = [tweet for tweet, bool in zip(statuses, bools) if bool]
        np.testing.assert_array_equal(expectations, actuals)


if __name__ == "__main__":
    unittest.main()
