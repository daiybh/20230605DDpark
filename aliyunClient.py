# -*- coding: utf-8 -*-

import sys
import os
curPath =os.path.split(__file__)[0]

sys.path.append(fr"{curPath}/api-gateway-demo-sign-python/aliyun-api-gateway-demo-sign3/")

from com.aliyun.api.gateway.sdk import client
from com.aliyun.api.gateway.sdk.http import request
from com.aliyun.api.gateway.sdk.common import constant

import config
import json
import time
import uuid
import logging

class AliyunClient:
    def __init__(self,Logger):
        self.cli = client.DefaultClient(app_key=config.aliyun["app_key"], app_secret=config.aliyun["app_secret"])
        self.logger= Logger
    
    def generate_uuid(slef):
        return str(uuid.uuid4())
    def _createbody(self,params):
        return {
            "id":self.generate_uuid(),              
            "params":params,
            "request":{
                "apiVer":"1.0.0"
            },
            "version":"1.0"
        }

    def _doRequest(self,url,params):
        try:
            body = self._createbody(params)        
            req_post = request.Request(host=config.aliyun["host"], protocol=constant.HTTPS, url=url, method="POST", time_out=30000)
            req_post.set_body(bytearray(source=json.dumps(body), encoding="utf8"))
            req_post.set_content_type(constant.CONTENT_TYPE_STREAM)
            status,_,responseText = self.cli.execute(req_post)
            a = json.loads(responseText)
            if a['code'] == 200:
                return True,a
            
        except Exception as e:
            print(e)
            self.logger.error(f"error:{e}")

        self.logger.error(f"_doRequest url:{url}")
        self.logger.error(f"_doRequest body:{json.dumps(body)}")
        self.logger.error(f"response:{status} {responseText}")
        self.logger.error(f"response json:{json.dumps(a)}")
        
        return False,a
        

    def CreatePark(self,params):
        ''' 
        params={
                "vendorParkId": "p23734375693",
                "parkName": "天鹅座停车场",
                "address": "无锡市新吴区净慧东路96号",
                "longitude": 120.367013,
                "latitude": 31.492141,
                "totalSpace": 100,
                "parkEstateType": "PUBLIC_PARKING",
                "parkBusinessType": "OFFICE_BUILDING",
                "pictureUrls": ["http://aliyun.com/parking.jpg"],
            }       
        '''
        url = "/park/isv/v1/park/create"
        ret,b=self._doRequest(url,params)
        if ret==False and b['code']==50852:
            self.update_park(params)
            

    def update_park(self,params):        
        url = "/park/isv/v1/park/update"
        self._doRequest(url,params)

    def update_availablespace(self,params):
        '''
        params={
                "vendorParkId": "2947297626687",
            "uploadTime": 1550030400000,
            "availableSpaces": 99
            }        
        
        '''
        url = "/park/isv/v1/park/availablespace/update"    
        return self._doRequest(url,params)

    def record_enter(self,params):
        '''params={
            "vendorParkId": "2947297626687",
            "vendorRecordId": "R20200218135602565",
            "plateNo": "苏B11111",
            "plateColor": "BLUE",
            "inTime": 1550030400000,
            "inPictureUrl": "http://aliyun.com/parking.jpg",
            "inChannelId": "C19008934",
            "inChannelName": "天鹅座东门入口"
        }'''   

        url = "/park/isv/v1/park/record/enter"    
        
        return self._doRequest(url,params)

    def record_exit(self,params):   
        '''
        params={
            "vendorParkId": "2947297626687",
            "vendorRecordId": "R20200218135602565",
            "plateNo": "苏B11111",
            "plateColor": "BLUE",
            "outTime": 1550030400000,
            "outPictureUrl": "http://aliyun.com/parking.jpg",
            "outChannelId": "C19008934",
            "outChannelName": "天鹅座东门出口"
        } '''    
        
        url = "/park/isv/v1/park/record/depart"  
        return self._doRequest(url,params)


if __name__ == '__main__':
    aliyun = AliyunClient()
    print("create park")
    aliyun.CreatePark(config.parkInfo['10044380'])
    print("\n")
    print("update availablespace")
    params={
                "vendorParkId": "10044380",
            "uploadTime": 1550030400000,
            "availableSpace": 99
            }   
    aliyun.update_availablespace(params)
    print("\n")
    print("record enter")
    vendorRecordId = f"R{time.strftime('%Y%m%d%H%M%S000', time.gmtime())}"
    params={
            "vendorParkId": "10044380",
            "vendorRecordId": vendorRecordId,
            "plateNo": "苏B11111",
            "plateColor": "BLUE",
            "inTime": 1550030400000,
            "inPictureUrl": "http://aliyun.com/parking.jpg",
            "inChannelId": "C19008934",
            "inChannelName": "天鹅座东门入口"
        }
    params={
   "vendorParkId":10044380,
   "vendorRecordId":"529545B01F3311E8_1686124978",
   "plateNo":"鲁DZX738",
   "plateColor":"green",
   "inTime":1686124978,
   "inPictureUrl":"http: //ist-falcon.oss-cn-shenzhen.aliyuncs.com/order-images/10044380/in/529545B01F3311E8_1686124978.jpg?Expires=1686211390&OSSAccessKeyId=LTAIQQrl6GICP0QX&Signature=4B0RK3akXu7ZybkriQwFTBG6PV4%3D",
   "inChannelId":"camera_529545B01F3311E8C2381565",
   "inChannelName":"无"
    }
    
    aliyun.record_enter(params)
    print("\n")
    print("record exit")
    params={
            "vendorParkId": "10044380",
            "vendorRecordId": vendorRecordId,
            "plateNo": "苏B11111",
            "plateColor": "BLUE",
            "outTime": 1550030400000,
            "outPictureUrl": "http://aliyun.com/parking.jpg",
            "outChannelId": "C19008934",
            "outChannelName": "天鹅座东门出口"
        } 
    params={
   "vendorParkId":"10044380",
   "vendorRecordId":"529545B01F3311E8_1686114162",
   "plateNo":"鲁DUL333",
   "plateColor":"GREEN",
   "outTime":1686125411000,
   "outPictureUrl":"http://ist-falcon.oss-cn-shenzhen.aliyuncs.com/order-images/10044380/out/529545B01F3311E8_1686114162.jpg?Expires=1686211857&OSSAccessKeyId=LTAIQQrl6GICP0QX&Signature=aLg6B%2F%2FIYMJVEODTRXxho91KG7Y%3D",
   "outChannelId":"camera_EBF427CBC68A5C93F7586E3D",
   "outChannelName":"无"
}
    aliyun.record_exit(params)
    print("\n******OVER*******\n")