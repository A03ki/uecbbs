import unittest
from unittest.mock import Mock

from twissify.timeline import Timeline


class TestTimeline(unittest.TestCase):
    def test_home_timeline_api(self):
        expectation_tweets = []
        api = Mock(**{"home_timeline.return_value": expectation_tweets})
        storage = None
        timeline = Timeline(api, storage)
        expectation_kwargs = {"count": 100,
                              "since_id": 10,
                              "max_id": 1}
        actual = timeline.home_timeline(**expectation_kwargs)
        self.assertEqual(expectation_tweets, actual)

        api.home_timeline.assert_called_once_with(**expectation_kwargs)

    def test_home_timeline_storage_create_ids(self):
        expectation_tweets = [1]
        api = Mock(**{"home_timeline.return_value": expectation_tweets})
        storage = Mock()
        timeline = Timeline(api, storage)
        expectation_kwargs = {"count": 200,
                              "since_id": 20,
                              "max_id": 2}
        actual = timeline.home_timeline(**expectation_kwargs)
        self.assertEqual(expectation_tweets, actual)

        storage.create_ids.assert_called_once_with("home_timeline",
                                                   expectation_tweets)

    def test_home_timeline_storage_update_ids(self):
        expectation_tweets = [2, 3]
        api = Mock(**{"home_timeline.return_value": expectation_tweets})
        storage = Mock(**{"create_ids.side_effect": ValueError})
        timeline = Timeline(api, storage)
        expectation_kwargs = {"count": 300,
                              "since_id": 30,
                              "max_id": 3}
        actual = timeline.home_timeline(**expectation_kwargs)
        self.assertEqual(expectation_tweets, actual)

        storage.update_ids.assert_called_once_with("home_timeline",
                                                   expectation_tweets)

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
