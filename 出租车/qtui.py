# coding=utf-8
import binascii
import csv
import os
import re
import time
from socket import *

import diaoyongjar


def get_bcc(inputStr: str) -> str:
    bcc = 0
    for i in inputStr.split(' '):
        bcc = bcc ^ int(i, 16)

    return f'{bcc:x}'


def get_xor(data):
    result = re.sub(r"(?<=\w)(?=(?:\w\w)+$)", " ", data)
    return result




wd1 = 23.019173 * 60 / 0.0001
print(wd1)
wd2 = hex(int(wd1))
print(wd2[2:].zfill(8).upper())

jd1 = 114.348462 * 60 / 0.0001
print(jd1)
jd2 = hex(int(jd1))
print(jd2[2:].zfill(8).upper())


紧急报警 = '00000001'
进出区域路线报警 = '00100000'
路段行驶时间不足 = '00200000'
禁行路段行驶 = '00400000'
车辆非法点火 = '01000000'
车辆非法位移 = '02000000'
正常 = '00000000'


class login1:
    def get(self, nob, noc):

        for i in range(2,10991):
            try:
                print(i)
                now_time = time.strftime('%Y%m%d%H%M%S', time.localtime())
                now_time1 = time.strftime('%H%M%S', time.localtime())
                标识位 = '7E'
                消息ID = '0B04'
                消息体属性 = '0043'
                # 设备号 = '1359000011'
                if 1 < i < 10:
                    设备号 = f'000000000{i}'
                if 9 < i < 100:
                    设备号 = f'00000000{i}'
                if 99 < i < 1000:
                    设备号 = f'0000000{i}'
                if 999 < i < 10000:
                    设备号 = f'000000{i}'
                if 9999<i<10991:
                    设备号 = f'00000{i}'
                ISU标识 = '10{}'.format(设备号)  # 10位
                流水号 = f'0001'
                报警 = 紧急报警
                状态 = '00000003'
                纬度 = wd2[2:].zfill(8).upper()
                经度 = jd2[2:].zfill(8).upper()
                速度 = '0001'
                方向 = '00'
                时间 = now_time[2:]
                企业经营许可证号 = '534E3132333435363738393100000000'  # SN1234567891
                # 驾驶员从业资格证号 = '534E3132333435363738393132333435363739'  # SN12345678912345679
                驾驶员从业资格证号 = '534E3132333435363738393132333435363731'  # SN12345678912345671
                车牌号 = '534E31323535'  # SN1255
                计价器K值 = '0013'  # 计价12
                当班开机时间 = now_time[:12]
                当班关机时间 = now_time[:12]
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
                # print(t)
                print(data)

                # return '登录包数据：{}\n\n设备号：{}\n\n原始数据：{}'.format(t,t[12:-30],q)

                #
                s = socket(AF_INET, SOCK_STREAM)
                # s.connect(('120.79.74.223', 17800))
                s.connect(('120.79.176.183', 17800))  # 压测
                # s.connect(('47.119.168.112', 17800))  # 生产
                s.send(bytes().fromhex(t))
                print('\n' * 1)
                # time.sleep(1)
                s.close()
            except:
                pass

if __name__ == '__main__':
    ll = login1()
    for j in range(10):
        ll.get(2, 1)
