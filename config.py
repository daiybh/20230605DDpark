
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
    'SigSecret':'DE0D64B041DD20CA',
    'token':"MA61WH5Y-X-41DD20CA7EA158C9"
}  

parkyunInfos={
    "10045928":{
       'park_id':10045928,
            'ukey':"D6P94JBBOAPHN7P7" 
    }    
}

jsonPath=baseConfigPath+'config.json'
#load config.json into parkyunInfos
import json
def ReadJson():
    global parkyunInfos
    try:
        f = open(jsonPath, 'r')
        if f:
            parkyunInfos = json.load(f)
            print(parkyunInfos)
            f.close()
            return True
    except Exception as e:
        print(e)
    return False

def writeJson(): 
    global parkyunInfos   
    # write parkyunInfos to config.json
    with open(jsonPath, 'w') as f2:
        json.dump(parkyunInfos, f2,indent=4)  
        f2.close()

import os
if not os.path.exists(baseConfigPath):
    os.makedirs(baseConfigPath)


if ReadJson()==False:
    writeJson()