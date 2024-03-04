# encoding=utf-8
from data.resuly import ResultFile
from api.user import user
from lxpy import copy_headers_dict


# 发送短信验证码
def sendnote(phone):
    result = ResultFile()
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    body = {
        'phone': phone
    }
    res = user.SendNote(headers=headers, json=body)
    print(res.json())
    return result


# 注册
def register(realName, phoneNumber, password, confirmPassword):
    result = ResultFile()
    headers = {
        'Content-Type': 'application/json'
    }
    code = input('验证码：')
    body = {
        'realName': realName,
        'phoneNumber': phoneNumber,
        'password': password,
        'confirmPassword': confirmPassword,
        'code': code
    }
    res = user.Register(headers=headers, data=body)
    print(res.json())
    return result

#统计设备数据
def num(sessionId):
    result = ResultFile()
    headers = {
        'Content-Type': 'application/json',
        'sessionId': sessionId
    }
    res=user.Num(headers=headers)
    print(res.json())
    return result

# 登录
def login(name, password):
    result = ResultFile()
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    body = {
        'name': name,
        'password': password,
    }
    res = user.Login(headers=headers, json=body)
    print(res.json())
    sessionId = res.json()['data']['sessionId']
    result = res.json()
    print(sessionId)
    return result


# 插入公司信息
def company(sessionId, file, companyName):
    result = ResultFile()
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'sessionId': sessionId
    }

    body = {
        'companyName': companyName,
        'file': file
    }
    res = user.Company(headers=headers, json=body)
    print(res.json())
    return result


# 获取公司信息
def detail(sessionId):
    result = ResultFile()
    headers = {
        'Content-Type': 'application/json',
        'sessionId': sessionId
    }
    res = user.Detail(headers=headers)
    print(res.json())
    return result

ids=[]
# 组织的树形结构
def gettree(sessionId):
    result = ResultFile()
    headers = {
        'Content-Type': 'application/json',
        'sessionId': sessionId
    }
    res = user.GetTree(headers=headers)
    tree=res.json()
    print('组织树形结构:'+str(tree))
    data=res.json()['data']
    data1=res.json()['data'][0]
    for data1 in data:
        print(f"组织ID:{data1['id']}  ,  组织名称 :{data1['orgName']}  , 当前组织上级组织ID：{data1['parentIdRecord']}")
        ids.append(data1['id'])
    return result

import random
#添加部门信息
def addorgran(sessionId,orgName):
    result=ResultFile()
    headers={
        'Content-Type': 'application/json',
        'sessionId': sessionId
    }
    gettree(sessionId)
    parentId=random.choice(ids)
    body={
        'orgName':orgName,
        'parentId':parentId  #父级id
    }
    print(parentId)
    res=user.Addorgan(headers=headers,data=body)
    bm=res.json()
    print('添加部门：' + str(bm))
    return result

#添加员工
def adduser(sessionId,userName,phone,gender,position):
    result=ResultFile()
    headers={
        'Content-Type': 'application/json',
        'sessionId': sessionId
    }
    orgId=random.choice(ids)
    body={
        'userName':userName,
        'phone':phone,
        'gender':gender,
        'position':position,
        'orgId':orgId
    }
    print(orgId)
    res=user.AddUser(headers=headers,data=body)
    yg=res.json()
    print('添加员工：' + str(yg))
    return result


#添加设备
def adddevice(sessionId,name,sn,lockRule,installAddress):
    result=ResultFile()
    headers={
        'Content-Type': 'application/json',
        'sessionId': sessionId
    }
    body={
        'name':name,
        'sn':sn,
        'lockRule':lockRule,
        'installAddress':installAddress
    }
    res=user.AddDevice(headers=headers,data=body)
    sb=res.json()
    print('添加设备：'+str(sb))
    return result


#设备授权
def authdrive(sessionId,deviceId):
    result=ResultFile()
    headers={
        'Content-Type': 'application/json',
        'sessionId': sessionId
    }
    body={
  "deviceId": deviceId,
  "list":  [
        {
            "level": 1,
            "objectType": 1,
            "objectId": 982
        }
        ]
    }

    res=user.AuthDrive(headers=headers,data=body)
    print('设备授权'+str(res.json()))
    return result



# 修改密码
def uppwd(sourcePwd, targetPed, sessionId):
    result = ResultFile()
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'sessionId': sessionId
    }
    body = {
        'sourcePwd': sourcePwd,
        'targetPed': targetPed
    }
    res = user.Uppwd(headers=headers, json=body)
    print(res.json())
    return result


# 退出登录
def outlogin(sessionId):
    result = ResultFile()
    headers = {
        'Content-Type': 'application/json',
        'sessionId': sessionId
    }
    res = user.OutLogin(headers=headers)
    result = res.json()
    print(result)
    return result















if __name__ == '__main__':
    res=login('15875226034','789987')
    # res1=num(res['data']['sessionId'])
    # res=login('yzq','123456')
    # res=outlogin('1550175b-3320-4102-bcbe-f83529f28bc2')
    # res=sendnote('15875226034')
    # res1=register('yzq','15875226034','123456','123456')
    # res1=uppwd('qq123456','123456',res['data']['sessionId'])
    # res2=company(res['data']['sessionId'],'config/logo.png','帝国大厦')
    # res2=detail(res['data']['sessionId'])
    # res6 = gettree(res['data']['sessionId'])
    # for i in range(1000):
    #     res3=addorgran(res['data']['sessionId'],f'帝国大厦2{i}')
    # for i in range(10,99):
    #     res4=adduser(res['data']['sessionId'],f'员工{i}',f'158751203{i}','1','1')
    for i in range(1000):
        res5=adddevice(res['data']['sessionId'],f'测试列表{i}',f'00{i}','1,2','1212')
    # for i in range(387,403):
    #     res1=authdrive(res['data']['sessionId'],f'10{i}')