import requests
import config
import json
import time
import hashlib

def makeSign(payload,parkid):
    dataS =json.dumps( payload["data"] , separators=(',', ':'),ensure_ascii=False)
    
    data = dataS + "key=" + config.parkyunInfos[parkid]['ukey']
    
    newSign=hashlib.md5(data.encode('utf-8')).hexdigest().upper()
    return newSign

def test():
    a = '{"car_number":"浙AB19097","query_time":1672129283}'
    b = makeSign(a,'10045928')
    print(b)



def queryOrder(logger,car_number,park_id):
    url = "http://istparking.sciseetech.com/public/order/queryOrder"
    query_time=int(time.time())
    payload = {"service_name":"query_order",
               "sign":"3FF85B6DD886F11A19484525F45253EA",
               "park_id":park_id,
               "data":{"car_number":car_number,"query_time":query_time}
               }
     
    payload["sign"] = makeSign(payload,parkid=park_id) 
    logger.debug(f'queryOrder payload >>{payload}')
    headers = {"content-type": "application/json"}
    response = requests.request("POST", url, json=payload, headers=headers)
    return response.json()



def discountNotice(logger,order_id,shuyunJson):
    #下发优惠信息
    #URL如下
    #http://istparking.sciseetech.com/public/charge/discountNotice
    #阿里云向停车云下发优惠信息
 
 #>{"orderNo": "MA005DBW1230809062617020720", 
 # "plateNo": "浙ABP9387", 
 # "saleType": "1", 
 # "saleValue": "120", 
 # "startTime": "2023-08-09 06:26:16", 
 # "endTime": "2023-08-09 07:20:18", 
 # "parkId": "10045928"}
    url='http://istparking.sciseetech.com/public/charge/discountNotice'
    payload ={
            "service_name": "charge_discount_notice",
            "sign": "60B6FB3106DE9EB45D0CA01BDA0DE160",
            "park_id": shuyunJson['parkId'],
            "data": 
                {
                    "car_number": shuyunJson['plateNo'],
                    "order_id": order_id,
                    "reduce_amount": 0,
                    "deduction_time": 0,
                    "deduction_money": 0,
                    "duration": shuyunJson['saleValue'],
                    "remark": "remark",
                    "start_charging_time": shuyunJson['startTime'],
                    "stop_charging_time": shuyunJson['endTime'],
                    "uuid": shuyunJson['orderNo']
                }
            }
    payload["sign"] = makeSign(payload,parkid=shuyunJson['parkId']) 
    logger.debug(f'discountNotice payload >>{payload}')
    headers = {"content-type": "application/json"}
    response = requests.request("POST", url, json=payload, headers=headers)
    return response.json()



def testchargeorder(car_number,saleValue):
    park_id = '10045928'
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