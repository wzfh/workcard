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


def get_longitude(base_log=None,radius=None):
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
        for i in range(9):
            try:
                now_time = time.strftime('%Y%m%d%H%M%S', time.localtime())
                # wd1 = f'23.01{i}173'
                # wd1 = f'23.019173'
                wd1 = get_latitude(base_lat=23.019173, radius=1500)
                print(wd1)
                wd2 = float(wd1) * 60 / 0.0001
                wd3 = hex(int(wd2))
                # print(wd3[2:].zfill(8).upper())

                # jd1 = f'114.34{i}462'
                # jd1 = f'114.348462'
                jd1 = get_longitude(base_log=114.348462, radius=1000)
                print(jd1)
                jd2 = float(jd1) * 60 / 0.0001
                jd3 = hex(int(jd2))
                # print(jd3[2:].zfill(8).upper())
                # for i in range(9):
                消息ID='9101'
                消息体属性='0015'
                设备号=f'0{13560000000}'
                流水号=f'000{i}'
                IP长度='0D'
                IP='3132302E37392E37342E323233'
                tcp='5D50'
                udp='1F40'
                逻辑通道号='35'
                数据类型='02'
                码流='01'
                标识位 ='7E'

                w = 消息ID+消息体属性+设备号+流水号+IP长度+IP+tcp+udp+逻辑通道号+数据类型+码流
                a = get_xor(w)
                b = get_bcc(a)
                t = 标识位 + w + b.upper() + 标识位
                data = get_xor(t)
                print(t)
                print(data)

                # return '登录包数据：{}\n\n设备号：{}\n\n原始数据：{}'.format(t,t[12:-30],q)

                # # #
                # s = socket(AF_INET, SOCK_STREAM)
                # s.connect(('120.79.74.223', 17700))#测试
                # # s.connect(('47.119.168.112', 17800))#生产
                # s.send(bytes().fromhex(t))
                # print('\n' * 1)
                # time.sleep(2)
                # s.close()
            except:
                continue


if __name__ == '__main__':
    ll = login()
    ll.get(2, 1)
