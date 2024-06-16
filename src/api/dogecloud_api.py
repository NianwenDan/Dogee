from hashlib import sha1
from src.config import ACCESS_KEY, SECRET_KEY
import hmac
import json
import urllib
import sys
import src.logger as logger
import httpx


def send(api_path: str, data: dict={}, json_mode: bool=False) -> dict:
    """
    调用多吉云API

    :param api_path:    调用的 API 接口地址，包含 URL 请求参数 QueryString, 例如：/console/vfetch/add.json?url=xxx&a=1&b=2
    :param data:        POST 的数据，字典，例如 {'a': 1, 'b': 2}，传递此参数表示不是 GET 请求而是 POST 请求
    :param json_mode:   数据 data 是否以 JSON 格式请求，默认为 false 则使用表单形式 (a=1&b=2)

    :type api_path: string
    :type data: dict
    :type json_mode bool

    :return str: 返回的数据
    """

    # 这里替换为你的多吉云永久 AccessKey 和 SecretKey，可在用户中心 - 密钥管理中查看
    # 请勿在客户端暴露 AccessKey 和 SecretKey，否则恶意用户将获得账号完全控制权
    access_key = ACCESS_KEY
    secret_key = SECRET_KEY

    body = ''
    mime = ''
    if json_mode:
        body = json.dumps(data)
        mime = 'application/json'
    else:
        body = urllib.parse.urlencode(data) # Python 2 可以直接用 urllib.urlencode
        mime = 'application/x-www-form-urlencoded'
    sign_str = api_path + "\n" + body
    signed_data = hmac.new(secret_key.encode('utf-8'), sign_str.encode('utf-8'), sha1)
    sign = signed_data.digest().hex()
    authorization = 'TOKEN ' + access_key + ':' + sign
    
    try:
        response = httpx.post('https://api.dogecloud.com'+ api_path, headers= {
            'Authorization': authorization,
            'Content-Type': mime
        })
        logger.new('debug', 'httpx requested:', response.url)

        contents = response.json()
        logger.new('debug', 'httpx response:', contents)
        if response.status_code == 200:
            return contents
    except Exception as err:
        logger.new('error', err)

    return None
