class Timeline:
    """タイムラインの取得とsince_idとmax_idを保存、取得するクラス"""
    def __init__(self, api, storage):
        """
        Parameters
        ----------
        api : tweepy.api.API
            tweepyでユーザー認証したTwitterAPIのラッパー
        storage : TimelineIndexStorage
            since_idとmax_idを保存するためのストレージ
        """
        self._api = api
        self._storage = storage

    def home_timeline(self, count, since_id=None, max_id=None):
        """ホームタイムライン上のツイートを取得する

        Parameters
        ----------
        count : int
            取得するツイートの総数。最大は200
        since_id : int, default None
            タイムラインを取得し始めるツイートID
        max_id : int, default None
            タイムラインを取得し終えるツイートID

        Returns
        -------
        tweets : tweepy.models.ResultSet
            ホームタイムライン上のツイート

        Notes
        -----
        `since_id`で指定した値を超えるIDを持つツイートを取得する。
        `max_id`で指定した値以下のIDを持つツイートを取得する。
        両方指定しなければ、最新のタイムラインを取得する。
        """
        tweets = self._api.home_timeline(count=count, since_id=since_id,
                                         max_id=max_id)
        timeline_name = self.home_timeline.__name__

        if tweets != []:
            try:
                self._storage.create_ids(timeline_name, tweets)
            except ValueError:
                self._storage.update_ids(timeline_name, tweets)

        return tweets

    @property
    def get_home_timeline_ids(self):
        """前回のsince_idとmax_idを保持するオブジェクトを取得する

        Returns
        -------
        TimelineIndex or None
            since_idとmax_idを保持するオブジェクト。存在しなければNone
        """
        return self._storage.get_ids("home_timeline")