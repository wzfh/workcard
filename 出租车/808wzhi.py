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
超速报警 = '00000002'
疲劳驾驶 = '00000004'
LED顶灯故障 = '00008000'
进出区域路线报警 = '00100000'
路段行驶时间不足 = '00200000'
禁行路段行驶 = '00400000'
车辆非法点火 = '01000000'
车辆非法位移 = '02000000'
所有清零报警 = '03700000'
紧急报警和超速报警 = '00010001'
正常 = '00000000'
危险预警 = '00000008'
模块故障 = '00000010'
模块开路 = '00000040'
终端欠压 = '00000080'
终端掉电 = '00000100'
终端LCD故障 = '00000200'
TTS故障 = '00000400'
摄像头故障 = '00000800'
当天累计驾驶时长 = '00040000'
超时停车 = '00080000'


class login:
    def get(self):
        global s, t, 设备号
        count = 0

        for i in range(1):

            try:
                now_time = time.strftime('%Y%m%d%H%M%S', time.localtime())
                wd1 = f'23.013173'
                # wds = ['23.012171', '23.012271', '23.012371', '23.012471', '23.012571', '23.012671', '23.012771',
                #        '23.012871']
                # wd = random.choice(wds)
                # wd1 = get_latitude(base_lat=float(wd), radius=15000)
                wd2 = float(wd1) * 1000000
                print(int(wd2))
                wd3 = hex(int(wd2))
                jd1 = f'114.340462'
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
                # sbs = ['013829622585', '015474855555', '013652585555', '013526985544', '015326548554', '013526855522',
                #        '013526855521', '013526855544', '013526855532', '545465454556', '545465454559', '013534985577',
                #        '013525874455', '015869596655']
                sb = '013533663300'
                设备号 = f'{sb}'
                print(f'设备号:{设备号}')

                流水号 = f'{i}'.zfill(4)
                baojlxs = [
                    f'{紧急报警}', f'{超速报警}', f'{疲劳驾驶}', f'{LED顶灯故障}', f'{进出区域路线报警}',
                    f'{路段行驶时间不足}', f'{禁行路段行驶}', f'{车辆非法点火}', f'{车辆非法位移}', f'{所有清零报警}',
                    f'{正常}', f'{危险预警}', f'{模块故障}', f'{模块开路}', f'{终端欠压}', f'{终端掉电}',
                    f'{终端LCD故障}',
                    f'{TTS故障}', f'{摄像头故障}', f'{当天累计驾驶时长}', f'{超时停车}'
                ]
                报警 = random.choice(baojlxs)
                print(f'报警：{报警}')

                状态 = '00000002'
                纬度 = wd3[2:].zfill(8).upper()
                经度 = jd3[2:].zfill(8).upper()
                print(f'纬度:{纬度}' + ' ' + f'经度：{经度}')
                高程 = '0001'
                sdu = ['2A', '0A', '5C', '3D']
                速度 = f'005C'
                方向 = '000C'
                时间 = now_time[2:]
                里程s = ['1A', '5E', '4F']
                附加里程 = f'0104000000{random.choice(里程s)}'
                油量=['5208','044C','04B0']
                附加油量 = f'0202{random.choice(油量)}'
                附加信息ID = '250400000000300103'
                # 附加信息长度 = '04'
                # 附加信息 = f'00000001'
                # print(附加信息)
                # 附加='01040000006E0202044C250400000000300103'

                w = 消息ID + 油耗消息体属性 + 设备号 + 流水号 + 报警 + 状态 + 纬度 + 经度 + 高程 + 速度 + 方向 + 时间 + 附加里程  + 附加油量+附加信息ID
                a = get_xor(w)
                b = get_bcc(a)
                # print(附加信息67)
                if b.upper() == "7E":
                    a.replace("00", "01")
                    b = get_bcc(a)
                E = w + b.upper().zfill(2)
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
                print(t)
                count += 1

                # return '登录包数据：{}\n\n设备号：{}\n\n原始数据：{}'.format(t,t[12:-30],q)
                # while True:
                #     # # #
                s = socket(AF_INET, SOCK_STREAM)
                s.settimeout(10)  # 设置超时时间

                s.connect(('120.79.74.223', 17201))  # 测试
                # s.connect(('120.77.133.46', 7788))# 106开发测试
                # s.connect(('120.79.176.183', 17700))  # 压测
                # s.connect(('47.119.168.112', 17700))#生产
                s.send(bytes().fromhex(data))
                send = s.recv(1024).hex()
                print('服务器应答：' + send.upper())
                print('\n' * 1)
                countdown(1)



            # s.close()
            except:
                pass


def countdown(t):
    for i in range(t):
        print("\r休眠倒计时：%d" % (t - i) + '秒', end='')
        time.sleep(1)


if __name__ == '__main__':
    ll = login()
    # while True:
        # 执行任务的代码
    ll.get()
        # print("任务执行中...")

        # 暂停10秒
        # countdown(10)
        # print('\n')
