from flask import Flask, request,Response,jsonify
from flask_restful import Api,Resource
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



formatter=logging.Formatter('%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
handler=TimedRotatingFileHandler(filename=f'{config.baseConfigPath}py_record.log',
                                 when='midnight',interval=1,backupCount=10,encoding='utf-8')
handler.setFormatter(formatter)


logging.basicConfig(handlers=[handler],                 
                    level=logging.DEBUG, )

app = Flask(__name__)

app.config['JSON_AS_ASCII'] = False

# "park_id":{"empty_plot":0,"lastUPdateTIme":0}
global_LastInfo={"parkinfo":{},"last_handle_query_token":{"json":{},"time":0},"last_handle_chargeorder":{"json":{},"time":0}}
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
    b = {"shuyunInfo":config.shuyunInfo,"info":global_LastInfo,"urls":[]}
    for a in app.url_map.iter_rules():
        b['urls'].append(a.rule)
    return jsonify(b)

@app.route('/query_token', methods=['POST'])
def handle_query_token():
    json_body = request.json
    app.logger.debug(f'{request.path},>>>{json.dumps(json_body,ensure_ascii=False)}') 
    retJson,message = shuyun.decocdeMessage(json_body)
    ret =1
    if retJson is None:
        app.logger.debug(f'{request.path},decocdeMessage failed>>>{message}')
    else:
        global global_LastInfo
        global_LastInfo['last_handle_query_token']['json'] = retJson
        global_LastInfo['last_handle_query_token']['time'] = time.time()
        ret =0
        app.logger.debug(f'{request.path},decocdeMessage data>>>{json.dumps(retJson,ensure_ascii=False)}')
    responseJson = shuyun.makeTokenResponse(ret,message,app.logger)
    app.logger.debug(f'{request.path},responseJson>>>{json.dumps(responseJson,ensure_ascii=False)}')
    return jsonify(responseJson)
    

@app.route('/chargeorder', methods=['POST'])
def handle_chargeorder():
    auth = request.authorization
    ret =1
    message=""
    if not auth or auth.type!='bearer'  or auth.token!=config.shuyunInfo['token']:
        message="Unauthorized"
    else:    
        
        json_body = request.get_json()
        app.logger.debug(f'{request.path},>>>{json.dumps(json_body,ensure_ascii=False)}')
#{"Data": "Y03KgUvj225kvcvVszQ3HTLzjRsZzj0KZ9PVapvGA1JwmvTuBgH6KPsEvFSHt89h02dCLQniDPoSrHwl4COjkpjS7c+bxLyzoLyqK/2hUMnU6dSOtGS03S2Ns6qIcCEEc44cSOxSZHfrRkc+agE4+a26g6BvJugJOa73x70jwAi5QWv0EnQaPVhRvG01PINWhVp8dP5ztSCwhxUR/6oe0aGrDgzfkuydElTBWKSnkcOGZmOQZD1jOgvx76ZeVibMcQI+UCg9YpfgYgoGzFoPPQ==", "OperatorID": "10004", "TimeStamp": "1691039453", "Sig": "3B10EFC59AA7395F94B3E38BBA162CFD", "Seq": "107"}

        a,message = shuyun.decocdeMessage(json_body)
        if a is None:
            app.logger.debug(f'{request.path},decocdeMessage failed>>>{message}')
        else:
            ret =0
            global_LastInfo['last_handle_chargeorder']['json'] = a
            global_LastInfo['last_handle_chargeorder']['time'] = time.time()
            app.logger.debug(f'{request.path},decocdeMessage data>>>{json.dumps(a,ensure_ascii=False)}')
#{"parkId": "10045928", "endTime": "2023-02-16 15:37:05", "orderNo": "MA005DBW1230216153336221729", "plateNo": "沪A66609", "saleType": 120, "saleValue": 120, "startTime": "2023-02-16 15:33:36"}
            saleValue = a['saleValue']
            carNumber = a['plateNo']
            parkId = a['parkId']

            orderInfo = parkyun.queryOrder(carNumber,parkId)
            app.logger.debug(f'{request.path},queryOrder>>>{json.dumps(orderInfo,ensure_ascii=False)}')
            if orderInfo['state'] ==1:
                discountInfo = parkyun.discountNotice(carNumber,parkId,orderInfo['data']['order_id'],saleValue)
                app.logger.debug(f'{request.path},discountNotice>>>{json.dumps(discountInfo,ensure_ascii=False)}')

    responseStatus = {"SuccStat":0,"FailReason":""}
    responseJson = shuyun.make_chargeorde_Repsonse(json.dumps(responseStatus,ensure_ascii=False),ret,message)
    return jsonify(responseJson)

@app.route('/all', methods=['GET'])
def handle_infos():
    try:            
        shuyun =config.shuyunInfo       
        response=f'<section> <section><div><h1>shuyun</h1><ul>'        
        for k in shuyun:
            #formHtml=f'''<input type="submit" value="delete" onclick="deleteLed({row[0]})">'''
            print(k,shuyun[k])
            response +=f'''<li>{k}:'''+shuyun[k]+'</li>'
        response+='</ul></div></section>'
        response+='<section><div>" " </div></section>'
        parkinfos = config.parkyunInfos
        response+='<section><div><h1>Parks</h1><ul>'
        for row in parkinfos:  
            formHtml=f'''<input type="submit" value="delete" onclick="deletepark({row})">'''          
            response +='<li>'+formHtml+str(row)+'</li>'
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
            <section>
                <div><h1>ADD parks </h1>
                <form  onsubmit = "return setparkAction(this)" method="POST">	
                <p>Park id: <input type = "text" name = "park_id" />
                <p>ukey   : <input type = "text" name = "ukey" />
                <input type="text" name="actiontype" value="add" hidden>
                <p><input type = "submit" value = "Add" />
                </form>
                </div>
            </section>
            <section>
                <div><h1>update parks </h1>
                <form  onsubmit = "return setparkAction(this)" method="POST">	
                <p>Park id: <input type = "text" name = "park_id" />
                <p>ukey   : <input type = "text" name = "ukey" />
                <input type="text" name="actiontype" value="update" hidden>
                <p><input type = "submit" value = "update" />
                </form>
                </div>
            </section>       
        </section>
        ''';

        rHtml+=f'''<p>{response}</p>            </body>            </html>'''
        resp = Response(rHtml,mimetype='text/html')
        return resp
    except Exception as e:
        print(e)
        return str(e)
 

class ParkInfo(Resource):
    def get(self,park_id):
        try:
            response=f'{park_id}\n'
            parkinfo = config.parkyunInfos.get(str(park_id))
            if parkinfo is None:
                response +='not found'
            else:
                return jsonify(parkinfo)
            return response
        except Exception as e:
            print(e)
            return str(e)
        
    def post(self,park_id):
        try:
            ukey = request.values['ukey']             

            if request.values['actiontype']=='add': 
                config.parkyunInfos[str(park_id)]={'park_id':park_id,'ukey':ukey }
                config.writeJson()    

            elif request.values['actiontype']=='update':
                config.parkyunInfos[str(park_id)]={'park_id':park_id,'ukey':ukey }
                config.writeJson() 
            return 'ok'
        except Exception as e:
            print(e)
            return str(e)
    def delete(self,park_id):
        try:            
            parkinfo = config.parkyunInfos.get(str(park_id))
            if parkinfo is not None:
                config.parkyunInfos.pop(str(park_id))
                config.writeJson()
            return 'ok'
        except Exception as e:
            print(e)
            return str(e)


api = Api(app)
api.add_resource(ParkInfo, '/api/parkinfo/<int:park_id>')
    

if __name__ == '__main__':    
    app.run(host='0.0.0.0',port=config.port, debug=False)

