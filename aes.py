from Crypto.Cipher import AES
from base64 import b64decode, b64encode

BLOCK_SIZE = AES.block_size

class AesCbCCrypt():
    def __init__(self, key, iv):
        self.iv = bytes(iv, encoding='utf-8')
        self.key = bytes(key, encoding='utf-8')

    def pkcs5padding(self, data):
        return self.pkcs7padding(data, 8)

    def pkcs7padding(self, data, block_size=16):
        if type(data) != bytearray and type(data) != bytes:
            raise TypeError("仅支持 bytearray/bytes 类型!")
        pl = block_size - (len(data) % block_size)
        return data + bytearray([pl for i in range(pl)])
    
    def encrypt(self, data):       
        data = self.pkcs7padding(data, 16)
        return AES.new(self.key,  AES.MODE_CBC, self.iv).encrypt(data)
    
    def encrypt_toStr(self,data):
        return b64encode(self.encrypt(data.encode())).decode('utf-8')
    
    def decrypt(self, data):
        aes = AES.new(self.key, AES.MODE_CBC, self.iv)
        decrypt_text = aes.decrypt(data)
        return decrypt_text[:-int(decrypt_text[-1])]
    def decrypt_toStr(self,data):
        return self.decrypt(b64decode(data)).decode('utf-8')

shuyunInfo={
    'OperatorID':'MA61WH5Y-X',
    'OperatorSecret':'41DD20CA7EA158C9',
    'DataSecret':'7EA158C99079009A',
    'DataSecretIV':'8602818628180248',
    'SigSecret':'DE0D64B041DD20CA',
    'token':"MA61WH5Y-X-41DD20CA7EA158C9"
}  
def testPading7():
    aes = AesCbCCrypt(shuyunInfo['DataSecret'],shuyunInfo['DataSecretIV'])
    text = "#START好好学习,天天向上!END#"
    en_byte = aes.encrypt(text.encode())
    print("密文(HEX):", en_byte.hex().upper())
    de_byte = aes.decrypt(en_byte)
    print("明文:", de_byte.decode())

def t1():
    iv='pJPClgUKoLNyLYQv'
    key = 'w1rTWx7tRK6VMtu0'
    encodedMsg ='ActIhQ1JwfQv+uR2akHV5p/bes5VnoDKi6y+UyioKynZZA3w5jWDQF5pg6BcI/5mKEpEnEiecfCaPGxhu/B68DwN/dsmAp1OvU3I+DQ4m1I5Zh6RPiMlB2tsQrDHTBjUXWkb7GIhCCCiVzOTcBJ3s+KyAksKNwm4DlVuXZOYJvLRlRhOB15YzjbfhO1Bz8hTK21bJGKPu9XlzP+emh8NugRwLrMahkgBI3xtTqt47o4='
    aes=AesCbCCrypt(key,iv)

    data =  aes.decrypt(b64decode(encodedMsg))
    print(data.decode())
    myEncodedMsg = aes.encrypt(data)
    print(b64encode(myEncodedMsg).decode())

    data = aes.decrypt_toStr(encodedMsg)
    print(data)

    myEncodedMsg = aes.encrypt_toStr(data)
    print(myEncodedMsg)

def t2():
    aes = AesCbCCrypt(shuyunInfo['DataSecret'],shuyunInfo['DataSecretIV'])
    text = "#START好好学习,天天向上!END#"
    en_byte = aes.encrypt_toStr(text)
    print("密文(HEX):", en_byte)
    de_byte = aes.decrypt_toStr(en_byte)
    print("明文:", de_byte)
   
if __name__ == '__main__':

    t1()
    t2()
 
    