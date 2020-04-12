import io
import requests
from PIL import Image


def load_image_url(image_url):
    """画像urlからImageオブジェクトとHTTPステータスコードを得る

    画像urlに正常にアクセスできたときはImageオブジェクトとHTTPステータスコードを得る
    正常にアクセスできなかったときはImageオブジェクトの代わりにNoneが返る

    Parameters
    ----------
    image_url : str
        画像urlの文字列

    Returns
    -------
    tuple of a inheritance of PIL.ImageFile.ImageFile and int
        Imageオブジェクト(またはNone)とHTTPステータスコードのタプル

    Note: urlが存在しないときはConnectionErrorが呼ばれる
        また、画像url以外のurlではUnidentifiedImageErrorが呼ばれる
    """
    image = None
    response = requests.get(image_url)
    if response.status_code == 200:
        image = Image.open(io.BytesIO(response.content))
    return image, response.status_code
