import csv
import math
import os
import random
import re
import time
from socket import *


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


def countdown(t):
    for i in range(t):
        print("\r休眠倒计时：%d" % (t - i) + '秒', end='')
        time.sleep(1)


class login:
    def __init__(self):

        self.ww1()
        # sbhaos = [
        # "015875226032",
        # "015875226033",
        # "015875226034",
        # "015875226035",
        # "015875226036",
        # '013433663399',
        # "015875226037",
        # "015875226038",
        # "015875226039",
            # "015875226040",
            # "015875226041",
            # "015875226042",
            # "015875226043",
            # "015875226044",
            # "015875226045",
            # "015875226046",
            # "015875226047",
            # "015875226048",
            # "015875226049",
            # "015875226050",
            # "015875226051",
            # "015875226052",
            # "015875226053",
            # "015875226054",
            # "015875226030"
        # ]
        # for sbhao in sbhaos:
        #     self.sbhao = sbhao
        #     self.ww1()
            # continue
        # sys.exit()

    def ww1(self):
        try:

            path = os.getcwd()
            file_path = path + '/conf/12.csv'
            fCase = open(file_path, 'r', encoding='gbk')
            datas = csv.reader(fCase)
            data1 = []
            o = 0
            for line in datas:
                data1.append(line)
            for nob1 in range(0, 205):
                t = data1[nob1]
                o += 1
                print('发送第%d条' % o)
                now_time = time.strftime('%Y%m%d%H%M%S', time.localtime())
                消息ID = '0200'
                消息体属性 = '002F'
                设备号 = "013658596655"
                print(f'设备号:{设备号}')
                流水号 = f'{0}'.zfill(4)
                baojlxs = [
                    f'{紧急报警}', f'{超速报警}', f'{疲劳驾驶}', f'{LED顶灯故障}', f'{进出区域路线报警}',
                    f'{路段行驶时间不足}', f'{禁行路段行驶}', f'{车辆非法点火}', f'{车辆非法位移}', f'{所有清零报警}',
                    f'{正常}', f'{危险预警}', f'{模块故障}', f'{模块开路}', f'{终端欠压}', f'{终端掉电}', f'{终端LCD故障}',
                    f'{TTS故障}', f'{摄像头故障}', f'{当天累计驾驶时长}', f'{超时停车}'
                ]
                报警 = f'{紧急报警}'
                状态 = '00000003'
                wd2 = float(t[0]) * 1000000
                wd3 = hex(int(wd2))
                纬度 = wd3[2:].zfill(8).upper()
                jd2 = float(t[1]) * 1000000
                jd3 = hex(int(jd2))
                经度 = jd3[2:].zfill(8).upper()
                高程 = f'00{random.randint(12, 20)}'
                速度 = f'00{random.randint(12, 20)}'
                方向 = f'00{random.randint(12, 20)}'
                时间 = now_time[2:]
                附加里程 = f'0104000000{random.randint(12, 20)}'
                附加信息ID = '0202044C250400000000300103'
                w = 消息ID + 消息体属性 + 设备号 + 流水号 + 报警 + 状态 + 纬度 + 经度 + 高程 + 速度 + 方向 + 时间 + 附加里程 + 附加信息ID
                a = get_xor(w)
                b = get_bcc(a)
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

                s = socket(AF_INET, SOCK_STREAM)

                s.connect(('120.79.74.223', 17201))  # 测试
                # s.connect(('120.79.192.231', 7788))  # 测试
                s.send(bytes().fromhex(data))
                send = s.recv(1024).hex()
                print('服务器应答：' + send.upper())
                print('\n' * 1)
                countdown(3)
        except:
            pass


if __name__ == '__main__':
    # while True:
        login()
    # sched = BlockingScheduler()  # 设置定时任务，周一至周五 上午8.50自动打上班卡，下午6.10自动打下班卡
    # sched.add_job(login, 'cron', day_of_week='mon-sat', hour='11', minute='56')
    # sched.start()
