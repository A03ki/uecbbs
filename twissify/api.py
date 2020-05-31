def has_media(tweet):
    """メディア情報を含んでいるかを確認する

    Parameters
    ----------
    tweet : tweepy.models.Status
        ツイートオブジェクト

    Returns
    -------
    bool
        メディア情報を含むかどうかの真偽値
    """
    return "media" in tweet.entities


def is_photo(tweet):
    """画像ツイートであるかを確認する

    Parameters
    ----------
    tweet : tweepy.models.Status
        ツイートオブジェクト

    Returns
    -------
    bool
        画像ツイートかどうかの真偽値

    Notes
    -----
    Twitterの仕様上、動画やGIFは複数投稿できないため、最初のmediaのみを確認している
    """
    if has_media(tweet):
        return tweet.extended_entities["media"][0]["type"] == "photo"
    return False


def is_retweet(tweet):
    """リツイートであるかを確認する

    Parameters
    ----------
    tweet : tweepy.models.Status
        ツイートオブジェクト

    Returns
    -------
    bool
        リツイートかどうかの真偽値
    """
    return hasattr(tweet, "retweeted_status")


def filter_myretweeted_tweets(tweets):
    """自身がリツイート済みのツイートを取り除く

    Parameters
    ----------
    tweets : tweepy.models.ResultSet or array-like of tweepy.models.Status
        ツイートオブジェクトを格納したリスト

    Returns
    -------
    list of tweepy.models.Status
        リツイート済みのツイートを含まないツイートオブジェクトを格納したリスト
    """
    return [tweet for tweet in tweets if not tweet.retweeted]


def filter_retweets(tweets):
    """リツイートを取り除く

    Parameters
    ----------
    tweets : tweepy.models.ResultSet or array-like of tweepy.models.Status
        ツイートオブジェクトを格納したリスト風のオブジェクト

    Returns
    -------
    list of tweepy.models.Status
        リツイートではないツイートオブジェクトを格納したリスト
    """
    return [tweet for tweet in tweets if not is_retweet(tweet)]


def filter_protected_tweets(tweets):
    """非公開ツイートを取り除く

    Parameters
    ----------
    tweets : tweepy.models.ResultSet or array-like of tweepy.models.Status
        ツイートオブジェクトを格納したリスト風のオブジェクト

    Returns
    -------
    list of tweepy.models.Status
        非公開ツイートではないツイートオブジェクトを格納したリスト
    """
    return [tweet for tweet in tweets if not tweet.user.protected]


def extract_photo_tweets(tweets):
    """画像のツイートを取り出す

    Parameters
    ----------
    tweets : tweepy.models.ResultSet or array-like of tweepy.models.Status
        ツイートオブジェクトを格納したリスト風のオブジェクト

    Returns
    -------
    list of tweepy.models.Status
        画像情報を含むツイートオブジェクトを格納したリスト
    """
    return [tweet for tweet in tweets if is_photo(tweet)]


def extract_tweet_ids(tweets):
    """ツイートIDを取り出す

    Parameters
    ----------
    tweets : tweepy.models.ResultSet or array-like of tweepy.models.Status
        ツイートオブジェクトを格納したリスト風のオブジェクト

    Returns
    -------
    list of int
        ツイートIDを格納したリスト
    """
    return [tweet.id for tweet in tweets]


def extract_photo_urls(photo_tweet):
    """画像のツイートに含まれる複数の画像のurlを取り出す

    Parameters
    ----------
    tweets : tweepy.models.Status
        画像情報を含むツイートオブジェクト

    Returns
    -------
    list of str
        最大4つの画像urlを格納したリスト
    """
    return [media["media_url"]
            for media in photo_tweet.extended_entities["media"]]


def extract_photos_urls(tweets):
    """それぞれのツイートに含まれる複数の画像のurlを取り出す

    Parameters
    ----------
    tweets : tweepy.models.ResultSet or array-like of tweepy.models.Status
        ツイートオブジェクトを格納したリスト風のオブジェクト

    Returns
    -------
    lift of list of str
        画像urlを格納したリストを格納したリスト
    """
    return [extract_photo_urls(tweet) for tweet in tweets if is_photo(tweet)]


def extract_retweets_origin(tweets):
    """リツイート元のツイートを取り出す

    Parameters
    ----------
    tweets : tweepy.models.ResultSet or array-like of tweepy.models.Status
        ツイートオブジェクトを格納したリスト風のオブジェクト

    Returns
    -------
    list of tweepy.models.Status
        リツイート元のツイートオブジェクトを格納したリスト
    """
    return [tweet.retweeted_status for tweet in tweets if is_retweet(tweet)]
