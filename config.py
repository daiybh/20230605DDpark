
import platform

port=18086
waitTime=60
sysstr = platform.system()
if(sysstr=="Linux"):
    baseConfigPath='/home/admin/fujianpark/'
elif(sysstr=="Windows"):
    baseConfigPath='./fujianpark/'

parkInfo=[
    {
        "park_id":"10001",
        "parkName":"商都酒店停车场",
        "address":"福建福州",
        "address_lal":"100.00,100.11",
        "sum_pot":50
    },
    {
        "park_id":"10002",
        "parkName":"商都酒店停车场",
        "address":"福建福州",
        "address_lal":"100.00,100.11",
        "sum_pot":50
        
    },
    {
        "park_id":"10003",
        "parkName":"商都酒店停车场",
        "address":"福建福州",
        "address_lal":"100.00,100.11",
        "sum_pot":50
    },
    {
        "park_id":"10004",
        "parkName":"商都酒店停车场",
        "address":"福建福州",
        "address_lal":"100.00,100.11",
        "sum_pot":50
    },
    {
        "park_id":"10005",
        "parkName":"商都酒店停车场",
        "address":"福建福州",
        "address_lal":"100.00,100.11",
        "sum_pot":50
    },
]
