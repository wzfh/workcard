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
    def qda(self, nob, noc):

        # for i in range(18,29):
            标识位 = '7E'
            消息ID = '0B01'
            消息体属性 = '002F'
            设备号 = f'1356000000'
            ISU标识 = '10{}'.format(设备号)  # 10位
            流水号 = f'{1}'.zfill(4)
            # print(i)
            # qw=hex(int(i))
            # 业务ID=f'{qw[2:]}'.zfill(8).upper()
            业务ID=f'223'.zfill(8).upper()

            # 附加='01040000006E0202044C250400000000300103'

            w = 消息ID + 消息体属性 + ISU标识 + 流水号 +业务ID
            a = get_xor(w)
            b = get_bcc(a)
            t = 标识位 + w + b.upper() + 标识位
            data = get_xor(t)
            print(t)
            print(data)

            # return '登录包数据：{}\n\n设备号：{}\n\n原始数据：{}'.format(t,t[12:-30],q)

            #
            s = socket(AF_INET, SOCK_STREAM)

            # s.connect(('47.119.168.112', 17800))
            s.connect(('120.79.74.223', 17800))
            s.send(bytes().fromhex(t))
            print('\n' * 1)
            time.sleep(2)
            s.close()
    def qr(self, nob, noc):
        for i in range(1):
            标识位 = '7E'
            消息ID = '0B07'
            消息体属性 = '002F'
            设备号 = f'1356000000'
            ISU标识 = '10{}'.format(设备号)  # 10位
            流水号 = f'{i}'.zfill(4)
            业务ID='222'.zfill(8)

            # 附加='01040000006E0202044C250400000000300103'

            w = 消息ID + 消息体属性 + ISU标识 + 流水号 +业务ID
            a = get_xor(w)
            b = get_bcc(a)
            t = 标识位 + w + b.upper() + 标识位
            data = get_xor(t)
            print(t)
            print(data)

            # return '登录包数据：{}\n\n设备号：{}\n\n原始数据：{}'.format(t,t[12:-30],q)

            #
            s = socket(AF_INET, SOCK_STREAM)
            # s.connect(('47.119.168.112', 17800))
            s.connect(('120.79.74.223', 17800))
            s.send(bytes().fromhex(t))
            print('\n' * 1)
            time.sleep(2)
            # s.close()
    def qx(self, nob, noc):
        for i in range(1):
            标识位 = '7E'
            消息ID = '0B08'
            消息体属性 = '002F'
            设备号 = f'1356000000'
            ISU标识 = '10{}'.format(设备号)  # 10位
            流水号 = f'{i}'.zfill(4)
            业务ID='221'.zfill(8)
            取消原因='01'

            # 附加='01040000006E0202044C250400000000300103'

            w = 消息ID + 消息体属性 + ISU标识 + 流水号 +业务ID +取消原因
            a = get_xor(w)
            b = get_bcc(a)
            t = 标识位 + w + b.upper() + 标识位
            data = get_xor(t)
            print(t)
            print(data)

            # return '登录包数据：{}\n\n设备号：{}\n\n原始数据：{}'.format(t,t[12:-30],q)

            #
            s = socket(AF_INET, SOCK_STREAM)
            s.connect(('120.79.74.223', 17800))
            s.send(bytes().fromhex(t))
            print('\n' * 1)
            time.sleep(2)
            s.close()


if __name__ == '__main__':
    ll = login()
    ll.qda(2, 1)
