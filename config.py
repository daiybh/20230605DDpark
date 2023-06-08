
import platform

port=18081
waitTime=60
sysstr = platform.system()
if(sysstr=="Linux"):
    baseConfigPath='/home/admin/tenzhoupark/'
elif(sysstr=="Windows"):
    baseConfigPath='./tenzhoupark/'

aliyun={
        "host":"https://api.link.aliyun.com",
        "app_id":"your appId",
    "app_key":"34396617",
    "app_secret":"4be931e6b7635cd5e03ef19d6b4f8ddb"
}

parkInfo={
    "10044380":{
        "vendorParkId": "10044380",
        "parkName":"商都酒店停车场",
        "address":"山东省枣庄市滕州市杏坛路7号",
        "longitude":120.367013,
        "latitude":31.492141,
        "totalSpace":50,
        "parkEstateType":"PUBLIC_PARKING",
        "parkBusinessType":"OFFICE_BUILDING",
        "pictureUrls":["http://aliyun.com/parking.jpg"]
    }
}
