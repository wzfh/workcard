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

# print(now_time[2:])

紧急报警='00000001'
超速报警='00010000'
LED顶灯故障='00008000'
进出区域路线报警='00100000'
路段行驶时间不足='00200000'
禁行路段行驶='00400000'
车辆非法点火='01000000'
车辆非法位移='02000000'
所有清零报警='03700000'
正常='00000000'
class login:
    def get(self):

        for i in range(1):
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

                # if i < 10:
                #     a = f'1113000000{i}'
                # elif 9 < i < 100:
                #     a = f'111300000{i}'
                # elif 99 < i < 1000:
                #     a = f'11130000{i}'
                # elif 999 < i < 10000:
                #     a = f'1113000{i}'
                # 设备号='0'+f'{a}'
                a='13859622221'
                长度='0A'
                消息体='00000000123456789100000000000000000000000000000000000000001234567891234500'
                data=f'010200{长度}0{a}000100013838383838383838'
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




            # return '登录包数据：{}\n\n设备号：{}\n\n原始数据：{}'.format(t,t[12:-30],q)


            #
                s = socket(AF_INET, SOCK_STREAM)
                # s = socket(AF_INET, SOCK_DGRAM)
                # s.connect(('120.77.26.175', 7788))
                # # s.connect(('120.79.176.183', 17700))  # 压测
                s.connect(('47.119.168.112', 17700))  # 生产
                s.send(bytes().fromhex(t))
                send = s.recv(1024).hex()
                print('服务器应答'+send.upper())
                print('\n' * 1)
                time.sleep(1)
                s.close()
            # except:
            #     continue


if __name__ == '__main__':
    ll = login()
    ll.get()
