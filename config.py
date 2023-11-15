
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
        "park_id":"10035698",
        "parkName":"仙居县城北东路人民医院斜对面",
        "address":"仙居东门停车场",
        "address_lal":"120.751084,28.864096",
        "sum_pot":170,
        "use_pot":0
    },
    {
        "park_id":"84488",
        "parkName":"西门公园地下停车场",
        "address":"仙居县环城南路西门公园地下",
        "address_lal":"120.73614,28.853253",
        "sum_pot":200,
        "use_pot":0
    },
    {
        "park_id":"10036032",
        "parkName":"梦家园保障房小区停车场",
        "address":"仙居县泰和北路梦家园小区",
        "address_lal":"120.723703,28.860992",
        "sum_pot":120,
        "use_pot":0
    },
    {
        "park_id":"86371",
        "parkName":"仙居市民公园地下停车场",
        "address":"仙居市民公园地下",
        "address_lal":"120.731635,28.850694",
        "sum_pot":160,
        "use_pot":0
    },
    {
        "park_id":"10045410",
        "parkName":"环城西路城西停车场",
        "address":"仙居环城西路城西菜场内",
        "address_lal":"120.732529,28.860442",
        "sum_pot":100,
        "use_pot":0
    },
]

