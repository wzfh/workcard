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
    return str(longitude)[:9]


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
        global s, t
        count = 0

        for i in range(1):
            now_time = time.strftime('%Y%m%d%H%M%S', time.localtime())
            wd1 = get_latitude(base_lat=23.01217, radius=15000)
            wd2 = float(wd1) / 0.00001
            print(str(int(wd2)))
            # wd3 = hex(int(wd2))

            jd1 = get_longitude(base_log=114.34046, radius=15000)
            jd2 = float(jd1) / 0.00001
            print(str(int(jd2)))
            # jd3 = hex(int(jd2))
            标识位 = '2929'
            消息ID = '80'
            消息体属性 = '0028'
            # 伪ip = '58D8D858'
            伪ip = '81828CA2'
            # 伪ip = 'DBDFFA38'
            时间 = now_time[2:]
            # 纬度 = '02132004'
            纬度 = str(int(wd2)).zfill(8)
            经度 = str(int(jd2)).zfill(8)
            # 经度 = '10501560'
            速度 = '0120'
            方向 = '0154'
            定位 = 'F0'

            附加信息ID = '000000FEFC0000001E000000000000'


            w = 消息ID + 消息体属性 + 伪ip + 时间 + 纬度 + 经度 + 速度 + 方向 + 定位 + 附加信息ID
            a = get_xor(w)
            b = get_bcc(a).zfill(2)
            E = w + b.upper()
            t = 标识位 + E.replace("7E", "00") + '0D'
            print(t)
            data = get_xor(t)
            print(data)
            count += 1

            # return '登录包数据：{}\n\n设备号：{}\n\n原始数据：{}'.format(t,t[12:-30],q)
            # while True:
            # # #
            # s = socket(AF_INET, SOCK_STREAM)
            s = socket(AF_INET, SOCK_DGRAM)
            #
            s.settimeout(5)  # 设置超时时间
            #
            s.connect(('47.107.222.141', 6688))  # 测试
            # s.connect(('120.77.130.46', 6688))  # 测试
            # s.connect(('120.79.74.223', 6688))# 106开发测试
            # s.connect(('120.79.176.183', 17700))  # 压测
            # s.connect(('47.119.168.112', 17700))#生产
            # s.sendall(bytes().fromhex(t))
            s.send(bytes().fromhex(t))
            # s.send()
            send = s.recv(1024).hex()
            print(send.upper())
            # print('\n' * 1)
            time.sleep(1)

            # print("总计发送成功808位置数据条数：{}".format(count))

        # s.close()
        # except:
        #     continue


if __name__ == '__main__':
    ll = login()
    ll.get(2, 1)
