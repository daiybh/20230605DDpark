# -*- coding: utf-8 -*-
import base64
from Crypto.Cipher import AES
from Crypto.Cipher import AES

class MyAes:
    def encrypt(self,data,dataSecretIV,dataSecret):
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

    def decrypt(self,data,dataSecretIV,dataSecret):
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
    key='7EA158C99079009A'
    IV='8602818628180248'
    aes_encrypt = AES_ENCRYPT(key,IV)    
    myaes = MyAes()

    origin='{"SuccStat":0,"TokenAvailableTime":7200,"AccessToken":"FVYBoyQzNN7c6QQtLNGtB/wrZqzn09BuzLpHxM7aRZaC4CLtnyl5NvnnEOPet+Jg","OperatorID":"MA01R636X","FailReason":0}'
    
    res = aes_encrypt.encrypt(origin)
    print(res)
    res4 = aes_encrypt.decrypt(res)
    print(res4)


    res2 = myaes.encrypt(origin,IV,key)
    print(res2)

    res3 = myaes.decrypt(res2,IV,key)
    print(res3)

    print("*"*20)
    res5 = aes_encrypt.decrypt(res2)
    print(res5)



    