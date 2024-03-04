# coding=utf-8
import binascii
import csv
import os
import re
import time
from socket import *

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
危险预警 = '00000002'
定位模块故障 = '00000004'
定位天线开路 = '00000008'
定位天线短路 = '00000010'
终端主电源欠压 = '00000020'
终端主电源掉电 = '00000040'
液晶LCD显示故障 = '00000080'
语音模块TTS故障 = '00000100'
摄像头故障 = '00000200'
超速报警 = '00010000'
疲劳驾驶 = '00020000'
当天累计驾驶超时 = '00040000'
超时停车 = '00080000'
车速传感器故障 = '00800000'
录音设备故障 = '08000000'
计价器故障 = '00000400'
服务评价器故障 = '00000800'
LED广告屏故障 = '00001000'
液晶LED显示屏故障 = '00002000'
安全访问模块故障 = '00004000'
LED顶灯故障 = '00008000'
计价器实时时钟 = '10000000'
进出区域路线报警 = '00100000'
路段行驶时间不足 = '00200000'
禁行路段行驶 = '00400000'
车辆非法点火 = '01000000'
车辆非法位移 = '02000000'
所有清零报警 = '03700000'
紧急报警和超速报警 = '00010001'
正常 = '00000000'


def countdown(t):
    for i in range(t):
        print("\r休眠倒计时：%d" % (t - i) + '秒', end='')
        time.sleep(1)


class login:
    # def __init__(self):
    #
    #     sbhaos = [
    #         '014569856655'
    #     ]
    #     for sbhao in sbhaos:
    #         self.sbhao = sbhao
    #         self.ww1()
    #         # continue
    #     # sys.exit()

    def ww1(self):
        try:
            global s, t
            path = os.path.dirname(__file__)
            # print(path)
            file_path = path + '/12.csv'
            fCase = open(file_path, 'r', encoding='gbk')
            datas = csv.reader(fCase)
            data1 = []
            o = 0
            for line in datas:
                data1.append(line)
            for nob1 in range(0, 1100):
                t = data1[nob1]
                o += 1
                print('发送第%d条' % o)
                now_time = time.strftime('%Y%m%d%H%M%S', time.localtime())
                # wd1 = get_latitude(base_lat=23.012173, radius=100000)
                # wd2 = float(wd1) * 60 / 0.0001
                wd2 = float(t[0]) * 60 / 0.0001
                wd3 = hex(int(wd2))
                # jd1 = get_longitude(base_log=114.348462, radius=100000)
                # jd2 = float(jd1) * 60 / 0.0001
                jd2 = float(t[1]) * 60 / 0.0001
                jd3 = hex(int(jd2))
                标识位 = '7E'
                消息ID = '0200'
                消息体属性 = '0023'
                # 设备号 = f'14569856655'
                # ISU标识 = '0{}'.format(设备号)  # 10位
                ISU标识 = '015265236688'  # 10位
                流水号 = f'{1}'.zfill(4)
                报警 = 正常
                状态 = '00000100'
                纬度 = wd3[2:].zfill(8).upper()
                经度 = jd3[2:].zfill(8).upper()
                速度 = '00E3'
                方向 = '01'
                时间 = now_time[2:]
                里程s = ['1A', '5E', '4F']
                附加里程 = f'0104000000{random.choice(里程s)}'
                油量 = ['5208', '044C', '04B0']
                附加油量 = f'0202{random.choice(油量)}'
                w = 消息ID + 消息体属性 + ISU标识 + 流水号 + 报警 + 状态 + 纬度 + 经度 + 速度 + 方向 + 时间 + 附加里程 + 附加油量
                a = get_xor(w)
                b = get_bcc(a).zfill(2)
                E = w + b.upper()
                t = 标识位 + E.replace("7E", "00") + 标识位
                D = get_xor(E)
                data = '7E ' + D + ' 7E'
                if data[:2] != "7E":
                    print(f"错误：{data}")
                    print('\n' * 1)
                    # print(t[80:])
                    t = t[:81] + "00" + t[82:]
                    # print("修改后t：{}".format(t))
                    data = get_xor(t)
                    print("修改后data：{}".format(data))
                    print('\n' * 1)
                print(t)
                # print('\n' * 1)
                print(data)
                s = socket(AF_INET, SOCK_STREAM)
                s.connect(('120.79.74.223', 17202))  # 测试
                # s.connect(('120.79.176.183', 17800))#压测
                # s.connect(('47.119.168.112', 17800))#生产
                s.send(bytes().fromhex(data))
                send = s.recv(1024).hex()
                print('服务器应答：' + send.upper())
                print('\n' * 1)
                countdown(10)
        except:
            pass


if __name__ == '__main__':
    while True:
        login().ww1()
