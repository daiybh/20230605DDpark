from flask import Flask, request,Response,jsonify
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


logging.basicConfig(handlers=[handler],                 
                    level=logging.DEBUG, )

app = Flask(__name__)

aliyunClient= AliyunClient(app.logger)

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
                aliyunClient.update_availablespace(params)
                global_LastInfo['parkinfo'][info]['lastupdate'] = time.ctime()
            except Exception as e:
                print(e)
                app.logger.error(f"update_availablespace_Thread error:{e}")

def handle_createPark(park_id):
    global aliyunClient
    params=config.parkInfo[park_id]
    aliyunClient.CreatePark(params)        

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
    b = {"info":global_LastInfo,"urls":[]}
    for a in app.url_map.iter_rules():
        b['urls'].append(a.rule)
    return jsonify(b)

@app.route('/out_park', methods=['POST','GET'])  
@app.route('/in_park', methods=['POST','GET']) 
def out_in_park():
    global global_LastInfo    
    json_body = request.json
    
    app.logger.debug(f'{request.path},>>>{json.dumps(json_body)}')
    park_id=json_body['park_id']
    park_id = f"{park_id}"
    if park_id not in global_LastInfo['parkinfo']:
        global_LastInfo['parkinfo'][park_id]={}
        handle_createPark(park_id)
    global_LastInfo['parkinfo'][park_id]['empty_plot']=json_body['data']['empty_plot']
    global_LastInfo['parkinfo'][park_id]['lastrecv']=json_body
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

        code,responseJson=aliyunClient.record_enter(params)

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
        code,responseJson=aliyunClient.record_exit(params)

    global_LastInfo['parkinfo'][park_id]['lastresponseFromAliyun']={'code':code,'response':responseJson}


    reuslt={
  "state": 1,
  "order_id": json_body['data']['order_id'],
  "park_id": park_id,
  "service_name": json_body['service_name'],
  "errmsg": " send success!"
}
    return jsonify(reuslt)


@app.route('/all', methods=['GET'])
def handle_led_infos():
    try:            
        response=''
        #parkinfos = query_db('''select park_id,park_name,pgmfilepath from parkinfo;''')
        response+='<section><div><h1>Parks</h1><ul>'
        for v,k in config.parkInfo.items():  
            formHtml=f'''<input type="submit" value="delete" onclick="deletepark({v})">'''          
            response +=f'<li>{formHtml}{k}</li>'
        response+='</ul></div></section></section>'

        rHtml='''            
        <html>
        <script>
         function setparkAction(form){
                form.action = "/api/parkinfo/"+form.park_id.value;
                fetch(form.action, {method:'post', body: new FormData(form)})
            .then(() =>{
            window.location.reload();
            } );
            return false;
            }       

        function deletepark(parkid){
            let deleteurl = "/api/parkinfo/"+parkid;
            fetch(deleteurl, {method: "DELETE"})
            .then(() =>{
            window.location.reload();
            } );
        }

        </script>
        <link rel="stylesheet" href="https://unpkg.com/mvp.css@1.12/mvp.css"> 
        <body>        
        <section>
            <div><h1>ADD Parks </h1>
            <form enctype = "multipart/form-data" onsubmit = "return setparkAction(this)" method="POST">	
                <p>Park Name: <input type = "text" name = "park_name" /></p>
                <p>Park id: <input type = "text" name = "park_id" /></p>
                <p>pgm File: <input type = "file" name = "file" /></p>
                <input type="text" name="actiontype" value="add" hidden>	
                <p><input type = "submit" value = "Add" /></p>
            </form>
            </div>
        </section>
        ''';

        rHtml+=f'''<p>{response}</p>            </body>            </html>'''
        resp = Response(rHtml,mimetype='text/html')
        return resp
    except Exception as e:
        print(e)
        return str(e)
  
@app.route('/createpark', methods=['GET'])
def Acreatepark():
    global aliyunClient
    global global_LastInfo 
    r={}
    for park_id in global_LastInfo['parkinfo']:
        if park_id==0:
            continue
        params=config.parkInfo[park_id]
        a,b= aliyunClient.CreatePark(params)
        r.append(b)
    return jsonify(r)

  
if __name__ == '__main__':
    t1= threading.Thread(target=update_availablespace_Thread).start()
    app.run(host='0.0.0.0',port=config.port, debug=False)
    t1.join()
