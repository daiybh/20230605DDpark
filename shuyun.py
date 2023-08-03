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
        print("OperatorID not in message")
        return None
    if 'Data' not in message:
        print("Data not in message")
        return None
    if 'TimeStamp' not in message:
        print("TimeStamp not in message")
        return None
    if 'Sig' not in message:
        print("Sig not in message")
        return None
    if 'Seq' not in message:
        print("Seq not in message")
        return None
    
    try:
        data = decrypt(message['Data'],config.shuyunInfo['DataSecretIV'],config.shuyunInfo['DataSecret'])        
        sig = hmacSign(f"{message['OperatorID']}{message['Data']}{message['TimeStamp']}{message['Seq']}",config.shuyunInfo['SigSecret'])
        if sig != message['Sig']:
            print("sig not match")
            return None
        apos = data.rfind("}")
        dataA=data[:apos+1]
        return json.loads(dataA)
    except Exception as e:
        print(f"decocdeMessage error:{e}")
        #app.logger.error(f"decocdeMessage error:{e}")
        return None

def make_chargeorde_Repsonse(dataJson,ret=0,msg="请求成功"):
    responseJson = {"Data":"J3OPNG7s6nVbKeCHQVDs0g==","Msg":msg,"Ret":ret,"Sig":"15163CB3D8D950E7E4C4450B2D39A08A"}
    responseJson['Data'] = encrypt(dataJson,config.shuyunInfo['DataSecretIV'],config.shuyunInfo['DataSecret'])
    #拼接顺序为返回值（Ret）、返回信息（Msg）、参数内容（Data）。
    responseJson['Sig'] = hmacSign(f"{ret}{msg}{responseJson['Data']}",config.shuyunInfo['SigSecret'])
    return responseJson

def makeTokenResponse(ret=0,msg="请求成功"):
    print("makeTokenResponse--------------")
    responseStatus = {"SuccStat":0,"FailReason":0,
                    "Token":config.shuyunInfo['OperatorID'],
                    "TokenAvailableTime":int(time.time()*1000)+config.waitTime*1000,
                    "OperatorID":config.shuyunInfo['OperatorID'],
                    }
    responseJson = {"Data":"J3OPNG7s6nVbKeCHQVDs0g==","Msg":msg,"Ret":ret,"Sig":"15163CB3D8D950E7E4C4450B2D39A08A"}
    responseJson['Data'] = encrypt(responseStatus.dumps(responseStatus,ensure_ascii=False),config.shuyunInfo['DataSecretIV'],config.shuyunInfo['OperatorSecret'])
    #拼接顺序为返回值（Ret）、返回信息（Msg）、参数内容（Data）。
    responseJson['Sig'] = hmacSign(f"{ret}{msg}{responseJson['Data']}",config.shuyunInfo['SigSecret'])
    return responseJson



def test():
    shuyundata={"Data": "Y03KgUvj225kvcvVszQ3HTLzjRsZzj0KZ9PVapvGA1JwmvTuBgH6KPsEvFSHt89h02dCLQniDPoSrHwl4COjkpjS7c+bxLyzoLyqK/2hUMnU6dSOtGS03S2Ns6qIcCEEc44cSOxSZHfrRkc+agE4+a26g6BvJugJOa73x70jwAi5QWv0EnQaPVhRvG01PINWhVp8dP5ztSCwhxUR/6oe0aGrDgzfkuydElTBWKSnkcOGZmOQZD1jOgvx76ZeVibMcQI+UCg9YpfgYgoGzFoPPQ==", "OperatorID": "10004", "TimeStamp": "1690959156", "Sig": "3D45105B17D24F1BB1451D0C6FEAE674", "Seq": "853"}
    a = decocdeMessage(shuyundata)
    print(a)

    makeTokenResponse()
    
if __name__ == '__main__':
    test()