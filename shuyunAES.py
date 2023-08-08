# -*- coding: utf-8 -*-
import base64
from Crypto.Cipher import AES
from Crypto.Cipher import AES

class MyAes:
    def encrypt(data,dataSecretIV,dataSecret):
        dataSecretIV = bytes(dataSecretIV, encoding='utf-8')
        dataSecret = bytes(dataSecret, encoding='utf-8')
        data = bytes(data, encoding='utf-8')
        cipher = AES.new(dataSecret, AES.MODE_CBC, dataSecretIV)
        # 余数
        remainder = len(data) % AES.block_size
        # 补足16位
        if remainder != 0:
            data += b'\0' * (AES.block_size - remainder)
        msg = cipher.encrypt(data)
        return base64.b64encode(msg).decode('utf-8')

    def decrypt(data,dataSecretIV,dataSecret):
        dataSecretIV = bytes(dataSecretIV, encoding='utf-8')
        dataSecret = bytes(dataSecret, encoding='utf-8')
        data = bytes(data, encoding='utf-8')
        cipher = AES.new(dataSecret, AES.MODE_CBC, dataSecretIV)
        # 余数
        remainder = len(data) % AES.block_size
        # 补足16位
        if remainder != 0:
            data += b'\0' * (AES.block_size - remainder)
        msg = cipher.decrypt(base64.b64decode(data))
        return msg.decode('utf-8').rstrip('\0')

def hmacSign(aValue,sigSecret):
    import hmac
    import hashlib

    sigSecret = bytes(sigSecret, encoding='utf-8')
    aValue = bytes(aValue, encoding='utf-8')
    return hmac.new(sigSecret, aValue, hashlib.md5).hexdigest().upper()



# padding算法
BS = AES.block_size
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s: s[0:-ord(s[-1:])]


class AES_ENCRYPT(object):
    def __init__(self,key,iv):
        self.key = key
        self.mode = AES.MODE_CBC
        self.iv = iv

    # 加密函数
    def encrypt(self, text):
        cryptor = AES.new(self.key.encode("utf8"), self.mode, self.iv.encode("utf8"))
        self.ciphertext = cryptor.encrypt(bytes(pad(text), encoding="utf8"))
        # AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题，使用base64编码
        return base64.b64encode(self.ciphertext).decode('utf-8')

    # 解密函数
    def decrypt(self, text):
        decode = base64.b64decode(text)
        cryptor = AES.new(self.key.encode("utf8"), self.mode, self.iv.encode("utf8"))
        plain_text = cryptor.decrypt(decode)
        return unpad(plain_text).decode('utf-8')


def encrypt(data,dataSecretIV,dataSecret):
    aes_encrypt = AES_ENCRYPT(dataSecret,dataSecretIV)
    return aes_encrypt.encrypt(data)

def decrypt(data,dataSecretIV,dataSecret):
    aes_encrypt = AES_ENCRYPT(dataSecret,dataSecretIV)
    return aes_encrypt.decrypt(data)


if __name__ == '__main__':
    aes_encrypt = AES_ENCRYPT()
    origin='{"SuccStat":0,"TokenAvailableTime":7200,"AccessToken":"FVYBoyQzNN7c6QQtLNGtB/wrZqzn09BuzLpHxM7aRZaC4CLtnyl5NvnnEOPet+Jg","OperatorID":"MA01R636X","FailReason":0}'
    # encryptResult = aes_encrypt.encrypt(origin)
    # print(encryptResult)
    # encrypt="ActIhQ1JwfQv+uR2akHV5p/bes5VnoDKi6y+UyioKynZZA3w5jWDQF5pg6BcI/5mKEpEnEiecfCaPGxhu/B68DwN/dsmAp1OvU3I+DQ4m1I5Zh6RPiMlB2tsQrDHTBjUXWkb7GIhCCCiVzOTcBJ3s+KyAksKNwm4DlVuXZOYJvLRlRhOB15YzjbfhO1Bz8hTK21bJGKPu9XlzP+emh8NugRwLrMahkgBI3xtTqt47o4="
    encrypt='wpmHajRHMYn7xOSGM/kUqkxQUAd2VxsX8QfW12L0UOO2UpCvlKahs5CJgfU5jv6O'
    d = aes_encrypt.decrypt(encrypt)
    print(d)


    