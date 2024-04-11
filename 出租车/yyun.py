# coding=utf-8
import os
import random
import re
import time
from socket import socket, AF_INET, SOCK_STREAM

from configobj import ConfigObj


def get_bcc(inputStr: str) -> str:
    bcc = 0
    for i in inputStr.split(' '):
        bcc = bcc ^ int(i, 16)

    return f'{bcc:x}'


def get_xor(data):
    result = re.sub(r"(?<=\w)(?=(?:\w\w)+$)", " ", data)
    return result


紧急报警 = '00000001'
进出区域路线报警 = '00100000'
路段行驶时间不足 = '00200000'
禁行路段行驶 = '00400000'
车辆非法点火 = '01000000'
车辆非法位移 = '02000000'
正常 = '00000000'

未卫星定位 = '00000001'
南纬 = '00000002'
西经 = '00000004'
停运状态 = '00000008'
预约任务车 = '00000010'
空转重 = '00000020'
重转空 = '00000040'
ACC开 = '00000100'
重车 = '00000200'
车辆油路断开 = '00000400'
车辆电路断开 = '00000800'
车门加锁 = '00001000'
车辆锁定 = '00002000'
已达到限制营运次数时间 = '00004000'
ACC开和载客 = '00000300'


class login:
    def __init__(self):
        conf_ini = os.path.dirname(os.path.dirname(__file__)) + "\\conf\\config.ini"
        config = ConfigObj(conf_ini, encoding='UTF-8')
        self.wg = config['ces']['出租车_cswg']
        self.wg_port = config['ces']['出租车_cs905wg_port']
        self.wd = config['address']['茂名市WD']
        self.jd = config['address']['茂名市JD']
        self.wd1 = config['address']['规划WD']
        self.jd1 = config['address']['规划JD']
        self.baojing = config['905baojing']
        self.ztai = config['905ztai']
        self.sbei = config['sbei']['905sbei']
        self.驾驶员从业资格证号 = config['驾驶员从业资格证号']['欧先生']

    def get(self):
        hex_list = [hex(ord(char))[2:].upper() for char in self.驾驶员从业资格证号]
        驾驶员从业资格证号1 = ''.join(hex_list)
        for i in range(1):
            wd1 = float(self.wd) * 60 / 0.0001
            wd2 = float(self.wd1) * 60 / 0.0001
            wd3 = hex(int(wd1))
            wd4 = hex(int(wd2))

            jd1 = float(self.jd) * 60 / 0.0001
            jd2 = float(self.jd1) * 60 / 0.0001
            jd3 = hex(int(jd1))
            jd4 = hex(int(jd2))
            print(i)
            now_time = time.strftime('%Y%m%d%H%M%S', time.localtime())
            标识位 = '7E'
            消息ID = '0B05'
            消息体属性 = '0073'
            ISU标识 = self.sbei
            流水号 = f'0001'
            报警 = self.baojing['紧急报警']
            状态 = self.ztai['ACC开']
            纬度 = wd3[2:].zfill(8).upper()
            经度 = jd3[2:].zfill(8).upper()
            速度 = '0013'
            方向 = '01'
            时间 = now_time[2:]

            报警1 = self.baojing['正常']
            状态1 = self.ztai['重转空']
            纬度1 = wd4[2:].zfill(8).upper()
            经度1 = jd4[2:].zfill(8).upper()
            速度1 = '0031'
            方向1 = '04'
            时间1 = now_time[2:]

            营运ID = '3590AA28'  # 001101  0110  01000  01010 101000 101000
            评价ID = '3590AA28'
            评价选项 = '01'
            评价选项扩展 = '0000'
            电召订单ID = '1'.zfill(8)
            车牌号 = '534E31323535'  # SN1255
            企业经营许可证号 = '534E3132333435363738393100000000'  # SN1234567891
            驾驶员从业资格证号 = 驾驶员从业资格证号1
            上车时间 = 时间[:10]
            print(f'上车时间：{上车时间}')
            上车 = 时间[6:8].replace(f"{时间[6:8]}", "%02d" % (int(时间[6:8]) + 1))
            print(上车)
            上车时间1 = 时间[:8] + '00'
            print('ww:' + 上车时间1)
            下车时间 = 上车 + 上车时间[8:]
            print('ww:' + 下车时间)
            计程公里数 = f'000{random.randint(38, 42)}0'
            空驶里程 = f'0{random.randint(32, 40)}0'
            附加费 = f'0000{random.randint(10, 12)}'
            等待计时时间 = f'0{random.randint(10, 12)}0'
            交易金额 = f'000{random.randint(10, 12)}0'
            当前车次 = f'{2}'.zfill(8)
            交易类型 = '00'  # 0x00:现金交易：0x01:M1卡交易：0x03：CPU卡交易：0x09:其他
            附加 = '01040000008E0202044C250400000000300103'

            w = 消息ID + 消息体属性 + ISU标识 + 流水号 + 报警 + 状态 + 纬度 + 经度 + 速度 + 方向 + 时间 + 报警1 + 状态1 + 纬度1 + 经度1 + 速度1 + 方向1 + 时间1 + 营运ID + 评价ID + 评价选项 + 评价选项扩展 + 电召订单ID + 车牌号 + 企业经营许可证号 + 驾驶员从业资格证号 + 上车时间1 + 下车时间 + 计程公里数 + 空驶里程 + 附加费 + 等待计时时间 + 交易金额 + 当前车次 + 交易类型 + 附加
            a = get_xor(w)
            b = get_bcc(a)
            t = 标识位 + w + b.upper() + 标识位
            data = get_xor(t)
            print(t)
            print(data)
            #
            s = socket(AF_INET, SOCK_STREAM)
            s.connect((self.wg, int(self.wg_port)))

            s.send(bytes().fromhex(t))
            send = s.recv(1024).hex()
            print(send.upper())
            print('\n' * 1)
            time.sleep(1)


if __name__ == '__main__':
    ll = login()
    ll.get()
