# coding=utf-8
import re
import time


def get_bcc(inputStr: str) -> str:
    bcc = 0
    for i in inputStr.split(' '):
        bcc = bcc ^ int(i, 16)

    return f'{bcc:x}'
def get_xor(data):
    result = re.sub(r"(?<=\w)(?=(?:\w\w)+$)", " ", data)
    return result

def get_longitude(base_log=None,radius=None):
    radius_in_degrees = radius / 111300
    u = float(random.uniform(0.0, 1.0))
    v = float(random.uniform(0.0, 1.0))
    w = radius_in_degrees * math.sqrt(u)
    t = 2 * math.pi * v
    y = w * math.sin(t)
    longitude = y + base_log
    return str(longitude)[:10]


def get_latitude(base_lat=None, radius=None):
    radius_in_degrees = radius / 111300
    u = float(random.uniform(0.0, 1.0))
    v = float(random.uniform(0.0, 1.0))
    w = radius_in_degrees * math.sqrt(u)
    t = 2 * math.pi * v
    x = w * math.cos(t)
    latitude = x + base_lat
    return str(latitude)[:9]


class login:
    def get(self, nob, noc):

        # for i in range(11):
        #     try:
                # wd1 = f'23.012173'
                now_time = time.strftime('%Y%m%d%H%M%S', time.localtime())
                wd1 = get_latitude(base_lat=23.012173, radius=15000)
                print(wd1)
                wd2 = float(wd1)/0.000001
                wd3 = hex(int(wd2))
                # print(wd3[2:].zfill(8).upper())

                # jd1 = f'114.34{i}462'
                # jd1 = f'114.340462'
                jd1 = get_longitude(base_log=114.340462, radius=10000)
                print(jd1)
                jd2 = float(jd1)/0.000001
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
                设备号='012345678911'
                状态='00000001'
                纬度=wd3[2:].zfill(8).upper()
                经度=jd3[2:].zfill(8).upper()
                速度='0010'
                时间=now_time[2:]
                标志状态='01'
                附加信息64=f'642F00000001{标志状态}01011020000000100000{经度}{纬度}{时间}000030303030303030{时间}000100'
                附加信息65=f'652F00000001{标志状态}04010500000000100000{纬度}{经度}{时间}000030303030303030{时间}000100'
                长度='4D'
                data=f'020000{长度}{设备号}00010000000000000000{纬度}{经度}0000{速度}000C{时间}'+附加信息65
                # print(附加信息67)
                print(data)
                a = get_xor(data)
                b = get_bcc(a)
                t = '7E'+data+b.upper()+'7E'
                data1=get_xor(t)
                # print(t)
                print(data1)



            # return '登录包数据：{}\n\n设备号：{}\n\n原始数据：{}'.format(t,t[12:-30],q)


            #
                # s = socket(AF_INET, SOCK_STREAM)
                # # s.connect(('120.79.74.223', 17700))
                # # s.connect(('120.79.176.183', 17700))  # 压测
                # s.connect(('47.119.168.112', 17700))  # 生产
                # s.send(bytes().fromhex(t))
                # print('\n' * 1)
                # time.sleep(1)
                # s.close()
            # except:
            #     continue


if __name__ == '__main__':
    ll = login()
    ll.get(2,1)
#!/usr/bin/env python
# coding: utf-8

# from __future__ import division
import random
import math


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
