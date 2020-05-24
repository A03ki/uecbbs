def has_media(tweet):
    "メディア情報を含んでいるかを確認する"
    return "media" in tweet.entities


def is_photo(tweet):
    """画像ツイートであるかを確認する

    Notes
    -----
    Twitterの仕様上、動画やGIFは複数投稿できないため、最初のmediaのみを確認している
    """
    if has_media(tweet):
        return tweet.extended_entities["media"][0]["type"] == "photo"
    return False


def is_retweet(tweet):
    return hasattr(tweet, "retweeted_status")


def filter_myretweeted_tweets(tweets):
    "自身がリツイート済みのツイートを取り除く"
    return [tweet for tweet in tweets if not tweet.retweeted]


def filter_retweets(tweets):
    "リツイートを取り除く"
    return [tweet for tweet in tweets if not is_retweet(tweet)]


def filter_protected_tweets(tweets):
    "非公開ツイートを取り除く"
    return [tweet for tweet in tweets if not tweet.user.protected]


def extract_photo_tweets(tweets):
    "画像のツイートを取り出す"
    return [tweet for tweet in tweets if is_photo(tweet)]


def extract_tweet_ids(tweets):
    "ツイートIDを取り出す"
    return [tweet.id for tweet in tweets]


def extract_photo_urls(photo_tweet):
    "画像のツイートに含まれる複数の画像のurlを取り出す"
    return [media["media_url"]
            for media in photo_tweet.extended_entities["media"]]


def extract_photos_urls(tweets):
    "それぞれのツイートに含まれる複数の画像のurlを取り出す"
    return [extract_photo_urls(tweet) for tweet in tweets if is_photo(tweet)]
