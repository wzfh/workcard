import math
import os.path
import random
import re
import time
from socket import *

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
        self.wg_port = config['ces']['出租车_cs808wg_port']
        self.wd = config['address']['茂名市WD']
        self.jd = config['address']['茂名市JD']
        self.baojing = config['808baojing']
        self.ztai = config['808ztai']
        self.sbei = config['sbei']['808sbei']

    def get(self):
        count = 0

        for i in range(61):
            now_time = time.strftime('%Y%m%d%H%M%S', time.localtime())
            wd1 = self.wd
            # wds = ['23.012171', '23.012271', '23.012371', '23.012471', '23.012571', '23.012671', '23.012771',
            #        '23.012871']
            # wd = random.choice(wds)
            # wd1 = get_latitude(base_lat=float(wd), radius=15000)
            wd2 = float(wd1) * 1000000
            print(int(wd2))
            wd3 = hex(int(wd2))
            jd1 = self.jd
            # jds = ['114.341461', '114.342461', '114.343461', '114.344461', '114.345461', '114.346461', '114.347461',
            #        '114.348461']
            # jd = random.choice(jds)
            # jd1 = get_longitude(base_log=float(jd), radius=10000)
            jd2 = float(jd1) * 1000000
            jd3 = hex(int(jd2))
            标识位 = '7E'
            消息ID = '0200'
            油耗消息体属性 = '002F'
            # 消息体属性 = '002B'
            # if i < 10:
            #     设备号 = f'01600000010{i}'
            # elif 9<i<100:
            #     设备号 = f'0160000001{i}'
            # elif 199<i<1000:
            #     设备号 = f'016000000{i}'
            # elif 99 < i < 1000:
            #     设备号 = '0'+f'11130000{i}'
            # elif 999 < i < 10000:
            #     设备号 = '0'+f'1113000{i}'

            # '013652585555', '013526985544', '015326548554', '013526855522',
            #        '013526855521', '013526855544', '013526855532', '545465454556', '545465454559', '013534985577',
            #        '013525874455', '015869596655']
            设备号 = '0' + self.sbei
            print(f"设备号:{设备号}")

            流水号 = f'{i}'.zfill(4)
            # baojlxs = [
            #     self.baojing['紧急报警'], self.baojing['超速报警'], self.baojing['疲劳驾驶'], self.baojing['LED顶灯故障'],
            #     self.baojing['进出区域路线报警'],
            #     self.baojing['路段行驶时间不足'], self.baojing['禁行路段行驶'], self.baojing['车辆非法点火'],
            #     self.baojing['车辆非法位移'], self.baojing['所有清零报警'],
            #     self.baojing['正常'], self.baojing['危险预警'], self.baojing['模块故障'], self.baojing['模块开路'],
            #     self.baojing['终端欠压'], self.baojing['终端掉电'],
            #     self.baojing['终端LCD故障'],
            #     self.baojing['TTS故障'], self.baojing['摄像头故障'], self.baojing['当天累计驾驶时长'],
            #     self.baojing['超时停车']
            # ]
            报警 = self.baojing['紧急报警']
            # ztai = [self.ztai['ACC开'],
            #         self.ztai['定位'],
            #         self.ztai['南纬'],
            #         self.ztai['ACC开和定位'],
            #         self.ztai['西经'],
            #         self.ztai['停运状态'],
            #         self.ztai['经纬度已经保密插件保密'],
            #         self.ztai['单北斗'],
            #         self.ztai['单GPS'],
            #         self.ztai['北斗GPS双模'],
            #         self.ztai['ACC开定位开北斗GPS空车'],
            #         self.ztai['ACC开定位开北斗GPS满载'],
            #         self.ztai['车辆油路断开'],
            #         self.ztai['车辆电路断开'],
            #         self.ztai['车门加锁']]
            状态 = self.ztai['ACC开定位开北斗GPS满载']
            纬度 = wd3[2:].zfill(8).upper()
            经度 = jd3[2:].zfill(8).upper()
            print(f'纬度:{纬度}' + ' ' + f'经度：{经度}')
            高程 = '0001'
            # sdu = ['5C']
            速度 = f'0000'
            方向 = '000C'
            时间 = now_time[2:]
            里程s = ['5A', '5E', '5F']
            附加里程 = f'0104000000{random.choice(里程s)}'
            油量 = ['5208', '044C', '04B0']
            附加油量 = f'0202{random.choice(油量)}'
            附加信息ID = '250400000000300103'
            # 附加信息长度 = '04'
            # 附加信息 = f'00000001'
            # print(附加信息)
            # 附加='01040000006E0202044C250400000000300103'

            w = 消息ID + 油耗消息体属性 + 设备号 + 流水号 + 报警 + 状态 + 纬度 + 经度 + 高程 + 速度 + 方向 + 时间 + 附加里程 + 附加油量 + 附加信息ID
            a = get_xor(w)
            b = get_bcc(a)
            if b.upper() == "7E":
                a.replace("00", "01")
                b = get_bcc(a)
            E = w + b.upper().zfill(2)
            t = '7E' + E.replace("7E", "01") + '7E'
            D = get_xor(E)
            data = 标识位 + D + f' {标识位}'
            if data[:2] != "7E":
                print(f"错误：{data}")
                t = t[:81] + "00" + t[82:]
                data = get_xor(t)
                print("修改后data：{}".format(data))
                print('\n' * 1)
            print(data)
            print(t)
            count += 1

            s = socket(AF_INET, SOCK_STREAM)
            s.settimeout(10)  # 设置超时时间

            s.connect((self.wg, int(self.wg_port)))  # 测试
            s.send(bytes().fromhex(data))
            send = s.recv(1024).hex()
            print('服务器应答：' + send.upper())
            print('\n' * 1)
            countdown(1)


def countdown(t):
    for i in range(t):
        print("\r休眠倒计时：%d" % (t - i) + '秒', end='')
        time.sleep(1)


if __name__ == '__main__':
    # while True:
        ll = login()
        ll.get()
