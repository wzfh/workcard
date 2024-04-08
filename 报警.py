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


current_directory = os.getcwd()
print(current_directory)


class login:
    def __init__(self):
        conf_ini = current_directory + "\\conf\\config.ini"
        config = ConfigObj(conf_ini, encoding='UTF-8')
        self.wg = config['ces']['出租车_cswg']
        self.wg_port = config['ces']['出租车_cs808wg_port']
        self.wg905_port = config['ces']['出租车_cs905wg_port']
        self.wd = config['address']['茂名市WD']
        self.jd = config['address']['茂名市JD']
        self.baojing = config['808baojing']
        self.baojing905 = config['905baojing']
        self.ztai = config['808ztai']
        self.ztai905 = config['905ztai']
        self.sbei = config['sbei']['808sbei']
        self.sbei905 = config['sbei']['905sbei']

    # 808报警
    def get(self):
        count = 0
        for i in range(1):
            now_time = time.strftime('%Y%m%d%H%M%S', time.localtime())
            wd1 = self.wd
            wd2 = float(wd1) * 1000000
            wd3 = hex(int(wd2))
            jd1 = self.jd
            jd2 = float(jd1) * 1000000
            jd3 = hex(int(jd2))
            标识位 = '7E'
            消息ID = '0200'
            油耗消息体属性 = '002F'
            设备号 = '0' + self.sbei
            print(f"设备号:{设备号}")

            流水号 = f'{i}'.zfill(4)
            baojlxs = [
                self.baojing['紧急报警'], self.baojing['超速报警'], self.baojing['疲劳驾驶'],
                self.baojing['LED顶灯故障'],
                self.baojing['进出区域路线报警'],
                self.baojing['路段行驶时间不足'], self.baojing['禁行路段行驶'], self.baojing['车辆非法点火'],
                self.baojing['车辆非法位移'], self.baojing['所有清零报警'],
                self.baojing['正常'], self.baojing['危险预警'], self.baojing['模块故障'], self.baojing['模块开路'],
                self.baojing['终端欠压'], self.baojing['终端掉电'],
                self.baojing['终端LCD故障'],
                self.baojing['TTS故障'], self.baojing['摄像头故障'], self.baojing['当天累计驾驶时长'],
                self.baojing['超时停车']
            ]
            报警 = random.choice(baojlxs)
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
            高程 = f'00{random.randint(10, 15)}'
            速度 = f'00{random.randint(10, 15)}'
            方向 = f'00{random.randint(10, 15)}'
            时间 = now_time[2:]
            附加里程 = f'0104000000{random.randint(10, 15)}'
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
            data = get_xor(t)
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
            return '\n808普通报警应答：' + send.upper()

    # 粤标报警
    def get1(self):

        for i in range(1):
            now_time = time.strftime('%Y%m%d%H%M%S', time.localtime())
            wd1 = self.wd
            wd2 = float(wd1) * 1000000
            print(int(wd2))
            wd3 = hex(int(wd2))
            jd1 = self.jd
            jd2 = float(jd1) * 1000000
            jd3 = hex(int(jd2))
            print(jd3[2:].zfill(8).upper())
            协议版本号 = '01'
            a = f'{self.sbei}'.zfill(20)
            纬度 = wd3[2:].zfill(8).upper()
            经度 = jd3[2:].zfill(8).upper()
            速度 = '000B'
            时间 = now_time[2:]
            bz = ["01", "02"]
            标志状态 = random.choice(bz)
            baojlxs = ["01", "02", "03", "04", "05", "06", "07", "0C"]
            报警事件类型 = random.choice(baojlxs)
            终端ID = f'{a}'.zfill(60)
            报警标识号 = f'{终端ID}{时间}00000000'
            附加信息65 = f'653600000001{标志状态}{报警事件类型}010500000000100000{纬度}{经度}{时间}{报警标识号}'
            长度 = '4063'
            data = f'0200{长度}{协议版本号}{a}00010000000000000000{纬度}{经度}0000{速度}000C{时间}' + 附加信息65
            a = get_xor(data)
            b = get_bcc(a)
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

            s = socket(AF_INET, SOCK_STREAM)
            s.settimeout(10)  # 设置超时时间

            s.connect((self.wg, int(self.wg_port)))  # 测试
            s.send(bytes().fromhex(data))
            send = s.recv(1024).hex()
            print('服务器应答：' + send.upper())
            print('\n' * 1)
            return '\n粤标报警应答：' + send.upper()

    #苏标报警
    def get2(self):
        for i in range(1):
            now_time = time.strftime('%Y%m%d%H%M%S', time.localtime())
            wd1 = self.wd
            wd2 = float(wd1) * 1000000
            wd3 = hex(int(wd2))
            jd1 = self.jd
            jd2 = float(jd1) * 1000000
            jd3 = hex(int(jd2))
            纬度 = wd3[2:].zfill(8).upper()
            经度 = jd3[2:].zfill(8).upper()
            速度 = '0010'
            时间 = now_time[2:]
            bz = ["01", "02"]
            标志状态 = random.choice(bz)
            baojlxs = ["01", "02", "03", "04", "05", "06", "07", ]
            报警事件类型 = random.choice(baojlxs)
            print(报警事件类型)
            附加信息65 = f'652F00000001{标志状态}{报警事件类型}010500000000100000{纬度}{经度}{时间}000030303030303030{时间}000100'
            data = f'0200004D0{self.sbei}00010000000000000000{纬度}{经度}0000{速度}000C{时间}' + 附加信息65
            a = get_xor(data)
            b = get_bcc(a)
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
            print(t)

            s = socket(AF_INET, SOCK_STREAM)

            s.connect((self.wg, int(self.wg_port)))  # 测试
            s.send(bytes().fromhex(data))
            send = s.recv(1024).hex()
            print('服务器应答：' + send.upper())
            print('\n' * 1)
            return '\n苏标报警应答：' + send.upper()

    def ww1(self):
        now_time = time.strftime('%Y%m%d%H%M%S', time.localtime())
        wd2 = float(self.wd) * 60 / 0.0001
        wd3 = hex(int(wd2))
        jd2 = float(self.jd) * 60 / 0.0001
        jd3 = hex(int(jd2))
        标识位 = '7E'
        消息ID = '0200'
        消息体属性 = '0023'
        ISU标识 = self.sbei905  # 10位
        流水号 = f'{1}'.zfill(4)
        报警 = self.baojing905['超时停车']
        状态 = self.ztai905['ACC开和载客']
        纬度 = wd3[2:].zfill(8).upper()
        经度 = jd3[2:].zfill(8).upper()
        速度 = '00E3'
        方向 = '01'
        时间 = now_time[2:]
        附加里程 = f'0104000000{random.randint(10, 15)}'
        油量 = ['5208', '044C', '04B0']
        附加油量 = f'0202{random.choice(油量)}'
        w = 消息ID + 消息体属性 + ISU标识 + 流水号 + 报警 + 状态 + 纬度 + 经度 + 速度 + 方向 + 时间 + 附加里程 + 附加油量
        a = get_xor(w)
        b = get_bcc(a).zfill(2)
        E = w + b.upper()
        t = 标识位 + E.replace("7E", "00") + 标识位
        data = get_xor(t)
        if data[:2] != "7E":
            print(f"错误：{data}")
            print('\n' * 1)
            t = t[:81] + "00" + t[82:]
            data = get_xor(t)
            print("修改后data：{}".format(data))
            print('\n' * 1)
        print(t)
        print(data)
        s = socket(AF_INET, SOCK_STREAM)
        s.connect((self.wg, int(self.wg905_port)))  # 测试
        s.send(bytes().fromhex(data))
        send = s.recv(1024).hex()
        print('服务器应答：' + send.upper())
        print('\n' * 1)
        return '\n服务器应答：' + send.upper()

    # 人证不匹配报警
    def get3(self):
        now_time = time.strftime('%Y%m%d%H%M%S', time.localtime())
        时间 = now_time[2:]
        nums = [
            f'0B030043{self.sbei905}0015000000000000030000C7166903F5C10700C819{时间}534E3132333435363738390000000000534E3132333435363738393132333435363739534E3132343520240403141701040000006E0202044C250400000000300103'
        ]
        for w in nums:
            a = get_xor(w)
            b = get_bcc(a)
            if b.upper() == "7E":
                a.replace("00", "01")
                b = get_bcc(a)
            E = w + b.upper().zfill(2)
            t = '7E' + E.replace("7E", "01") + '7E'
            data = get_xor(t)
            if data[:2] != "7E":
                print(f"错误：{data}")
                t = t[:81] + "00" + t[82:]
                data = get_xor(t)
                print("修改后data：{}".format(data))
                print('\n' * 1)
            print(data)
            print(t)
            s = socket(AF_INET, SOCK_STREAM)
            s.connect((self.wg, int(self.wg905_port)))  # 测试
            s.send(bytes().fromhex(data))
            send = s.recv(1024).hex()
            print('服务器应答：' + send.upper())
            print('\n' * 1)
            return '\n人证不匹配报警应答：' + send.upper()

    # 绕路报警
    def get4(self):
        now_time = time.strftime('%Y%m%d%H%M%S', time.localtime())
        时间 = now_time[2:]
        上车时间 = 时间[:10]
        上车 = 时间[6:8].replace(f"{时间[6:8]}", "%02d" % (int(时间[6:8]) + 1))
        上车时间1 = 时间[:8] + '00'
        下车时间 = 上车 + 上车时间[8:]
        nums = [
            f'0B050073{self.sbei905}0001000000010000010000C640B903F7CAAC001301{时间}000000000000004000C7166903F5C107003104{时间}3590AA283590AA2801000000000001534E31323535534E3132333435363738393100000000534E3132333435363738393132333435363738{上车时间1}{下车时间}000{random.randint(52, 56)}005200000120120000100000000020301040000008E0202044C250400000000300103'
        ]
        for w in nums:
            a = get_xor(w)
            b = get_bcc(a)
            if b.upper() == "7E":
                a.replace("00", "01")
                b = get_bcc(a)
            E = w + b.upper().zfill(2)
            t = '7E' + E.replace("7E", "01") + '7E'
            data = get_xor(t)
            if data[:2] != "7E":
                print(f"错误：{data}")
                t = t[:81] + "00" + t[82:]
                data = get_xor(t)
                print("修改后data：{}".format(data))
                print('\n' * 1)
            print(data)
            print(t)
            s = socket(AF_INET, SOCK_STREAM)
            s.connect((self.wg, int(self.wg905_port)))  # 测试
            s.send(bytes().fromhex(data))
            send = s.recv(1024).hex()
            print('服务器应答：' + send.upper())
            print('\n' * 1)
            return '\n绕路报警应答：' + send.upper()


def countdown(t):
    for i in range(t):
        print("\r休眠倒计时：%d" % (t - i) + '秒', end='')
        time.sleep(1)


if __name__ == '__main__':
    # while True:
    ll = login()
    ll.get()
    ll.get1()
    ll.get2()
    ll.ww1()
    ll.get3()
    ll.get4()
