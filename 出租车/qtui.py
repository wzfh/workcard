# coding=utf-8
import os
import re
import time
from socket import *

from configobj import ConfigObj


def get_bcc(inputStr: str) -> str:
    bcc = 0
    for i in inputStr.split(' '):
        bcc = bcc ^ int(i, 16)

    return f'{bcc:x}'


def get_xor(data):
    result = re.sub(r"(?<=\w)(?=(?:\w\w)+$)", " ", data)
    return result







紧急报警 = '00000001'
进出区域路线报警 = '00100000'
路段行驶时间不足 = '00200000'
禁行路段行驶 = '00400000'
车辆非法点火 = '01000000'
车辆非法位移 = '02000000'
正常 = '00000000'


class login1:
    def __init__(self):
        conf_ini = os.path.dirname(os.path.dirname(__file__)) + "\\conf\\config.ini"
        config = ConfigObj(conf_ini, encoding='UTF-8')
        self.wg = config['ces']['出租车_cswg']
        self.wg_port = config['ces']['出租车_cs905wg_port']
        self.wd = config['address']['茂名市WD']
        self.jd = config['address']['茂名市JD']
        self.baojing = config['905baojing']
        self.ztai = config['905ztai']
        self.sbei = config['sbei']['905sbei']
        self.驾驶员从业资格证号 = config['驾驶员从业资格证号']['欧先生']

    def get(self):

        for i in range(1):
            now_time = time.strftime('%Y%m%d%H%M%S', time.localtime())
            now_time1 = time.strftime('%H%M%S', time.localtime())
            标识位 = '7E'
            消息ID = '0B04'
            消息体属性 = '0043'
            ISU标识 = self.sbei  # 10位
            流水号 = f'0001'
            报警 = 紧急报警
            状态 = '00000003'
            wd1 = float(self.wd) * 60 / 0.0001
            wd2 = hex(int(wd1))

            jd1 = float(self.jd) * 60 / 0.0001
            jd2 = hex(int(jd1))

            纬度 = wd2[2:].zfill(8).upper()
            经度 = jd2[2:].zfill(8).upper()
            速度 = '0001'
            方向 = '00'
            时间 = now_time[2:]
            企业经营许可证号 = '534E3132333435363738393100000000'  # SN1234567891
            驾驶员从业资格证号 = self.驾驶员从业资格证号
            车牌号 = '534E31323535'  # SN1255
            计价器K值 = '0013'  # 计价12
            当班开机时间 = now_time[:12]
            print('当班开机时间' + 当班开机时间)
            当班关机时间 = now_time[:10] + '59'
            print(当班关机时间)
            当班里程 = '000120'  # 格式为XXXXX.X(km)
            当班营运里程 = '000120'  # 格式为XXXXX.X(km)
            车次 = '0002'  # 车次12
            计时时间 = now_time1
            总计金额 = '000130'
            卡收金额 = '000130'
            卡次 = '0012'
            班间里程 = '0130'
            总计里程 = '00000120'
            总营运里程 = '00000120'
                单价 = '1300'  # 12.00块
                总营运次数 = '0000001A'  # 高位在前就是在后面
                if (i % 2) == 0:
                    签退方式 = '01'
                else:
                    签退方式 = '00'
                附加 = '01040000006E0202044C250400000000300103'

            w = 消息ID + 消息体属性 + ISU标识 + 流水号 + 报警 + 状态 + 纬度 + 经度 + 速度 + 方向 + 时间 + 企业经营许可证号 + 驾驶员从业资格证号 + 车牌号 + 计价器K值 + 当班开机时间 + 当班关机时间 + 当班里程 + 当班营运里程 + 车次 + 计时时间 + 总计金额 + 卡收金额 + 卡次 + 班间里程 + 总计里程 + 总营运里程 + 单价 + 总营运次数 + 签退方式 + 附加
            a = get_xor(w)
            b = get_bcc(a)
            t = 标识位 + w + b.upper() + 标识位
            data = get_xor(t)
            print(t)
            print(data)

            s = socket(AF_INET, SOCK_STREAM)
            s.connect((self.wg, int(self.wg_port)))
            s.send(bytes().fromhex(data))
            send = s.recv(1024).hex()
            print(send.upper())
            print('\n' * 1)
            time.sleep(1)


if __name__ == '__main__':
    ll = login1()
    # for j in range(10):
    ll.get()
