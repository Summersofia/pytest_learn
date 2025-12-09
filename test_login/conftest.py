import pytest
import time
import json
import base64
import urllib.parse
import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import time

url = "http://192.168.8.192:32073"

class Decrypt_body(object):
    # ---------------------------
    # 配置（按实际修改）
    # ---------------------------
    key = b'd(3D0;Iad(3D0;Ia'  # 与后端一致的 16 字节 AES key

    def __init__(self, Key=key):
        self.Key = Key
    # 加解密工具
    def encrypt_for_request(self,plain_json: str) -> str:
        """
        AES-ECB-PKCS7 -> Base64 -> URL-encode
        返回值适合直接插入 form raw body: "body=<returned_string>"
        """
        cipher = AES.new(self.key, AES.MODE_ECB)
        padded = pad(plain_json.encode("utf-8"), AES.block_size)
        encrypted = cipher.encrypt(padded)
        b64 = base64.b64encode(encrypted).decode("utf-8")
        # URL encode the base64 string (same as Java URLEncoder.encode)
        return urllib.parse.quote(b64, safe='')

@pytest.fixture(scope="module")
def login_config():
    config = {
        "url_login" : f"{url}/SUP/Login/SupLogin",
        "headers" : {
            "Accept": "application/json",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
            "Origin": url,
            "Referer": f"{url}/ngweb/login/index.html",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
            "env": "java",
        },
        "cookeis" : {
            "ngloginimage": "-1",
            "loginTime": str(time.time() * 1000),
            "JSESSIONID": "04D9C71CF5856F91D53C7F06C67BD286",
            "JCusSessionId": "7df03a2d6fac48f2bf0055afe8179898"
        }
    }
    return config
@pytest.fixture
def zby_user():
    tool = Decrypt_body()
    body = {
        "orgCode": "",
        "isWeb": 1,
        # 动态时间戳（毫秒）
        "tm": int(time.time() * 1000),
        "userId": "zby",
        "userPwd": "",
        "dataBase": "0004",
        "account": "0004",
        "CustomerCode": "0004",
        "language": "zh-Cn",
        "sid": "7df03a2d6fac48f2bf0055afe8179898"
    }
    encrypted_body_value = tool.encrypt_for_request(json.dumps(body, separators=(',', ':'), ensure_ascii=False))
    raw_body = f"body={encrypted_body_value}"
    params = {
        'raw_body': raw_body,
        'body': body,
    }
    return params

@pytest.fixture
def unlogin_config():
    def _unlogin_config(sessionId, dataBase, userId):
        config = {
            'url_unlog' : f"{url}/SUP/Login/KillOnlineUser",
            'payload':f'ipAddress=100.116.59.64&sessionID={sessionId}&userId={userId}&account={dataBase}',
            'headers' : {
               'env': 'java',
               'Cookie': 'JCusSessionId=ae4ae0bf70d44177a4d071a76c091ed6',
               'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
            }
        }
        return config
    return _unlogin_config

@pytest.fixture
def wrong_pwd():
    tool = Decrypt_body()
    body = {
        "orgCode": "",
        "isWeb": 1,
        # 动态时间戳（毫秒）
        "tm": int(time.time() * 1000),
        "userId": "zby",
        "userPwd": "zxcvasd",
        "dataBase": "0004",
        "account": "0004",
        "CustomerCode": "0004",
        "language": "zh-Cn",
        "sid": "7df03a2d6fac48f2bf0055afe8179898"
    }
    encrypted_body_value = tool.encrypt_for_request(json.dumps(body, separators=(',', ':'), ensure_ascii=False))
    raw_body = f"body={encrypted_body_value}"
    params = {
        'raw_body': raw_body,
        'body': body,
    }
    return params

@pytest.fixture
def wrong_user():
    tool = Decrypt_body()
    body = {
        "orgCode": "",
        "isWeb": 1,
        # 动态时间戳（毫秒）
        "tm": int(time.time() * 1000),
        "userId": "faucka",
        "userPwd": "",
        "dataBase": "0004",
        "account": "0004",
        "CustomerCode": "0004",
        "language": "zh-Cn",
        "sid": "7df03a2d6fac48f2bf0055afe8179898"
    }
    encrypted_body_value = tool.encrypt_for_request(json.dumps(body, separators=(',', ':'), ensure_ascii=False))
    raw_body = f"body={encrypted_body_value}"
    params = {
        'raw_body': raw_body,
        'body': body,
    }
    return params