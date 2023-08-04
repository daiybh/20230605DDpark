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



def queryOrder(car_number,park_id):
    url = "http://istparking.sciseetech.com/public/order/queryOrder"
    query_time=int(time.time())
    payload = {"service_name":"query_order",
               "sign":"3FF85B6DD886F11A19484525F45253EA",
               "park_id":park_id,
               "data":{"car_number":car_number,"query_time":query_time}
               }
     
    payload["sign"] = makeSign(payload,parkid=park_id) 
    headers = {"content-type": "application/json"}
    response = requests.request("POST", url, json=payload, headers=headers)
    return response.json()



def discountNotice(car_number,parkId,order_id,saleValue):
    #下发优惠信息
    #URL如下
    #http://istparking.sciseetech.com/public/charge/discountNotice
    #阿里云向停车云下发优惠信息

    url='http://istparking.sciseetech.com/public/charge/discountNotice'
    payload ={
            "service_name": "charge_discount_notice",
            "sign": "60B6FB3106DE9EB45D0CA01BDA0DE160",
            "park_id": parkId,
            "data": 
                {
                    "car_number": car_number,
                    "order_id": order_id,
                    "reduce_amount": 8.0,
                    "deduction_time": 4,
                    "deduction_money": 5,
                    "duration": saleValue,
                    "remark": "remark",
                    "start_charging_time": "2020-08-27 00:02:09",
                    "stop_charging_time": "2020-08-27 00:25:07",
                    "uuid": "de6c26a945c9478295d7cffa7631d7f9"
                }
            }
    payload["sign"] = makeSign(payload,parkid=parkId) 
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