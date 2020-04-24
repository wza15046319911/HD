import base64
import requests
import re
import json
import time
import rsa
import binascii
from lxml import etree
from bs4 import BeautifulSoup as bs

class WeiboLogin:
    
    def __init__(self, username, password):
        self._nonce = ""
        self._pubkey = ""
        self._rsakv = ""
        self._session = requests.session()
        self._headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"
        }
        self._username = username
        self._password = password
        self._cookie_file = "../task/cookie.json"

    def pre_login(self):
        url = 'https://login.sina.com.cn/sso/prelogin.php?entry=weibo&su=&rsakt=mod&client=ssologin.js(v1.4.19)&_={}'.format(int(time.time() * 1000))
        response = requests.get(url)
        handled_text = response.text
        start = handled_text.find("(")
        handled_text = json.loads(handled_text[start + 1:])
        self._nonce, self._pubkey, self._rsakv = handled_text.get("nonce"), handled_text.get("pubkey"), handled_text.get("rsakv")
        return 1        
    
    def sso_login(self, username, password):
        data = {
            "entry": "weibo",
            "gateway": "1",
            "from": "",
            "savestate": "7",
            "qrcode_flag": "false",
            "useticket": "1",
            "pagerefer": "https://login.sina.com.cn/crossdomain2.php?action=logout&r=https%3A%2F%2Fpassport.weibo.com%2Fwbsso%2Flogout%3Fr%3Dhttps%253A%252F%252Fweibo.com%26returntype%3D1",
            "vsnf": "1",
            "su": password,
            "service": "miniblog",
            "servertime": int(time.time()),
            "nonce": self._nonce,
            "pwencode": "rsa2",
            "rsakv": self._rsakv,
            "sp": username,
            "sr": "2560*1440",
            "encoding": "UTF-8",
            "prelt": "230",
            "url": "https://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack",
            "returntype": "META",
        }
        url = 'https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.19)'
        self._session.post(url, headers=self._headers, data=data)

    def encode_username(self, username):
        return base64.b64encode(username.encode("utf-8"))[:-1]
    
    def encode_password(self, password):
        hex_pubkey = int(self._pubkey, 16)
        pub_key = rsa.PublicKey(hex_pubkey, 65537)
        crypto = rsa.encrypt(password.encode('utf8'), pub_key)
        return binascii.b2a_hex(crypto)
    
    def login(self):
        
        if self.pre_login() == 1:
            username = self.encode_username(self._username)
            text = str(int(time.time())) + '\t' + str(self._nonce) + '\n' + str(self._password)
            password = self.encode_password(text)
            self.sso_login(password, username)
            self.save_cookie(self._session.cookies)
            self._session.close()
            print("Login successful!")
        else:
            print("Login failed!")
            
    def save_cookie(self, cookie):
        with open(self._cookie_file, 'w') as f:
            json.dump(requests.utils.dict_from_cookiejar(cookie), f)

    def load_cookie(self):
        with open(self._cookie_file, 'r') as f:
            cookie = requests.utils.cookiejar_from_dict(json.load(f))
            return cookie    