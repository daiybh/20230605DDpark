from flask import Flask, request
import requests
import json
from aliyunClient import AliyunClient
from  threading import Thread,Event
import threading,time
from time import sleep
import logging
from logging.handlers import TimedRotatingFileHandler
import os
import config

if not os.path.exists(config.baseConfigPath):
    os.makedirs(config.baseConfigPath)

formatter=logging.Formatter('%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
handler=TimedRotatingFileHandler(filename=f'{config.baseConfigPath}py_record.log',
                                 when='midnight',interval=1,backupCount=10)
handler.setFormatter(formatter)


logging.basicConfig(
                    handlers=[handler],
                    
                    level=logging.DEBUG, )

app = Flask(__name__)

aliyunClient= AliyunClient(app.logger)

# "park_id":{"empty_plot":0,"lastUPdateTIme":0}
global_LastInfo={}
# Route to handle incoming data from the parking cloud
event= Event()

def update_availablespace_Thread():
    global global_LastInfo    
    while True:
        b = event.wait(20)
        if b:
            event.clear()
        app.logger.debug(f"update_availablespace_Thread acitve{time.ctime()} {global_LastInfo}")
        for info in global_LastInfo:
            try:
                params={
                    "vendorParkId": info,
                    "uploadTime": int(time.time()*1000),
                    "availableSpace": global_LastInfo[info]['empty_plot']
                }
                app.logger.debug(f"update_availablespace_Thread acitve{time.ctime()} {params}")
                aliyunClient.update_availablespace(params)
            except Exception as e:
                print(e)
                app.logger.error(f"update_availablespace_Thread error:{e}")

def handle_createPark(park_id):
    global aliyunClient
    params=config.parkInfo[park_id]
    aliyunClient.CreatePark(params)        
        

@app.route('/out_park', methods=['POST','GET'])  
@app.route('/in_park', methods=['POST','GET']) 
def out_in_park():
    global global_LastInfo    
    json_body = request.json
    
    app.logger.debug(f'{request.path},>>>{json.dumps(json_body)}')
    park_id=json_body['park_id']
    park_id = f"{park_id}"
    if park_id not in global_LastInfo:
        global_LastInfo[park_id]={}
        handle_createPark(park_id)
    global_LastInfo[park_id]['empty_plot']=json_body['data']['empty_plot']
    event.set()
    vendorRecordId=json_body['data']['order_id']
    plateNo=json_body['data']['car_number']
    plateColor="GREEN" if len(plateNo)==7 else "BLUE"
    
    if request.path=='/in_park':
        in_time=json_body['data']['in_time']        
        params={
            "vendorParkId": park_id,
            "vendorRecordId": vendorRecordId,
            "plateNo": plateNo,
            "plateColor": plateColor,
            "inTime":     in_time*1000,
            "inPictureUrl": json_body['data']['pic_addr'],
            "inChannelId": json_body['data']['in_channel_id'],
            "inChannelName": '无'#'入口'+inChannelId
        }      

        aliyunClient.record_enter(params)

    elif request.path=='/out_park':
        params={
           "vendorParkId": park_id,
            "vendorRecordId": vendorRecordId,
            "plateNo": plateNo,
            "plateColor": plateColor,
            "outTime": json_body['data']['out_time']*1000,
            "outPictureUrl": json_body['data']['pic_addr'],
            "outChannelId": json_body['data']['out_channel_id'],
            "outChannelName": '无'#'出口'+outChannelId
        }
        aliyunClient.record_exit(params)


    reuslt={
  "state": 1,
  "order_id": json_body['data']['order_id'],
  "park_id": park_id,
  "service_name": json_body['service_name'],
  "errmsg": " send success!"
}
    return json.dumps(reuslt)

if __name__ == '__main__':
    t1= threading.Thread(target=update_availablespace_Thread).start()
    app.run(host='0.0.0.0',port=config.port, debug=False)
    t1.join()
