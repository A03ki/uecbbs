from collections import namedtuple


MYTIMELINE_NAMES = ["home_timeline", "mentions_timeline", "retweets_of_me"]


class TimelineIndex(namedtuple("TimelineIndex",
                               ["since_id", "max_id"],
                               defaults=[None, None])):
    __slots__ = ()


class TimelineIndexModel:
    """最大のツイートIDと最小のツイートIDから1引いた値を保持するための基底クラス

    Notes
    -----
    各属性は`namedtuple`のサブクラスである`TimelineIndex`で初期化させる
    """
    def __init__(self):
        raise NotImplementedError

    def update(self, name, since_id, max_id):
        """属性が持つ`TimelineIndex`の`since_id`と`max_id`を更新する

        Parameters
        ----------
        name : str
            属性の名前
        since_id : int
            Twitter APIのクエリの結果の中で最も大きなツイートID
        max_id : int
            Twitter APIのクエリの結果の中で最も小さなツイートIDから1引いた値
        """
        timelineindex = getattr(self, name)
        timelineindex = timelineindex._replace(since_id=since_id,
                                               max_id=max_id)
        setattr(self, name, timelineindex)

    def __repr__(self):
        fields = [str(getattr(self, field)) for field in self._fields]
        return "{cls_name}({fields})".format(cls_name=self.__class__.__name__,
                                             fields=", ".join(fields))


class MyTimelineIndexModel(TimelineIndexModel):
    """"ユーザー認証したアカウントのタイムラインの`since_id`と`max_id`を保持する

    Attributes
    ----------
    home_timeline : TimelineIndex
        ホームタイムラインの`since_id`と`max_id`を保持するための名前付きタプル
    mentions_timeline : TimelineIndex
        メンションタイムラインの`since_id`と`max_id`を保持するための名前付きタプル
    retweets_of_me : TimelineIndex
        リツイートされたツイートの`since_id`と`max_id`を保持するための名前付きタプル
    _fields : set
        各属性名を要素にもつ集合
    """
    def __init__(self):
        for name in MYTIMELINE_NAMES:
            setattr(self, name, TimelineIndex())

        self._fields = MYTIMELINE_NAMES


class UserTimelineIndexModel(TimelineIndexModel):
    """user_timelineから取得した各ユーザータイムラインの`since_id`と`max_id`を保持する

    Attributes
    ----------
    _fields : set
        各ユーザー名を要素に持つ集合、初期値は{}
    """
    def __init__(self):
        self._fields = {}

    def setattr(self, username):
        """属性に`TimelineIndex`を設定する

        Parameters
        ----------
        username : str
            ユーザーの名前
        """
        setattr(self, username, TimelineIndex())
        self._field.add(username)

    @property
    def usernames(self):
        return self._fields

    def __len__(self):
        return len(self._fields)
