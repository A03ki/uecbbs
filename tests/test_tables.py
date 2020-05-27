import unittest
import sqlalchemy.orm as orm
from sqlalchemy import create_engine
from sqlalchemy.sql import text

from twissify.tables import TimelineIndex


class TestTimelineIndex(unittest.TestCase):
    def test_find_by_name_default_none(self):
        names = ["home_timeline", "mentions_timeline", "retweets_of_me"]
        session = create_test_session("sqlite:///:memory:")
        create_test_db(session)
        for name in names:
            with self.subTest(name=name):
                actual = TimelineIndex.find_by_name(name, session)
                self.assertEqual(actual, None)

    def test_find_by_name(self):
        names = ["home_timeline", "mentions_timeline", "retweets_of_me"]
        session = create_test_session("sqlite:///:memory:")
        ids = test_ids(names, 2)  # [(0, 1), (2, 3), (4, 5)]
        create_test_db(session)
        insert_test_db(names, ids, session)
        for name, (since_id, max_id) in zip(names, ids):
            with self.subTest(name=name, since_id=since_id, max_id=max_id):
                actual = TimelineIndex.find_by_name(name, session)
                self.assertEqual(actual.name, name)
                self.assertEqual(actual.since_id, since_id)
                self.assertEqual(actual.max_id, max_id)

    def test_all(self):
        names = ["home_timeline", "mentions_timeline", "retweets_of_me"]
        session = create_test_session("sqlite:///:memory:")
        ids = test_ids(names, 2)
        create_test_db(session)
        insert_test_db(names, ids, session)
        actuals = TimelineIndex.all(session)
        for name, (since_id, max_id), actual in zip(names, ids,
                                                    actuals):
            with self.subTest(name=name, since_id=since_id, max_id=max_id):
                self.assertEqual(actual.name, name)
                self.assertEqual(actual.since_id, since_id)
                self.assertEqual(actual.max_id, max_id)


def test_ids(names, n):
    ids = [iter(range(len(names)*n))]*n
    return list(zip(*ids))


def create_test_session(url):
    engine = create_engine(url)
    Session = orm.sessionmaker(bind=engine)
    session = Session()
    return session


def create_test_db(session):
    create_query = text("""create table TimelineIndex(name text,
                           since_id integer, max_id integer);""")
    session.execute(create_query)
    session.commit()


def insert_test_db(names, ids, session):
    rows = [("('{name}', {since_id}, {max_id})"
             .format(name=name, since_id=since_id, max_id=max_id))
            for name, (since_id, max_id) in zip(names, ids)]
    insert_query = text("insert into TimelineIndex values"
                        + ", ".join(rows) + ";")
    session.execute(insert_query)
    session.commit()


if __name__ == "__main__":
    unittest.main()
