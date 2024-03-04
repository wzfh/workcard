import os.path

from core.rquests import  Rquests
from data.read_data import read
from main import allpath


BASE_PATH=allpath()
config_path=os.path.join(BASE_PATH,'config','settings.ini')
api_url=read.read_ini(config_path)['host']['ces']

class USER(Rquests):
    def __init__(self,api_url,**kwargs):
        super(USER, self).__init__(api_url,**kwargs)

    #注册发送短信
    def SendNote(self,**kwargs):
        return self.post('/account/sendNote',**kwargs)

    #注册
    def Register(self,**kwargs):
        return self.post('/account/register',**kwargs)

    #统计设备数据
    def Num(self,**kwargs):
        return self.get('/home/statisticalNumber',**kwargs)

    #登录
    def Login(self,**kwargs):
        return self.post('/account/login',**kwargs)

    #插入公司信息
    def Company(self,**kwargs):
        return self.post('/accountOrgDetail/insertCompanyInfo',**kwargs)

    #获取公司信息
    def Detail(self,**kwargs):
        return self.get('/accountOrgDetail/getAccountOrgDetail',**kwargs)

    #组织的树形结构
    def GetTree(self,**kwargs):
        return self.get('/organization/getOrgTree',**kwargs)

    #添加部门信息
    def Addorgan(self,**kwargs):
        return self.post('/organization/addOrganization',**kwargs)

    #添加员工
    def AddUser(self,**kwargs):
        return self.post('/user/addUser',**kwargs)

    #添加设备
    def AddDevice(self,**kwargs):
        return self.post('/device/addDevice',**kwargs)

    #设备授权
    def AuthDrive(self,**kwargs):
        return self.post('/device/authDeviceBind',**kwargs)



    #修改密码
    def Uppwd(self,**kwargs):
        return self.post('/account/updateUserPassword',**kwargs)



    #退出登录
    def OutLogin(self,**kwargs):
        return self.post('/account/outLogin',**kwargs)














user=USER(api_url)
