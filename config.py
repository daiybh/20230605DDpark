
import platform

port=18088
waitTime=60
sysstr = platform.system()
if(sysstr=="Linux"):
    baseConfigPath='/home/admin/zjhuagong/'
elif(sysstr=="Windows"):
    baseConfigPath='./zjhuagong/'


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



#with open('./privateKey.pem', 'r') as f:
#    private_key = f.read()

import parkInfo

parkInfo = parkInfo.parkInfo