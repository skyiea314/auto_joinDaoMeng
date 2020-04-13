import hashlib
import requests
import time
import base64
from Crypto.Cipher import AES
import urllib.parse
from pyDes import des, ECB, PAD_PKCS5
import binascii


class AES_CBC:

    def add_to_16(self, value):
        while len(value) % 16 != 0:
            value += '\0'
        return str.encode(value)

    def encrypt_oracle(self, key, text):
        iv = "9618913120112010"
        aes = AES.new(self.add_to_16(key), AES.MODE_CBC, self.add_to_16(iv))
        bs = AES.block_size
        pad2 = lambda s: s + (bs - len(s) % bs) * chr(bs - len(s) % bs)  # PKS7

        encrypt_aes = aes.encrypt(str.encode(pad2(text)))
        encrypted_text = str(base64.encodebytes(encrypt_aes), encoding='utf-8')
        return encrypted_text


def jiami(str):
    aes = AES_CBC()
    # 加密
    key = "4T1JbdlgSM6h1urT"
    enc_text = aes.encrypt_oracle(key, str)
    enc_text = urllib.parse.quote(enc_text)
    return enc_text


def pwd_encrypt(s):
    KEY = '51434574'
    secret_key = KEY
    k = des(secret_key, ECB, pad=None, padmode=PAD_PKCS5)
    en = k.encrypt(s, padmode=PAD_PKCS5)
    return binascii.b2a_hex(en).upper().decode('utf-8')


class Signtoken:

    def signtoken(self, str):
        sha512 = hashlib.sha512()
        sha512.update(str.encode('utf-8'))
        res = sha512.hexdigest()[0:64]
        i = 1
        str2 = ''
        while i < len(res):
            str2 = str2 + res[i]
            i += 2
        return str2


def get_signtoken(str):
    sign = Signtoken()
    return sign.signtoken(str)


class Login:
    a = {"channelName": "dmkj_Android", "countryCode": "CN", "createTime": int(100 * time.time()),
         "device": "Xiaomi Mi MIX 2S", "hardware": "qcom", "modifyTime": int(100 * time.time()),
         "operator": "%E6%9C%AA%E7%9F%A5", "screenResolution": "1080-2116",
         "startTime": int(100 * time.time()) + 19606523,
         "sysVersion": "Android 29 10", "system": "android", "uuid": "A4:60:46:1F:74:BF", "version": "4.2.6"}

    headers = {
        'standardUA': str(a),
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'appdmkj.5idream.net',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'User-Agent': 'okhttp/3.11.0'
    }


    def get_token_pho(self, acc, pwd):
        sss = '{"account":"' + acc + '","pwd":"' + pwd_encrypt(pwd) + '","version":"4.2.4"}'
        sss = '{"account":"' + acc + '","pwd":"' + pwd_encrypt(pwd) + '","signToken":"' + get_signtoken(
            str(sss)) + '","version":"4.2.4"}'
        url = "https://appdmkj.5idream.net/v2/login/phone"
        data = "dataKey=t%2BZ88oeo2xscPIEBzd1JWLr%2Faae06xI9WOwwXOVRupB%2BsAsl1nj2HDpZPc3ygHRlgm0glZajSvF7FsxbGiBe%2FcykCvyhloLZfYPGGLrCZV6ZBVDBHgwg6%2Fkq87A6A%2Bp%2BmTeUyp3eZz4voIGytVkwmlofr0Jn5bgBOitzBJtnq0I%3D&data={}".format(
            jiami(sss))

        res = requests.post(url, headers=self.headers, data=data).json()
        if res['code'] == '100':
            self.name = res['data']['name']
            self.uid = str(res['data']['uid'])
            self.token = res['data']['token']
            return True
        else:
            return False



def get_token(acc, pwd):
    login = Login()
    if login.get_token_pho(acc, pwd):
        with open('a.ini', 'w+', encoding='utf-8') as f:
            f.write(login.token + '\n')
            f.write(login.name + '\n')
            f.write(login.uid)
        return True
    else:
        return False

