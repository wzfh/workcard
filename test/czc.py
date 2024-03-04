import requests
import grequests
import time
proxyMeta = "192.168.10.59:808"
proxysdata = {
    'http': proxyMeta,
    'https': proxyMeta
}

sessionId="412c7042-98f3-4728-9de0-18252f0bcfe4"
urls='http://47.119.168.112:90'
url='http://47.106.25.58:60'
用户登录 = url+'/user/login.json?account=admin&password=123456'
用户登录头信息={
    "Content-Type":"application/json"
}
添加用户 = url+'/user/addCustomer.json'
添加用户头信息={
    "Content-Type":"application/json",
    "sessionId":sessionId
}
#添加用户
# def 参数():
# start_time = time.time()
# for i in range(100):
#     print(i)
#     添加用户Body={
#             "userId":"",
#             "name": f"{i}",
#             "password": f"{i}",
#             "parentId": "57",
#             "account": f"{i}",
#             "accountType": "0",
#             "contactHuman": "",
#             "phone": "",
#             "code": "",
#             "groupIds": [1,46]
#     }
#
#
#     # start_time = time.time()
#     num_requests = 1
#     for _ in range(num_requests):
#         # response = requests.get(url=用户登录,headers=用户登录头信息,proxies=proxysdata)
#         response = requests.get(url=用户登录,headers=用户登录头信息,proxies=proxysdata)
#         # response = requests.post(url=添加用户,headers=添加用户头信息,params=添加用户Body,proxies=proxysdata)
#         # response = requests.post(url=删除用户,headers=头信息,params=参数(),proxies=proxysdata)
#         print(response.json())
#                 # 处理响应数据或记录响应时间等操作
#
#
# end_time = time.time()
# print(end_time)
# total_time = end_time - start_time
# average_time = total_time / 100
#
# print(f'Total time: {total_time}s')
# print(f'Average time: {average_time}s')
删除用户=url+'/user/removeCustomer.json'
删除用户头信息={
    "Content-Type":"application/x-www-form-urlencoded",
    "sessionId":sessionId
}
分页展示用户信息=url+'/user/pageCustomer.json?account=admin&pageNumber=1&pageSize=10&name=admin&userId=1'
新增车辆=url+'/vehicle/addVehicle'
分页展示车辆信息=url +'/vehicle/pageVehicle?pageNumber=1&pageSize=10'
分页展示车辆操作记录=url+'/vehicleLog/pageVehicleLog?startTime=2023-06-29 00:00:00&endTime=2023-07-29 23:59:59&pageSize=10&pageNumber=1'
输入一个地址和半径找出所有未离线的设备=url+'/location/searchLocationVehicleRange.json?lon=114.34009533027735&lat=23.01253168159737&distance=1'
车辆信息与位置数据=url+'/monitoring/vehicleList?ids=1&flag=1&searchType=1&pageSize=10&pageNumber=1'
获取车组树=url+'/group/getGroupTree.json'

#新增车辆
# start_time = time.time()
# for i in range(100):
#     新增车辆Body={'groupId': '47',
#     'terminalNo': f'{i}'.zfill(11),
#     'productType': '1',
#     'terminalModel': 'D8-808',
#     'driverIds': '',
#     'plate': f'{i}'.zfill(11),
#     'vehicleColor': '',
#     'vehicleType': '1',
#     'vin': '',
#     'frameNo': '',
#     'sim': '',
#     'iccid': '',
#     'humanName': '',
#     'humanPhone': '',
#     'driLicenseNo': '',
#     'driLicenseExpireTime': '',
#     'installHumanName': '',
#     'installHumanPhone': '',
#     'installTime': '',
#     'operationalState': '1',
#     'cameraCircuit': '1,2,3,4'}
#     num_requests = 1
#     for _ in range(num_requests):
#         # response = requests.get(url=用户登录,headers=用户登录头信息,proxies=proxysdata)
#         # response = requests.get(url=分页展示用户信息,headers=添加用户头信息,proxies=proxysdata)
#         response = requests.post(url=新增车辆,headers=添加用户头信息,params=新增车辆Body,proxies=proxysdata)
#         # response = requests.post(url=添加用户,headers=添加用户头信息,params=添加用户Body,proxies=proxysdata)
#         # response = requests.post(url=删除用户,headers=头信息,params=参数(),proxies=proxysdata)
#         print(response.json())
#                 # 处理响应数据或记录响应时间等操作
#
#
# end_time = time.time()
# print(end_time)
# total_time = end_time - start_time
# average_time = total_time / 100
#
# print(f'Total time: {total_time}s')
# print(f'Average time: {average_time}s')

