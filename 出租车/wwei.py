# coding=utf-8
import binascii
import csv
import os
import re
import time
from socket import *

import diaoyongjar
import random
import math


def get_longitude(base_log=None, radius=None):
    radius_in_degrees = radius / 111300
    u = float(random.uniform(0.0, 1.0))
    v = float(random.uniform(0.0, 1.0))
    w = radius_in_degrees * math.sqrt(u)
    t = 2 * math.pi * v
    y = w * math.sin(t)
    longitude = y + base_log
    # print()
    return str(longitude)[:10]


def get_latitude(base_lat=None, radius=None):
    radius_in_degrees = radius / 111300
    u = float(random.uniform(0.0, 1.0))
    v = float(random.uniform(0.0, 1.0))
    w = radius_in_degrees * math.sqrt(u)
    t = 2 * math.pi * v
    x = w * math.cos(t)
    latitude = x + base_lat
    # print(str(latitude)[:9])
    return str(latitude)[:9]


def get_bcc(inputStr: str) -> str:
    bcc = 0
    for i in inputStr.split(' '):
        bcc = bcc ^ int(i, 16)

    return f'{bcc:x}'


def get_xor(data):
    result = re.sub(r"(?<=\w)(?=(?:\w\w)+$)", " ", data)
    return result


# print(now_time[2:])

紧急报警 = '00000001'
超速报警 = '00010000'
LED顶灯故障 = '00008000'
进出区域路线报警 = '00100000'
路段行驶时间不足 = '00200000'
禁行路段行驶 = '00400000'
车辆非法点火 = '01000000'
车辆非法位移 = '02000000'
所有清零报警 = '03700000'
紧急报警和超速报警 = '00010001'
正常 = '00000000'


class login:
    def get(self, nob, noc):
        for i in range(99):
            # try:
                now_time = time.strftime('%Y%m%d%H%M%S', time.localtime())
                print(i)
                # wd1 = f'23.01{i}173'
                wd1 = f'23.013173'
                # wd1 = get_latitude(base_lat=23.019173, radius=1500)
                # print(wd1)
                wd2 = float(wd1) * 60 / 0.0001
                wd3 = hex(int(wd2))
                # print(wd3[2:].zfill(8).upper())

                # jd1 = f'114.34{i}462'
                jd1 = f'114.348462'
                # jd1 = get_longitude(base_log=114.348462, radius=1000)
                # print(jd1)
                jd2 = float(jd1) * 60 / 0.0001
                jd3 = hex(int(jd2))
                # print(jd3[2:].zfill(8).upper())
                # for i in range(9):
                标识位 = '7E'
                消息ID = '0200'
                消息体属性 = '002F'
                # if i < 10:
                #     设备号 = f'135900000{i}'
                # elif 9<i<100:
                #     设备号 = f'13590000{i}'
                # elif 99<i<200:
                #     设备号 = f'1359000{i}'
                # 设备号 = f'013120000000'
                设备号 = f'012345678911'
                # 设备号 = f'{i}'.zfill(12)
                # print(设备号)
                # ISU标识 = '10{}'.format(设备号)  # 10位
                流水号 = f'{1}'.zfill(4)
                # print(流水号)
                报警 = 正常
                状态 = '00000000'
                纬度 = '015F3EA5'
                经度 = '06D0D1AE'
                高程 = '0001'

                速度 = '0001'
                方向 = '000C'
                时间 = now_time[2:]
                附加信息ID = '01040000001E0202044C250400000000300103'
                # 附加信息长度 = '04'
                # 附加信息 = f'00000006'
                # print(附加信息)
                # 附加='01040000006E0202044C250400000000300103'

                w = 消息ID + 消息体属性 + 设备号 + 流水号 + 报警 + 状态 + 纬度 + 经度 + 高程 + 速度 + 方向 + 时间 + 附加信息ID
                a = get_xor(w)
                b = get_bcc(a)
                t = 标识位 + w + b.upper() + 标识位
                if "7E" in w+b.upper():
                    return '失败'
                else:

                    data = get_xor(t)
                    # print(t)
                    print(data)

                    # return '登录包数据：{}\n\n设备号：{}\n\n原始数据：{}'.format(t,t[12:-30],q)

                    # # #
                    s = socket(AF_INET, SOCK_STREAM)
                    s.connect(('120.79.74.223', 17700))#测试
                    # s.connect(('120.77.133.46', 7788))# 106开发测试
                    # s.connect(('120.79.176.183', 17700))  # 压测
                    # s.connect(('47.119.168.112', 17700))#生产
                    s.send(bytes().fromhex(t))
                    print('\n' * 1)
                    # time.sleep(3)
                    # s.close()
            # except:
            #     continue


if __name__ == '__main__':
    ll = login()
    ll.get(2, 1)
