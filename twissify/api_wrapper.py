from collections import namedtuple


class APIWrapper:
    """TwitterAPIのラッパーのラッパー

    Attributes
    ーーーーーー
    home_timeline_ids : TimelineIndex or None
        ホームタイムラインの ``since_id`` と ``max_id`` を保持するオブジェクト
    """
    def __init__(self, api, storage):
        """
        Parameters
        ----------
        api : tweepy.api.API
            tweepyでユーザー認証したTwitterAPIのラッパー
        storage : TimelineIndexStorage
            ``since_id`` と ``max_id`` を保存するためのストレージ
        """
        self._api = api
        self._storage = storage
        self._tweets = {}

        apiw_method_names = filter_special_methods(APIWrapper)
        api_attribute_names = filter_special_methods(api)

        for attribute_name in (api_attribute_names - apiw_method_names):
            try:
                setattr(self, attribute_name, getattr(api, attribute_name))
            except AttributeError:
                pass

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
        ``since_id`` で指定した値を超えるIDを持つツイートを取得する。
        ``max_id`` で指定した値以下のIDを持つツイートを取得する。
        両方指定しなければ、最新のタイムラインを取得する。
        """
        tweets = self._api.home_timeline(count=count, since_id=since_id,
                                         max_id=max_id)
        self._tweets[self.home_timeline.__name__] = tweets
        return tweets

    def save_timeline_ids(self, timeline_name, tweets):
        """タイムラインの ``since_id`` と ``max_id`` を保存する

        Parameters
        ----------
        timeline_name : str
            タイムライン名
        tweets : tweepy.models.ResultSet
            タイムライン上のツイート
        """
        if tweets != []:
            try:
                self._storage.create_ids(timeline_name, tweets)
            except ValueError:
                self._storage.update_ids(timeline_name, tweets)

    @property
    def home_timeline_ids(self):
        """前回の ``since_id`` と ``max_id`` を保持するオブジェクトを取得する

        Returns
        -------
        TimelineIndex
            ``since_id`` と ``max_id`` を保持するオブジェクト
        """
        return self._get_ids("home_timeline")

    def _get_ids(self, name):
        TimelineIndex = namedtuple("TimelineIndex", ["since_id", "max_id"])
        ids = self._storage.get_ids(name)
        if ids is None:
            return TimelineIndex(since_id=None, max_id=None)
        else:
            return TimelineIndex(since_id=ids.since_id, max_id=ids.max_id)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        "各タイムラインの ``since_id`` と ``max_id`` を保存する"
        for timeline_name, tweets in self._tweets.items():
            self.save_timeline_ids(timeline_name, tweets)


def filter_special_methods(obj):
    """特殊メソッド以外の属性名の集合を取得する

    Parameters
    ----------
    obj : object

    Returns
    -------
    set
        特殊メソッドを取り除いた属性の集合
    """
    return {method for method in dir(obj)
            if not (method.startswith("__") and method.endswith("__"))}
