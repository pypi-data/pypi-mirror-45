import random, requests
from hashlib import md5

from . import config

url = 'http://api.fanyi.baidu.com/api/trans/vip/translate'
# via langs. reference: http://api.fanyi.baidu.com/api/trans/product/apidoc
all_via_langs = [
    'zh', 'en', 'jp', 'fra', 'spa', 'th', 'ara', 'ru', 'pt', 
    'de', 'it', 'el', 'nl', 'pl', 'bul', 'est', 'dan', 'fin',
    'cs', 'rom', 'slo', 'swe', 'hu', 'vie',
]


def baidu_translate(text: str, from_lang: str, to_lang: str):
    def caculate_sign(appid, q, salt, key):
        return md5((appid + q + salt + key).encode("utf8")).hexdigest()
    
    salt = str(random.randint(10000, 99999))
    params = {
        "q": text,
        "from": from_lang,
        "to": to_lang,
        "appid": config.appid,
        "salt": salt,
        "sign": caculate_sign(config.appid, text, salt, config.key),
    }
    request = requests.get(url, params=params)
    response = request.json()
    return response["trans_result"][0]["dst"]
