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
def makeTokenResponse(ret=0,msg="请求成功",logger=None):
    global tokenCount
    print("makeTokenResponse--------------",tokenCount)
    responseToken = {
                        "SuccStat":0,
                        "FailReason":0,
                        "AccessToken":config.shuyunInfo['token'],
                        "TokenAvailableTime":int(time.time()*1000)+config.waitTime*1000,
                        "OperatorID":config.shuyunInfo['OperatorID'],
                    }
    responseJson = {"Data":"J3OPNG7s6nVbKeCHQVDs0g==","Msg":msg,"Ret":ret,"Sig":"15163CB3D8D950E7E4C4450B2D39A08A"}
    secret = config.shuyunInfo['OperatorSecret']
    if tokenCount%2==1:
        secret = config.shuyunInfo['DataSecret']
    tokenCount+=1
    jsonStr = json.dumps(responseToken,ensure_ascii=False)
    logger.debug(f"makeTokenResponse tokenCount:{tokenCount}\n secret:{secret} \njsonStr:{jsonStr}")
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
    token = {"Data":"rJthjZsDjdsh8ZFtumqzb/P8RyaXJ36Httbs8KiN5gc2gkWYbndQyd6Qsfepr1Mugaz4c4QJXCU9CA3DYimqDCwMHwpS9EKiQgkgeLW71L4NRzWMHkt95/Dn9//pn5vSxGDhOJYOwl8lApx8cs+VYYJZq/mOXhjlP8eKdEaz18NPCbJLJXNwq9UvTHrZUkP0","Msg":"\u8bf7\u6c42\u6210\u529f","Ret":0,"Sig":"4A60886CDB19E2919F3350268E439EEF"}
   
    print('+'*20)
    print("decryptData===OperatorSecret=")
    decryptData = decrypt(token['Data'],config.shuyunInfo['DataSecretIV'],config.shuyunInfo['OperatorSecret'])
    print(decryptData)
    

    print('+'*20)
    print("decryptData===DataSecret=")
    decryptData = decrypt(token['Data'],config.shuyunInfo['DataSecretIV'],config.shuyunInfo['DataSecret'])
    print(decryptData)
    
if __name__ == '__main__':
    test()