# -*- coding: utf-8 -*-
"""
@Time ： 2024/3/29 19:32
@Auth ： 锋
@File ：报警.py
@IDE ：PyCharm
@Motto：ABC(Always Be Coding)

"""
import math
import os.path
import random
import re
import time
from socket import *

import schedule as schedule
from configobj import ConfigObj




def get_longitude(base_log=None, radius=None):
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


def get_bcc(inputStr: str) -> str:
    bcc = 0
    for i in inputStr.split(' '):
        bcc = bcc ^ int(i, 16)

    return f'{bcc:x}'


def get_xor(data):
    result = re.sub(r"(?<=\w)(?=(?:\w\w)+$)", " ", data)
    return result


class login:
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

    def get(self):
        count = 0
        for i in range(1):
            now_time = time.strftime('%Y%m%d%H%M%S', time.localtime())
            时间 = now_time[2:]
            上车 = 时间[6:8].replace(f"{时间[6:8]}", "%02d" % (int(时间[6:8]) + 1))
            时间1 = now_time[2:8] + 上车 + 时间[:][8:]
            print(时间1)
            print(时间1[:10] + "01")
            下车 = 时间[6:8].replace(f"{时间[6:8]}", "%02d" % (int(时间[6:8]) + 2))
            print(下车 + 时间[:10][8:])
            print(时间1[:10] + "00")
            numbers = [
                # 人证匹配签到
                f'0B0300430158752260340020000000000000030000C7166903F5C10700C814{时间}534E3132333435363738390000000000534E3132333435363738393132333435363738534E3132343520240330095701040000006E0202044C250400000000300103',
                # # #超时运营报警
                f'0B0500730158752260340001000000010000010000C640B903F7CAAC001301{时间1}000000000000004000C7166903F5C1070031042403300951483590AA283590AA2801000000000001534E31323535534E3132333435363738393100000000534E3132333435363738393132333435363738{时间1[:8] + "01"}{下车 + 时间[:10][8:]}000{random.randint(30, 36)}001500000110110000{random.randint(10, 12)}0000000000001040000008E0202044C250400000000300103',
                # 人证不匹配报警
                f'0B0300430158752260340017000000000000030000C7166903F5C10700C820{now_time[2:]}534E3132333435363738390000000000534E3132333435363738393132333435363739534E3132343520240329193401040000006E0202044C250400000000300103',

            ]
            标识位 = '7E'
            for w in numbers:
                a = get_xor(w)
                b = get_bcc(a)
                E = w + b.upper().zfill(2)
                t = 标识位 + E.replace("7E", "00") + 标识位
                data = get_xor(t)
                if data[:2] != "7E":
                    print(f"错误：{data}")
                    t = t[:81] + "00" + t[82:]
                    data = get_xor(t)
                    print("修改后data：{}".format(data))
                    print('\n' * 1)
                print(t)
                print(data)
                count += 1

                s = socket(AF_INET, SOCK_STREAM)
                s.settimeout(10)  # 设置超时时间

                s.connect((self.wg, int(self.wg_port)))  # 测试
                s.send(bytes().fromhex(data))
                send = s.recv(1024).hex()
                print('服务器应答：' + send.upper())
                print('\n' * 1)


    def send_data(self):
        # countdown(1)
        now_time = time.strftime('%Y%m%d%H%M%S', time.localtime())
        标识位 = '7E'
        时间 = now_time[2:]
        print(时间)
        上车 = 时间[6:8].replace(f"{时间[6:8]}", "%02d" % (int(时间[6:8]) + 1))
        w = f'0B0500730158752260340001000000010000010000C640B903F7CAAC001301{now_time[2:]}000000000000004000C7166903F5C1070031042403300951483590AA283590AA2801000000000001534E31323535534E3132333435363738393100000000534E3132333435363738393132333435363738{now_time[2:][:8] + "00"}{上车 + 时间[:10][8:]}000{random.randint(30, 36)}001500000110110000{random.randint(10, 12)}0000000000001040000008E0202044C250400000000300103',
        a = get_xor(w)
        b = get_bcc(a)
        E = w + b.upper().zfill(2)
        t = 标识位 + E.replace("7E", "00") + 标识位
        data = get_xor(t)
        if data[:2] != "7E":
            print(f"错误：{data}")
            t = t[:81] + "00" + t[82:]
            data = get_xor(t)
            print("修改后data：{}".format(data))
            print('\n' * 1)
        print(t)
        print(data)
        # s = socket(AF_INET, SOCK_STREAM)
        # s.settimeout(10)  # 设置超时时间

        # s.connect((self.wg, int(self.wg_port)))  # 测试
        # s.send(bytes().fromhex(data))
        # send = s.recv(1024).hex()
        # print('服务器应答：' + send.upper())
        # print('\n' * 1)


import time


def countdown(hours):
    seconds = hours * 3600
    while seconds > 0:
        print(f"\r{seconds // 3600}小时{seconds % 3600 // 60}分钟{seconds % 60}秒", end='')
        time.sleep(1)
        seconds -= 1
    print("倒计时结束！")


if __name__ == '__main__':
    pass
    # while True:
    #     ll = login()
    #     ll.get()
    # ll.send_data()