#新增车组
# 新增车组=url+'/group/addVehGroup.json'
# start_time= time.time()
# for i in range(100):
#     新增车组Body={
#         "groupName":f"{i}",
#         "parentId":"47",
#
#     }
#     num_requests = 1
#     for _ in range(num_requests):
#         response = requests.post(url=新增车组, headers=添加用户头信息, params=新增车组Body,proxies=proxysdata)
#         print(response.json())
#         # 处理响应数据或记录响应时间等操作
#
# end_time = time.time()
# print(end_time)
# total_time = end_time - start_time
# average_time = total_time / 100
#
# print(f'Total time: {total_time}s')
# print(f'Average time: {average_time}s')

# 创建订单=url +'/order/createOrder'
# start_time= time.time()
# for i in range(100):
#     创建订单Body={'type': '0',
#     'usageTime': '2023-07-10 10:46:35',
#     'startLon': '114.3400953',
#     'startLat': '23.0125317',
#     'endLon': '114.3215441',
#     'endLat': '23.0071002',
#     'serviceFee': f'{i}',
#     'passengerMobile': '13829622001',
#     'passengerName': '姚先生',
#     'areaCoverage': '1',
#     'describe': f'{i}'}
#     num_requests = 1
#     start_time = time.time()
#     for _ in range(num_requests):
#         # response = requests.get(url=用户登录,headers=用户登录头信息,proxies=proxysdata)
#         # response = requests.get(url=分页展示用户信息,headers=添加用户头信息,proxies=proxysdata)
#         # response = requests.get(url=分页展示车辆信息,headers=添加用户头信息,proxies=proxysdata)
#         # response = requests.get(url=分页展示车辆操作记录,headers=添加用户头信息,proxies=proxysdata)
#         # response = requests.get(url=输入一个地址和半径找出所有未离线的设备,headers=添加用户头信息,proxies=proxysdata)
#         # response = requests.get(url=车辆信息与位置数据,headers=添加用户头信息,proxies=proxysdata)
#         # response = requests.get(url=获取车组树, headers=添加用户头信息, proxies=proxysdata)
#         # response = requests.post(url=新增车辆,headers=添加用户头信息,params=新增车辆Body,proxies=proxysdata)
#         response = requests.post(url=创建订单,headers=添加用户头信息,params=创建订单Body,proxies=proxysdata)
#         # response = requests.post(url=添加用户,headers=添加用户头信息,params=添加用户Body,proxies=proxysdata)
#         # response = requests.post(url=删除用户,headers=头信息,params=参数(),proxies=proxysdata)
#         print(response.json())
#         # 处理响应数据或记录响应时间等操作
#
# end_time = time.time()
# print(end_time)
# total_time = end_time - start_time
# average_time = total_time / 100
#
# print(f'Total time: {total_time}s')
# print(f'Average time: {average_time}s')



# num_requests = 100
# start_time= time.time()
# for _ in range(num_requests):
#     # response = requests.get(url=用户登录,headers=用户登录头信息,proxies=proxysdata)
#     # response = requests.get(url=分页展示用户信息,headers=添加用户头信息,proxies=proxysdata)
#     # response = requests.get(url=分页展示车辆信息,headers=添加用户头信息,proxies=proxysdata)
#     # response = requests.get(url=分页展示车辆操作记录,headers=添加用户头信息,proxies=proxysdata)
#     # response = requests.get(url=输入一个地址和半径找出所有未离线的设备,headers=添加用户头信息,proxies=proxysdata)
#     # response = requests.get(url=车辆信息与位置数据,headers=添加用户头信息,proxies=proxysdata)
#     response = requests.get(url=获取车组树,headers=添加用户头信息,proxies=proxysdata)
#     # response = requests.post(url=新增车辆,headers=添加用户头信息,params=新增车辆Body,proxies=proxysdata)
#     # response = requests.post(url=添加用户,headers=添加用户头信息,params=添加用户Body,proxies=proxysdata)
#     # response = requests.post(url=删除用户,headers=头信息,params=参数(),proxies=proxysdata)
#     print(response.json())
#             # 处理响应数据或记录响应时间等操作
#
#
# end_time = time.time()
# print(end_time)
# total_time = end_time - start_time
# average_time = total_time / 100
#
# print(f'Total time: {total_time}s')
# print(f'Average time: {average_time}s')