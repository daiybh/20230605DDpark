import requests
import config
import json
import time
import hashlib

def makeSign(payload,car_number):
    dataS =json.dumps( payload["data"] , separators=(',', ':'))
    payload["data"]["car_number"] = car_number 
    data = dataS.replace("#CAR_NUMBER#", car_number) + "key=" + config.parkyunInfo['ukey']
    
    newSign=hashlib.md5(data.encode('utf-8')).hexdigest().upper()
    return newSign

def test():
    a = '{"car_number":"浙AB19097","query_time":1672129283}'
    b = makeSign(a)
    print(b)



def queryOrder(car_number):
    url = "http://istparking.sciseetech.com/public/order/queryOrder"
    query_time=int(time.time())
    payload = {"service_name":"query_order",
               "sign":"3FF85B6DD886F11A19484525F45253EA",
               "park_id":10045928,
               "data":{"car_number":"#CAR_NUMBER#","query_time":query_time}
               }
     
    payload["sign"] = makeSign(payload,car_number)  

    payload['park_id']=config.parkyunInfo['park_id']

    print(payload)
    headers = {"content-type": "application/json"}

    response = requests.request("POST", url, json=payload, headers=headers)

    return response.json()



def discountNotice(car_number,order_id,saleValue):
    #下发优惠信息
    #URL如下
    #http://istparking.sciseetech.com/public/charge/discountNotice
    #阿里云向停车云下发优惠信息

    url='http://istparking.sciseetech.com/public/charge/discountNotice'
    payload ={
            "service_name": "charge_discount_notice",
            "sign": "60B6FB3106DE9EB45D0CA01BDA0DE160",
            "park_id": 30148,
            "data": 
                {
                    "car_number": "#CAR_NUMBER#",
                    "order_id": "1082774902",
                    "reduce_amount": 8.0,
                    "deduction_time": 4,
                    "deduction_money": 5,
                    "duration": 20,
                    "remark": "remark",
                    "start_charging_time": "2020-08-27 00:02:09",
                    "stop_charging_time": "2020-08-27 00:25:07",
                    "uuid": "de6c26a945c9478295d7cffa7631d7f9"
                }
            }
    payload["data"]["order_id"] = order_id
    payload["data"]["duration"] = saleValue
    payload["sign"] = makeSign(payload,car_number)  

    payload['park_id']=config.parkyunInfo['park_id']


    headers = {"content-type": "application/json"}

    response = requests.request("POST", url, json=payload, headers=headers)

    return response.json()



def testchargeorder(car_number,saleValue):
    orderInfo = queryOrder(car_number)
    print(orderInfo)
    if orderInfo['state'] !=1:
        return False
    discountInfo = discountNotice(car_number,orderInfo['data']['order_id'],saleValue)
    print(discountInfo)
    if discountInfo['state'] !=1:
        return False
    return True

    
if __name__ == '__main__':
    #test()
    testchargeorder('浙AB19097',20)