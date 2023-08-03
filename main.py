from flask import Flask, request,Response,jsonify
import requests
import json
from  threading import Thread,Event
import threading,time
from time import sleep
import logging
from logging.handlers import TimedRotatingFileHandler
import os
import config,shuyun
import parkyun

if not os.path.exists(config.baseConfigPath):
    os.makedirs(config.baseConfigPath)

formatter=logging.Formatter('%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
handler=TimedRotatingFileHandler(filename=f'{config.baseConfigPath}py_record.log',
                                 when='midnight',interval=1,backupCount=10,encoding='utf-8')
handler.setFormatter(formatter)


logging.basicConfig(handlers=[handler],                 
                    level=logging.DEBUG, )

app = Flask(__name__)

app.config['JSON_AS_ASCII'] = False

# "park_id":{"empty_plot":0,"lastUPdateTIme":0}
global_LastInfo={"parkinfo":{},"lastupdate":""}
# Route to handle incoming data from the parking cloud
event= Event()

def update_availablespace_Thread():
    global global_LastInfo    
    while True:
        b = event.wait(config.waitTime)
        if b:
            event.clear()
        
        global_LastInfo['lastupdate'] = time.ctime()
        app.logger.debug(f"update_availablespace_Thread acitve{time.ctime()} {global_LastInfo}")
        for info in global_LastInfo['parkinfo']:
            if info==0:
                continue
            try:
                params={
                    "vendorParkId": info,
                    "uploadTime": int(time.time()*1000),
                    "availableSpace": global_LastInfo['parkinfo'][info]['empty_plot']
                }
                app.logger.debug(f"update_availablespace_Thread acitve{time.ctime()} {params}")
                #aliyunClient.update_availablespace(params)
                global_LastInfo['parkinfo'][info]['lastupdate'] = time.ctime()
            except Exception as e:
                print(e)
                app.logger.error(f"update_availablespace_Thread error:{e}")


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    
@app.route('/shutdown', methods=['GET'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'
 
@app.route('/', methods=['GET'])
def routRoot():
    global global_LastInfo
    b = {"shuyunInfo":config.shuyunInfo,"info":global_LastInfo,"urls":[]}
    for a in app.url_map.iter_rules():
        b['urls'].append(a.rule)
    return jsonify(b)

@app.route('/query_token', methods=['POST'])
def handle_query_token():
    json_body = request.json
    app.logger.debug(f'{request.path},>>>{json.dumps(json_body,ensure_ascii=False)}') 
    a = shuyun.decocdeMessage(json_body)
    if a is None:
        return Response(status=400)
    app.logger.debug(f'{request.path},decocdeMessage data>>>{json.dumps(a,ensure_ascii=False)}')

    responseJson = shuyun.makeTokenResponse()
    return jsonify(responseJson)
    

@app.route('/chargeorder', methods=['POST'])
def handle_chargeorder():
    json_body = request.json
    app.logger.debug(f'{request.path},>>>{json.dumps(json_body,ensure_ascii=False)}')
    a = shuyun.decocdeMessage(json_body)
    if a is None:
        return Response(status=400)
    
    app.logger.debug(f'{request.path},decocdeMessage data>>>{json.dumps(a,ensure_ascii=False)}')

    saleValue = a['saleValue']
    carNumber = a['plateNo']

    orderInfo = parkyun.queryOrder(carNumber)
    app.logger.debug(f'{request.path},queryOrder>>>{json.dumps(orderInfo,ensure_ascii=False)}')
    if orderInfo['state'] ==1:
        discountInfo = parkyun.discountNotice(carNumber,orderInfo['data']['order_id'],saleValue)
        app.logger.debug(f'{request.path},discountNotice>>>{json.dumps(discountInfo,ensure_ascii=False)}')

    responseStatus = {"SuccStat":0,"FailReason":""}
    responseJson = shuyun.make_chargeorde_Repsonse(json.dumps(responseStatus,ensure_ascii=False))
    return jsonify(responseJson)

if __name__ == '__main__':    
    app.run(host='0.0.0.0',port=config.port, debug=False)

