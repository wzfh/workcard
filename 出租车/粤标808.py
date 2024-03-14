# coding=utf-8
import math
import os
import random
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
def countdown(t):
    for i in range(t):
        print("\r休眠倒计时：%d" % (t - i) + '秒', end='')
        time.sleep(1)


class login:
    def __init__(self):
        conf_ini = os.path.dirname(os.path.dirname(__file__)) + "\\conf\\config.ini"
        config = ConfigObj(conf_ini, encoding='UTF-8')
        self.wg = config['ces']['出租车_cswg']
        self.wg_port = config['ces']['出租车_cs808wg_port']
        self.wd = config['address']['茂名市WD']
        self.jd = config['address']['茂名市JD']
        self.baojing = config['808baojing']
        self.ztai = config['808ztai']
        self.sbei = config['sbei']['808sbei']

    def get(self):

        for i in range(1):
            now_time = time.strftime('%Y%m%d%H%M%S', time.localtime())
            wd1 = get_latitude(base_lat=23.012173, radius=15000)
            print(wd1)
            wd2 = float(wd1) * 1000000
            wd3 = hex(int(wd2))
            jd1 = get_longitude(base_log=114.340462, radius=10000)
            print(jd1)
            jd2 = float(jd1) * 1000000
            jd3 = hex(int(jd2))
            print(jd3[2:].zfill(8).upper())
            协议版本号 = '01'
            a = f'{self.sbei}'.zfill(20)
            状态 = '00000001'
            纬度 = wd3[2:].zfill(8).upper()
            经度 = jd3[2:].zfill(8).upper()
            速度 = '000B'
            时间 = now_time[2:]
            标志状态 = '01'
            baojlxs = ["01", "02", "03", "04", "05", "06", "07","0C" ]
            报警事件类型 = random.choice(baojlxs)
            终端ID = f'{a}'.zfill(60)
            报警标识号 = f'{终端ID}{时间}00000000'
            附加信息64 = f'643600000001{标志状态}{报警事件类型}011020000000100000{经度}{纬度}{时间}{报警标识号}'
            附加信息65 = f'653600000001{标志状态}{报警事件类型}010500000000100000{纬度}{经度}{时间}{报警标识号}'
            长度 = '4063'

            data = f'0200{长度}{协议版本号}{a}00010000000000000000{纬度}{经度}0000{速度}000C{时间}' + 附加信息65
            a = get_xor(data)
            b = get_bcc(a)
            # print(附加信息67)
            if b.upper() == "7E":
                a.replace("00", "01")
                b = get_bcc(a)
            E = data + b.upper().zfill(2)
            t = '7E' + E.replace("7E", "01") + '7E'
            data = get_xor(t)
            if data[:2] != "7E":
                print(f"错误：{data}")
                t = t[:81] + "00" + t[82:]
                data = get_xor(t)
                print("修改后data：{}".format(data))
                print('\n' * 1)
            print(data)
            # print(t)

            s = socket(AF_INET, SOCK_STREAM)
            s.settimeout(10)  # 设置超时时间

            s.connect((self.wg, int(self.wg_port)))  # 测试
            s.send(bytes().fromhex(data))
            send = s.recv(1024).hex()
            print('服务器应答：' + send.upper())
            print('\n' * 1)
            countdown(10)



if __name__ == '__main__':
    ll = login()
    while True:
        ll.get()
