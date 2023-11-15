from flask import Flask, request,Response,jsonify
import requests
import json

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
app.config['JSON_AS_ASCII'] = False


# "park_id":{"empty_plot":0,"lastUPdateTIme":0}
global_LastInfo={"parkinfo":{},"lastupdate":""}
global_Parkinfo=config.parkInfo
# Route to handle incoming data from the parking cloud
event= Event()

    

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
    global global_Parkinfo
    b = {"info":global_LastInfo,"urls":[]}
    for a in app.url_map.iter_rules():
        b['urls'].append(a.rule)
    b["parkinfo"]=global_Parkinfo
    
    return jsonify(b)

@app.route('/api/getPots', methods=['GET'])
def get_mutil_potinfo():

    service_name=request.args.get('service_name')
    Pot_id=request.args.get('pot_id')

    if service_name!="Select_pot":
        return jsonify({"state":0,"errmsg":"service_name error"})
    if Pot_id!="DL2023115":
        return jsonify({"state":0,"errmsg":"pot_id error"})

    global global_LastInfo
    global global_Parkinfo

    global_LastInfo['lastupdate']=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    result={
        "state":1,
        "errmsg":"",
        "data":[]
    }
    for parkinfo in global_Parkinfo:
        park_id=parkinfo['park_id']
        print(park_id)
        if park_id  in global_LastInfo['parkinfo']:   
            parkinfo['use_pot']=global_LastInfo['parkinfo'][park_id]['empty_plot']
            time_str = global_LastInfo['parkinfo'][park_id]['lastUPdateTime']
            format_str = "%Y-%m-%d %H:%M:%S"

            timestamp = int(time.mktime(time.strptime(time_str, format_str)))
            parkinfo['uptime']=    timestamp
        result['data'].append(parkinfo)

    return jsonify(result)

@app.route('/outpark', methods=['POST','GET'])  
@app.route('/inpark', methods=['POST','GET']) 
def out_in_park():
    global global_LastInfo    
    json_body = request.json
    
    app.logger.debug(f'{request.path},>>>{json.dumps(json_body)}')
    park_id=json_body['park_id']    
    if park_id not in global_LastInfo['parkinfo']:
        global_LastInfo['parkinfo'][park_id]={}
        
    global_LastInfo['parkinfo'][park_id]['empty_plot']=json_body['data']['empty_plot']
    global_LastInfo['parkinfo'][park_id]['lastrecv']=json_body
    global_LastInfo['parkinfo'][park_id]['lastUPdateTime']=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

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
    app.run(host='0.0.0.0',port=config.port, debug=False)
    
