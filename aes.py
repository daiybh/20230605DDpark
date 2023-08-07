from Crypto.Cipher import AES
from base64 import b64decode, b64encode

BLOCK_SIZE = AES.block_size


class AESCipher:

    def __init__(self, key, iv):
        self.key = key
        self.iv = iv

    @staticmethod
    def pad(text):
        return text + (BLOCK_SIZE - len(text.encode()) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(text.encode()) % BLOCK_SIZE)

    @staticmethod
    def un_pad(text):
        return text[:-ord(text[len(text) - 1:])]

    def encrypt(self, text):
        """
        加密
        """
        text = self.pad(text).encode()
        cipher = AES.new(key=self.key.encode(), mode=AES.MODE_CBC, IV=self.iv.encode())
        encrypted_text = cipher.encrypt(text)
        return b64encode(encrypted_text).decode('utf-8')

    def decrypt(self, encrypted_text):
        """
        解密
        """
        encrypted_text = b64decode(encrypted_text)
        cipher = AES.new(key=self.key.encode(), mode=AES.MODE_CBC, IV=self.iv.encode())
        decrypted_text = cipher.decrypt(encrypted_text)
        return self.un_pad(decrypted_text).decode('utf-8')
    

def decodeTest():
    decodedMsg ='ActIhQ1JwfQv+uR2akHV5p/bes5VnoDKi6y+UyioKynZZA3w5jWDQF5pg6BcI/5mKEpEnEiecfCaPGxhu/B68DwN/dsmAp1OvU3I+DQ4m1I5Zh6RPiMlB2tsQrDHTBjUXWkb7GIhCCCiVzOTcBJ3s+KyAksKNwm4DlVuXZOYJvLRlRhOB15YzjbfhO1Bz8hTK21bJGKPu9XlzP+emh8NugRwLrMahkgBI3xtTqt47o4='
    data = decrypt(decodedMsg,'pJPClgUKoLNyLYQv','w1rTWx7tRK6VMtu0')
    print(data)   
    
if __name__ == '__main__':
    test()