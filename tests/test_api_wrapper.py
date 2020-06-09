import unittest
from unittest.mock import Mock

from twissify.api_wrapper import APIWrapper

from test_tables import test_ids


class TestAPIWrapper(unittest.TestCase):
    def test__init__(self):
        class TestAPI:
            def __init__(self, a):
                self._test_attribute = a

            def test_method(self, b):
                return b

            def home_timeline(self):
                return 1

        names = {"_test_attribute", "test_method", "__weakref__", "__new__"}
        api = TestAPI(2)
        storage = None
        apiw = APIWrapper(api, storage)
        for attribute_name in dir(api):
            with self.subTest(attribute_name=attribute_name):
                api_attribute = str(getattr(api, attribute_name))
                apiw_attribute = str(getattr(apiw, attribute_name))

                if attribute_name in names:
                    self.assertEqual(api_attribute, apiw_attribute)
                else:
                    self.assertNotEqual(api_attribute, apiw_attribute)

    def test_home_timeline(self):
        expectation_tweets = [1, 2, 3]
        timeline_name = "home_timeline"
        expectation = {timeline_name: expectation_tweets}
        api = Mock(**{"home_timeline.return_value": expectation_tweets})
        storage = None
        apiw = APIWrapper(api, storage)
        expectation_kwargs = {"count": 100,
                              "since_id": 10,
                              "max_id": 1}
        actual_tweets = apiw.home_timeline(**expectation_kwargs)
        actual = apiw._tweets
        self.assertEqual(actual_tweets, expectation_tweets)
        self.assertEqual(actual, expectation)

    def test_save_timeline_ids_empty_tweets(self):
        tweets = []
        api = None
        storage = Mock()
        apiw = APIWrapper(api, storage)
        timeline_name = "home_timeline"
        apiw.save_timeline_ids(timeline_name, tweets)

        storage.create_ids.assert_not_called()
        storage.update_ids.assert_not_called()

    def test_save_timeline_ids_create_ids(self):
        tweets = [1]
        api = None
        storage = Mock()
        apiw = APIWrapper(api, storage)
        timeline_name = "home_timeline"
        apiw.save_timeline_ids(timeline_name, tweets)

        storage.create_ids.assert_called_once_with(timeline_name, tweets)

    def test_save_timeline_ids_update_ids(self):
        tweets = [2, 3]
        api = None
        storage = Mock(**{"create_ids.side_effect": ValueError})
        apiw = APIWrapper(api, storage)
        timeline_name = "home_timeline"
        apiw.save_timeline_ids(timeline_name, tweets)

        storage.update_ids.assert_called_once_with(timeline_name, tweets)

    def test_home_timeline_ids(self):
        expectation = "Success!"
        api = None
        storage = Mock(**{"get_ids.return_value": expectation})
        apiw = APIWrapper(api, storage)
        actual = apiw.home_timeline_ids
        self.assertEqual(expectation, actual)

        storage.get_ids.assert_called_once_with("home_timeline")

    def test_with_save_timeline_ids_called_timelines(self):
        names = ["home_timeline"]
        return_values = [name + ".return_value" for name in names]
        timelines_tweets = test_ids(return_values, 3)
        api = Mock(**dict(zip(return_values, timelines_tweets)))
        storage = None
        with APIWrapper(api, storage) as apiw:
            apiw.save_timeline_ids = Mock()
            apiw.home_timeline(100)

        for name, tweets in zip(names, timelines_tweets):
            with self.subTest(names=names, tweets=tweets):
                apiw.save_timeline_ids.assert_any_call(name, tweets)


if __name__ == "__main__":
    unittest.main()
