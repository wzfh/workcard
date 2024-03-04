import grequests

proxyMeta = "192.168.10.59:808"
proxysdata = {
    'http': proxyMeta,
    'https': proxyMeta
}
sessionId = "20743bfb-6ee1-4630-a598-356fbc1f2325"
# urls = 'http://47.119.168.112:90'
url = 'http://47.106.25.58:60'
用户登录 = url+'/user/login.json?account=admin&password=123456'
用户登录头信息 = {
    "Content-Type": "application/json"
}
添加用户 = url + '/user/addCustomer.json'
添加用户头信息 = {
    "Content-Type": "application/json",
    "sessionId": sessionId
}
添加用户Body = {
    "userId": "",
    "name": f"{3}",
    "password": f"{3}",
    "parentId": "57",
    "account": f"{3}",
    "accountType": "0",
    "contactHuman": "",
    "phone": "",
    "code": "",
    "groupIds": [1, 46]
}
新增驾驶员 = url + '/driver/addDriver'
新增驾驶员头信息 = {
    "Content-Type": "application/x-www-form-urlencoded",
    "sessionId": sessionId
}
新增驾驶员Body = {
    "name": "额温枪",
    "ethnicGroup": "汉",
    "phone": "13526988547",
    "email": "1114377437@qq.com",
    "sex": "1"
}
新增车组 = url + '/group/addVehGroup.json'
新增车组Body = {
    "groupName": "额温枪",
    "parentId": "47",
    "phone": "",
    "remark": ""
}

#
# req_list = [  # 请求列表
#     grequests.get(url=用户登录, headers=用户登录头信息, proxies=proxysdata),
#     grequests.post(url=添加用户, headers=添加用户头信息, params=添加用户Body, proxies=proxysdata),
#     grequests.post(url=新增驾驶员, headers=新增驾驶员头信息, params=新增驾驶员Body, proxies=proxysdata),
#     grequests.post(url=新增车组, headers=新增驾驶员头信息, params=新增车组Body, proxies=proxysdata),
#
# ]
#
# res_list = grequests.map(req_list)  # 并行发送，等最后一个运行完后返回
# print('用户登录' + res_list[0].text)  # 打印第一个请求的响应文本
# print('添加用户' + res_list[1].text)  # 打印第一个请求的响应文本
# print('新增驾驶员' + res_list[2].text)  # 打印第一个请求的响应文本
# print('新增车组' + res_list[3].text)  # 打印第一个请求的响应文本


删除用户=url+'/user/removeCustomer.json'
分页展示用户信息=url+'/user/pageCustomer.json?account=admin&pageNumber=1&pageSize=10&name=admin&userId=1'
新增车辆=url+'/vehicle/addVehicle'
分页展示车辆信息=url +'/vehicle/pageVehicle?pageNumber=1&pageSize=10'
分页展示车辆操作记录=url+'/vehicleLog/pageVehicleLog?startTime=2023-06-29 00:00:00&endTime=2023-07-29 23:59:59&pageSize=10&pageNumber=1'
输入一个地址和半径找出所有未离线的设备=url+'/location/searchLocationVehicleRange.json?lon=114.34009533027735&lat=23.01253168159737&distance=1'
车辆信息与位置数据=url+'/monitoring/vehicleList?ids=1&flag=1&searchType=1&pageSize=10&pageNumber=1'
获取车组树=url+'/group/getGroupTree.json'
新增车组Body={
        "groupName":"3",
        "parentId":"47",

    }
新增车辆Body={'groupId': '46',
    'terminalNo': f'3'.zfill(11),
    'productType': '1',
    'terminalModel': 'D8-808',
    'driverIds': '',
    'plate': f'3'.zfill(11),
    'vehicleColor': '',
    'vehicleType': '1',
    'vin': '',
    'frameNo': '',
    'sim': '',
    'iccid': '',
    'humanName': '',
    'humanPhone': '',
    'driLicenseNo': '',
    'driLicenseExpireTime': '',
    'installHumanName': '',
    'installHumanPhone': '',
    'installTime': '',
    'operationalState': '1',
    'cameraCircuit': '1,2,3,4'}
from locust import HttpUser, task, between

class MyUser(HttpUser):
    wait_time = between(1, 3) # 设置用户等待时间

    @task
    def my_task(self):
        self.client.get(url=用户登录) # 替换为您要测试的接口地址
        self.client.get(url=分页展示用户信息,headers=添加用户头信息) # 替换为您要测试的接口地址
        self.client.get(url=分页展示车辆信息,headers=添加用户头信息) # 替换为您要测试的接口地址
        self.client.get(url=分页展示车辆操作记录,headers=添加用户头信息) # 替换为您要测试的接口地址
        self.client.get(url=输入一个地址和半径找出所有未离线的设备,headers=添加用户头信息) # 替换为您要测试的接口地址
        self.client.get(url=车辆信息与位置数据,headers=添加用户头信息) # 替换为您要测试的接口地址
        self.client.get(url=获取车组树,headers=添加用户头信息) # 替换为您要测试的接口地址
        # self.client.post(url=添加用户,headers=添加用户头信息,params=添加用户Body) # 替换为您要测试的接口地址
        # self.client.post(url=新增车辆,headers=添加用户头信息,params=新增车辆Body) # 替换为您要测试的接口地址
        # self.client.post(url=新增驾驶员,headers=新增驾驶员头信息,params=新增驾驶员Body) # 替换为您要测试的接口地址
        # self.client.post(url=新增车组,headers=添加用户头信息,params=新增车组Body) # 替换为您要测试的接口地址
        # self.client.post(url=删除用户,headers=添加用户头信息,params=) # 替换为您要测试的接口地址


















