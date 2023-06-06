1. 【滕州停车云】host:api.link.aliyun.com

2. DDPark 启动时创建（注册）停车场 https://iotcity.yuque.com/iotcity/park/holfl9?singleDoc#uSl8S

3. DDPark 监听XXXX端口，用以接收【停车云】推送的数据

4. DDPark 接收到【停车云】推送的数据，解析其中的数据并转发给【滕州停车云】

    a. ???收到停车数据时动态创建(注册)停车场????
    
    b. 车位更新 /park/isv/v1/parkspace/update？？
    
    c. 车辆余位更新  /park/isv/v1/park/availablespace/update
    
    d. 车辆入场  /park/isv/v1/park/record/enter
    
    e. 车辆出场  /park/isv/v1/park/record/depart

5. ？？？【停车云】数据中带有停车场ID（park_id), 需要把这个ID 转发给【滕州停车云】？？？？