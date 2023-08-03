
import platform

port=18085
waitTime=60
sysstr = platform.system()
if(sysstr=="Linux"):
    baseConfigPath='/home/admin/shuyunPark/'
elif(sysstr=="Windows"):
    baseConfigPath='./shuyunPark/'

shuyunInfo={
    'OperatorID':'MA61WH5Y-X',
    'OperatorSecret':'41DD20CA7EA158C9',
    'DataSecret':'7EA158C99079009A',
    'DataSecretIV':'8602818628180248',
    'SigSecret':'DE0D64B041DD20CA'
}  

parkyunInfo={
    'park_id':10045928,
    'ukey':"D6P94JBBOAPHN7P7"
}