import unittest
from unittest.mock import Mock

from twissify.timeline import Timeline


class TestTimeline(unittest.TestCase):
    def test_home_timeline(self):
        expectation_tweets = [1, 2, 3]
        api = Mock(**{"home_timeline.return_value": expectation_tweets})
        storage = None
        timeline = Timeline(api, storage)
        timeline.save_timeline_ids = Mock()
        expectation = {"count": 100, "since_id": 20, "max_id": 5}
        actual = timeline.home_timeline(**expectation)
        self.assertEqual(actual, expectation_tweets)

        api.home_timeline.assert_called_once_with(**expectation)
        timeline.save_timeline_ids.assert_called_once_with("home_timeline",
                                                           expectation_tweets)

    def test_save_timeline_ids_empty_tweets(self):
        tweets = []
        api = None
        storage = Mock()
        timeline = Timeline(api, storage)
        timeline_name = "home_timeline"
        timeline.save_timeline_ids(timeline_name, tweets)

        storage.create_ids.assert_not_called()
        storage.update_ids.assert_not_called()

    def test_save_timeline_ids_create_ids(self):
        tweets = [1]
        api = None
        storage = Mock()
        timeline = Timeline(api, storage)
        timeline_name = "home_timeline"
        timeline.save_timeline_ids(timeline_name, tweets)

        storage.create_ids.assert_called_once_with(timeline_name, tweets)

    def test_save_timeline_ids_update_ids(self):
        tweets = [2, 3]
        api = None
        storage = Mock(**{"create_ids.side_effect": ValueError})
        timeline = Timeline(api, storage)
        timeline_name = "home_timeline"
        timeline.save_timeline_ids(timeline_name, tweets)

        storage.update_ids.assert_called_once_with(timeline_name, tweets)

    def test_home_timeline_ids(self):
        expectation = "Success!"
        api = None
        storage = Mock(**{"get_ids.return_value": expectation})
        timeline = Timeline(api, storage)
        actual = timeline.home_timeline_ids
        self.assertEqual(expectation, actual)

        storage.get_ids.assert_called_once_with("home_timeline")


if __name__ == "__main__":
    unittest.main()
