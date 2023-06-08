
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
    "app_key":"34380523",
    "app_secret":"481d28007527e7d91a5dd963591dd0da"
}

parkInfo={
    "10044380":{
        "vendorParkId": "10044380",
        "parkName":"商都酒店停车场",
        "address":"山东省枣庄市滕州市杏坛路7号",
        "longitude":117.16,
        "latitude":35.09,
        "totalSpace":50,
        "parkEstateType":"PUBLIC_PARKING",
        "parkBusinessType":"OFFICE_BUILDING",
        "pictureUrls":["http://aliyun.com/parking.jpg"]
    }
}
