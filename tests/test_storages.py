import unittest
from unittest.mock import Mock

from test_tables import test_ids, insert_test_db
from twissify.tables import TimelineIndex
from twissify.storages import TimelineIndexStorage


class TestTimelineIndexStorage(unittest.TestCase):
    def test__create_existing_timeline_name(self):
        names = ["home_timeline", "mentions_timeline", "retweets_of_me"]
        ids = test_ids(names, 2)
        storage = TimelineIndexStorage("sqlite:///:memory:")
        insert_test_db(names, ids, storage.session())
        for name in names:
            with self.subTest(name=name):
                with self.assertRaises(ValueError):
                    storage._create(name)

    def test__update_no_existing_timeline_name(self):
        names = ["home_timeline", "mentions_timeline", "retweets_of_me"]
        ids = test_ids(names, 2)
        storage = TimelineIndexStorage("sqlite:///:memory:")
        for name, (since_id, max_id) in zip(names, ids):
            with self.assertRaises(ValueError):
                storage._update(name, since_id=since_id, max_id=max_id)

    def test_create_ids(self):
        storage = TimelineIndexStorage("sqlite:///:memory:")
        expectation_ids = {"since_id": 100, "max_id": 2000}
        names = ["timeline"]
        tweets = Mock(**expectation_ids)
        storage.create_ids(names[0], tweets)
        timelineindex = TimelineIndex.find_by_name(names[0], storage.session())
        self.assertEqual(timelineindex.since_id, expectation_ids["since_id"])
        self.assertEqual(timelineindex.max_id, expectation_ids["max_id"])

    def test_update_ids(self):
        storage = TimelineIndexStorage("sqlite:///:memory:")
        names = ["timeline"]
        ids = test_ids(names, 2)
        expectation_ids = {"since_id": 100, "max_id": 2000}
        session = storage.session()
        insert_test_db(names, ids, session)
        tweets = Mock(since_id=expectation_ids["since_id"],
                      max_id=expectation_ids["max_id"])
        storage.update_ids(names[0], tweets)
        timelineindex = TimelineIndex.find_by_name(names[0], session)
        self.assertEqual(timelineindex.since_id, expectation_ids["since_id"])
        self.assertEqual(timelineindex.max_id, expectation_ids["max_id"])


if __name__ == "__main__":
    unittest.main()
