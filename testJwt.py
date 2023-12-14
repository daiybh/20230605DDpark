import jwt
import time
import uuid

companyId="d663b502-7ebb-4425-b3f2-1406d7e6edfa"

# 读取RSA私钥

private_key='''-----BEGIN RSA PRIVATE KEY-----
MIICdwIBADANBgkqhkiG9w0BAQEFAASCAmEwggJdAgEAAoGBAK59NiatxtVB6vwG
VtAJp6yMYcfpfx3eeh7kV7PgmkZnOA9UMv5jeDjbyS+Up7tTz0T3R2Aw0LH7YY3e
vC6KNkV/MGGijCWTR2g2Y7ePMrQinlTh+AmYGHRxArGIf9SKSPBQg1bFNlPbU9x2
uvqJHl7oG/lxxqPp8Z6ohp31OOHTAgMBAAECgYEAgyAxa4u4Glb5IgAZiSlYSkEM
0lDUaDvihgiPJ+wnw7SZ2lsqHyXdGM2COTF7gzkOUAOMLetBSh9hRl4WCNtwwDaJ
NoqcSZ9DTbPLOEm90nEEB2ghT9XhWNBjOMrUXiajLcRTZKWzw8gxubOl6p3G2yEI
YC2ge+Oo2+h5KUFbmjECQQDlQRynx+2yMI8lL6CActYJKMjh4ioNIxRwJosDWHlc
Ia16vscDbZpBfqVsXYxvSyG1BLPl/x3xCYMuJHastY5XAkEAwth8gVPDolr3rXMc
HY1/kJgcdiNTY5KRgpyKv0LRMJQ//+AwW670xlnQ1LP+5ak8GSKDhs6DDN+VvN7K
sb8i5QJAAYAsnNiNMMZqmXa3WT/nMMYoknn1hoJ9RsKp1ErG+Jhr10raaKZWBSm8
EXqHSc83GEVAnDfQTVyflDS+5iCGHwJARD2f9YeJyA4GGshq+2q4V8L+jN24cfI+
Zjk/Wtci/tmdRJeXODUhY2rHegeEaZkJBGCTIh6nxVV1Uw3QfcpMhQJBAKpFe7lY
IyJXu+FT/hyXxGjy9pFtif4zCTe0y33JP1YTFblMid3gV/maauR83C+StoerjzFV
ZeNq4DkaK2Kr0pU=
-----END RSA PRIVATE KEY-----'''


with open('./privateKey.pem', 'r') as f:
    private_key = f.read()


def getToken():
  payload={
    "companyId": companyId,
    "iat": int(time.time()),
    "jti": str(uuid.uuid4())
  }
  header={
    "alg": "RS256"
  }
  print(payload)
  # 生成JWT令牌
  token = jwt.encode(payload, private_key,headers=header, algorithm='RS256')

  print(token)
  return token




def postTo(plateNumber):
  url="https://www.zjxclcyy.com/extension/open-api/bayonet/car-inout/record"

  playload={
  "companyCode":companyId,
  "plateNumber":plateNumber,
  "inoutType": "0",
    "deviceId": "test",
    "deviceName": "测试"
  }
  print(playload)
  headers = {
      "Authorization": "Bearer "+getToken()
  }
  import requests

  x = requests.post(url,json=playload,headers=headers)

  print(x)
  print("code",x.status_code)
  pj = x.json()
  return pj['code']


postTo('川A12345')
