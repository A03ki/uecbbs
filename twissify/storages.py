import sqlalchemy.orm as orm
from sqlalchemy import create_engine

from twissify.tables import TimelineIndex


class TimelineIndexStorage:
    "各タイムラインの`since_id`と`max_id`の保存、更新を行うクラス"
    def __init__(self, url):
        self.engine = create_engine(url)
        TimelineIndex.metadata.create_all(self.engine)
        self.session = orm.scoped_session(orm.sessionmaker(bind=self.engine))

    def _create(self, name, since_id=None, max_id=None):
        """
        Raises
        ------
        ValueError
            既に同一の`name`が存在するとき
        """
        session = self.session()
        timelineindex = TimelineIndex.find_by_name(name, session)
        if timelineindex is not None:
            raise ValueError(("`name`: '{name}' exist.")
                             .format(name=name))

        row = TimelineIndex(name=name, since_id=since_id, max_id=max_id)
        session.add(row)
        session.commit()

    def _update(self, name, since_id, max_id):
        """
        Raises
        ------
        ValueError
            対応する`name`が存在しないとき
        """
        session = self.session()
        timelineindex = TimelineIndex.find_by_name(name, session)
        if timelineindex is None:
            raise ValueError(("`name`: '{name}' dosen't exist.")
                             .format(name=name))

        row = TimelineIndex.find_by_name(name, session)
        row.since_id = since_id
        row.max_id = max_id
        session.commit()

    def create_ids(self, name, tweets):
        """タイムラインから`name`に対応するレコードを新しく作成する

        Parameters
        ----------
        name : str
            名前の文字列
        tweets : tweepy.models.ResultSet
            タイムライン上のツイート
        """
        self._create(name, since_id=tweets.since_id, max_id=tweets.max_id)

    def update_ids(self, name, tweets):
        """タイムラインから`name`に対応するレコードを更新する

        Parameters
        ----------
        name : str
            名前の文字列
        tweets : tweepy.models.ResultSet
            タイムライン上のツイート
        """
        self._update(name, tweets.since_id, tweets.max_id)

    def get_ids(self, name):
        """`name`に対応するレコードを返す

        Parameters
        ----------
        name : str
            名前の文字列

        Returns
        -------
        TimelineIndex
            `since_id`と`max_id`をフィールドとして持つレコード
        """
        session = self.session()
        return TimelineIndex.find_by_name(name, session)
