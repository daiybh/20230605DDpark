import json,config,time

import base64

from Crypto.Cipher import AES


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



def decocdeMessage(message):
    if 'OperatorID' not in message:
        return (None,"OperatorID not in message")        
    if 'Data' not in message:
        return (None,"Data not in message")
    if 'TimeStamp' not in message:
        return (None,"TimeStamp not in message")
    if 'Sig' not in message:
        return (None,"Sig not in message")
    if 'Seq' not in message:
        return (None,"Seq not in message")
    
    try:
        data = decrypt(message['Data'],config.shuyunInfo['DataSecretIV'],config.shuyunInfo['DataSecret'])        
        sig = hmacSign(f"{message['OperatorID']}{message['Data']}{message['TimeStamp']}{message['Seq']}",config.shuyunInfo['SigSecret'])
        if sig != message['Sig']:
            return (None,"sig not match")
        apos = data.rfind("}")
        dataA=data[:apos+1]
        return (json.loads(dataA),"请求成功")
    except Exception as e:
        return (None,f"Exception decocdeMessage error:{e}")
        #app.logger.error(f"decocdeMessage error:{e}")

def make_chargeorde_Repsonse(dataJson,ret=0,msg="请求成功"):
    responseJson = {"Data":"J3OPNG7s6nVbKeCHQVDs0g==","Msg":msg,"Ret":ret,"Sig":"15163CB3D8D950E7E4C4450B2D39A08A"}
    responseJson['Data'] = encrypt(dataJson,config.shuyunInfo['DataSecretIV'],config.shuyunInfo['DataSecret'])
    #拼接顺序为返回值（Ret）、返回信息（Msg）、参数内容（Data）。
    responseJson['Sig'] = hmacSign(f"{ret}{msg}{responseJson['Data']}",config.shuyunInfo['SigSecret'])
    return responseJson

tokenCount=0

def GererateToken():    
    import uuid
    tokenSrc = f"{config.shuyunInfo['OperatorID']}{uuid.uuid1()}"
    token = encrypt(tokenSrc,config.shuyunInfo['DataSecretIV'],config.shuyunInfo['OperatorSecret'])
    return token

def makeTokenResponse(ret=0,msg="请求成功",logger=None):
    global tokenCount
    print("makeTokenResponse--------------",tokenCount)
    responseToken = {
                        "SuccStat":0,
                        "FailReason":0,
                        "AccessToken":config.shuyunInfo['token'],
                        "TokenAvailableTime":7200,
                        "OperatorID":config.shuyunInfo['OperatorID'],
                    }    
    responseJson = {"Data":"J3OPNG7s6nVbKeCHQVDs0g==","Msg":msg,"Ret":ret,"Sig":"15163CB3D8D950E7E4C4450B2D39A08A"}    
    secret = config.shuyunInfo['DataSecret']    
    jsonStr = json.dumps(responseToken,ensure_ascii=False)
    if logger:
        logger.debug(f"makeTokenResponse jsonStr:{jsonStr}")
    responseJson['Data'] = encrypt(jsonStr,config.shuyunInfo['DataSecretIV'],secret)
    #拼接顺序为返回值（Ret）、返回信息（Msg）、参数内容（Data）。
    responseJson['Sig'] = hmacSign(f"{ret}{msg}{responseJson['Data']}",config.shuyunInfo['SigSecret'])
    return responseJson



def test():
    shuyundata={"Data": "Y03KgUvj225kvcvVszQ3HTLzjRsZzj0KZ9PVapvGA1JwmvTuBgH6KPsEvFSHt89h02dCLQniDPoSrHwl4COjkpjS7c+bxLyzoLyqK/2hUMnU6dSOtGS03S2Ns6qIcCEEc44cSOxSZHfrRkc+agE4+a26g6BvJugJOa73x70jwAi5QWv0EnQaPVhRvG01PINWhVp8dP5ztSCwhxUR/6oe0aGrDgzfkuydElTBWKSnkcOGZmOQZD1jOgvx76ZeVibMcQI+UCg9YpfgYgoGzFoPPQ==", "OperatorID": "10004", "TimeStamp": "1690959156", "Sig": "3D45105B17D24F1BB1451D0C6FEAE674", "Seq": "853"}
    a = decocdeMessage(shuyundata)
    print(a)

    print('+'*20)
    print("makeTokenResponse====")
    token = makeTokenResponse()
    print(json.dumps(token,ensure_ascii=False,indent=4))
    
    print('+'*20)
    print("decryptData===DataSecret=")
    print("iv:",config.shuyunInfo['DataSecretIV'])
    print("secret:",config.shuyunInfo['DataSecret'])
    decryptData = decrypt(token['Data'],config.shuyunInfo['DataSecretIV'],config.shuyunInfo['DataSecret'])
    print(decryptData)
    

def decodeTest():
    encodedMsg ='ActIhQ1JwfQv+uR2akHV5p/bes5VnoDKi6y+UyioKynZZA3w5jWDQF5pg6BcI/5mKEpEnEiecfCaPGxhu/B68DwN/dsmAp1OvU3I+DQ4m1I5Zh6RPiMlB2tsQrDHTBjUXWkb7GIhCCCiVzOTcBJ3s+KyAksKNwm4DlVuXZOYJvLRlRhOB15YzjbfhO1Bz8hTK21bJGKPu9XlzP+emh8NugRwLrMahkgBI3xtTqt47o4='
    data = decrypt(encodedMsg,'pJPClgUKoLNyLYQv','w1rTWx7tRK6VMtu0')    
    print("\n Decoded Msg\n",data)

    

    myEncodedMsg = encrypt(data,'pJPClgUKoLNyLYQv','w1rTWx7tRK6VMtu0')
    print("\n myEncodedMsg\n",myEncodedMsg)
    print("\n encodedMsg\n",encodedMsg)
    print("\n \n myEncodedMsg==decodedMsg:",myEncodedMsg==encodedMsg)
    print("\n"*5)
    
if __name__ == '__main__':
    decodeTest()