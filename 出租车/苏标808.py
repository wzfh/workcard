# coding=utf-8
import binascii
import csv
import os
import re
import time
from socket import *
import random
import diaoyongjar
import math


def get_bcc(inputStr: str) -> str:
    bcc = 0
    for i in inputStr.split(' '):
        bcc = bcc ^ int(i, 16)

    return f'{bcc:x}'


def get_xor(data):
    result = re.sub(r"(?<=\w)(?=(?:\w\w)+$)", " ", data)
    return result


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
正常 = '00000000'


class login:
    def get(self):

        for i in range(1):
            #     try:
            # wd1 = f'23.012173'
            now_time = time.strftime('%Y%m%d%H%M%S', time.localtime())
            wd1 = get_latitude(base_lat=23.012173, radius=15000)
            print(wd1)
            wd2 = float(wd1) / 0.000001
            wd3 = hex(int(wd2))
            # print(wd3[2:].zfill(8).upper())

            # jd1 = f'114.34{i}462'
            # jd1 = f'114.340462'
            jd1 = get_longitude(base_log=114.340462, radius=10000)
            print(jd1)
            jd2 = float(jd1) / 0.000001
            print(int(jd2))
            jd3 = hex(int(jd2))
            print(jd3[2:].zfill(8).upper())
            # for i in range(9):
            # if i < 10:
            #     设备号 = f'00135900000{i}'
            # elif 9<i<100:
            #     设备号 = f'0013590000{i}'
            # elif 99<i<200:
            #     设备号 = f'001359000{i}'

            # if i < 10:
            #     a = f'1113000000{i}'
            # elif 9 < i < 100:
            #     a = f'111300000{i}'
            # elif 99 < i < 1000:
            #     a = f'11130000{i}'
            # elif 999 < i < 10000:
            #     a = f'1113000{i}'
            # 设备号='0'+f'{a}'
            a = '13526855532'
            print(a)
            状态 = '00000001'
            纬度 = wd3[2:].zfill(8).upper()
            经度 = jd3[2:].zfill(8).upper()
            速度 = '0010'
            时间 = now_time[2:]
            标志状态 = '01'
            baojlxs = ["01", "02", "03", "04", "05", "06", "07", ]
            报警事件类型 = '01'
            print(报警事件类型)
            附加信息64 = f'642F00000001{标志状态}{报警事件类型}010000000000100000{经度}{纬度}{时间}0000{a.zfill(14)}{时间}000000'
            附加信息65 = f'652F00000001{标志状态}{报警事件类型}010500000000100000{纬度}{经度}{时间}000030303030303030{时间}000100'
            data = f'0200004D0{a}00010000000000000000{纬度}{经度}0000{速度}000C{时间}' + 附加信息64
            a = get_xor(data)
            b = get_bcc(a)
            # print(附加信息67)
            if b.upper() == "7E":
                a.replace("00", "01")
                b = get_bcc(a)
            E = data + b.upper().zfill(2)
            t = '7E' + E.replace("7E", "01") + '7E'
            D = get_xor(E)
            data = '7E ' + D + ' 7E'
            if data[:2] != "7E":
                print(f"错误：{data}")
                t = t[:81] + "00" + t[82:]
                data = get_xor(t)
                print("修改后data：{}".format(data))
                print('\n' * 1)
            print(data)

            # return '登录包数据：{}\n\n设备号：{}\n\n原始数据：{}'.format(t,t[12:-30],q)

            #
            s = socket(AF_INET, SOCK_STREAM)
            # s = socket(AF_INET, SOCK_DGRAM)
            # s.connect(('120.77.26.175', 7788))
            s.connect(('120.79.74.223', 17201))  # 压测
            # s.connect(('47.119.168.112', 17700))  # 生产
            s.send(bytes().fromhex(data))
            send = s.recv(1024).hex()
            print('服务器应答：' + send.upper())
            print('\n' * 1)
            time.sleep(10)
            # s.close()
        # except:
        #     continue


if __name__ == '__main__':
    ll = login()
    # while True:
    #     sbhaos = [
    #         "13534877410",
    #         "13534877411",
    #         "13534877412",
    #         "13534877413",
    #         "13534877414",
    #         "13534877415",
    #         "13534877416",
    #         "13534877417",
    #         "13534877418",
    #         "13534877519",
    #         "13534877522",
    #         "13534877523",
    #         "13534877524",
    #         "13534877525",
    #         "13534877526",
    #         "13534877527",
    #         "13534877528",
    #         "13534877529",
    #         "13534877530",
    #         "13534877531",
    #         "13534877532",
    #         "13534877533",
    #         "13534877534",
    #         "13534877535",
    #         "13534877536",
    #         "13534877537"
    #     ]
    ll.get()
# !/usr/bin/env python
# coding: utf-8

# from __future__ import division
# import random
# import math


# def get_longitude(base_log=None, base_lat=None, radius=None):
#     radius_in_degrees = radius / 111300
#     u = float(random.uniform(0.0, 1.0))
#     v = float(random.uniform(0.0, 1.0))
#     w = radius_in_degrees * math.sqrt(u)
#     t = 2 * math.pi * v
#     y = w * math.sin(t)
#     longitude = y + base_log
#     print(str(longitude)[:10])
#     return longitude
#
# def get_latitude(base_log=None, base_lat=None, radius=None):
#     radius_in_degrees = radius / 111300
#     u = float(random.uniform(0.0, 1.0))
#     v = float(random.uniform(0.0, 1.0))
#     w = radius_in_degrees * math.sqrt(u)
#     t = 2 * math.pi * v
#     x = w * math.cos(t)
#     latitude = x + base_lat
#     print(str(latitude)[:9])
#     return latitude
#
#
# if __name__ == '__main__':
#     log = get_longitude(base_log=114.3, radius=100000)
#     lat = get_latitude(base_lat=23, radius=100000)
