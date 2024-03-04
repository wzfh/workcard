import os
import threading
import time
import random
import math
from V3ku import *
from socket import *
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
from 出租车.V905ku import 报警标志, 车辆状态, 经纬度, 速度, 签退方式, 报警标志1, 车辆状态1, 经纬度1, 速度1, 评价选项, \
    电召订单ID, 交易类型

# coding=utf-8
import binascii
import re
import tkinter as tk
from tkinter.colorchooser import askcolor
from pygame import mixer

import ttkbootstrap as ttk

LOG_LINE_NUM = 0
init_window = ttk.Window()  # 实例化出一个父窗口

s = ttk.Style()  # 实例化Style
s.theme_use("superhero")
# menubar = Menu(init_window, tearoff=False)

now_time = time.strftime('%Y%m%d%H%M%S', time.localtime())
now_time1 = time.strftime('%H%M%S', time.localtime())


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
from PIL import Image, ImageTk, ImageSequence
import fnmatch

current_directory = os.getcwd()

# 设置MP3文件匹配模式
mp3_pattern = '*.mp3'
ico_pattern = '*.ico'
gif_pattern = '*.gif'


class MY_GUI(tk.Tk):

    def __init__(self, init_window_name):
        self.init_window_name = init_window_name

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
            流水号 = f'0001'
            报警 = self.sb_bj()
            状态 = self.sb_ztai()
            纬度 = wd2[2:].zfill(8).upper()
            经度 = jd2[2:].zfill(8).upper()
            速度 = self.sdu()[2:].zfill(4).upper()
            方向 = '00'
            时间 = now_time[2:]
            附加 = '0104000000020202044C250400000000300103'
            if self.sb_on() == '是':
                for i in range(int(su), int(plsu)):
                    ISU标识 = self.sb_hao().zfill(12)[:12 - len(f'{i}')] + f'{i}'
                    w = 消息ID + 消息体属性 + ISU标识 + 流水号 + 报警 + 状态 + 纬度 + 经度 + 速度 + 方向 + 时间 + 附加
                    a = get_xor(w)
                    b = get_bcc(a)
                    E = w + b.upper().zfill(2)
                    t = 标识位 + E.replace("7E", "00") + 标识位
                    data = get_xor(t)
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
                        s.send(bytes().fromhex(t))
                        send = s.recv(1024).hex()
                        print(send.upper())
                        print('\n' * 1)
                        tip_content = '服务器应答：\n{}\n\n'.format(send.upper())
                        self.result_data_Text1.insert(1.0, tip_content)
            else:
                for i in range(1):
                    ISU标识 = self.sb_hao().zfill(12)
                    w = 消息ID + 消息体属性 + ISU标识 + 流水号 + 报警 + 状态 + 纬度 + 经度 + 速度 + 方向 + 时间 + 附加
                    a = get_xor(w)
                    b = get_bcc(a)
                    E = w + b.upper().zfill(2)
                    t = 标识位 + E.replace("7E", "00") + 标识位
                    data = get_xor(t)
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
                        s.send(bytes().fromhex(t))
                        send = s.recv(1024).hex()
                        print(send.upper())
                        print('\n' * 1)
                        tip_content = '服务器应答：\n{}\n\n'.format(send.upper())
                        self.result_data_Text1.insert(1.0, tip_content)
        except:
            return "数据解析有误，查看是否数据填写错误，修改无误后，请重新点击生成数据"
        self.result_data_Text1.insert(1.0, "总计发送成功位置数据条数:{}\n\n".format(str(count)))
        showinfo("发送结果", "总计发送成功位置数据条数:  {}".format(str(count)))
        return "操作已完成"

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
            流水号 = f'{0}'.zfill(4)
            报警 = self.sb_bj2()
            状态 = self.sb_ztai2()
            纬度 = wd3[2:].zfill(8).upper()
            经度 = jd3[2:].zfill(8).upper()
            高程 = '0001'
            速度 = self.sdu2()[2:].zfill(4).upper()
            方向 = '0000'
            时间 = now_time[2:]
            附加信息ID = '01040000000B0202044C250400000000300103'
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
                    data = get_xor(t)
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
                        s.send(bytes().fromhex(t))
                        send = s.recv(1024).hex()
                        print(send.upper())
                        print('\n' * 1)
                        tip_content = '服务器应答：\n{}\n\n'.format(send.upper())
                        self.result_data_Text2.insert(1.0, tip_content)
            else:
                for i in range(1):
                    设备号 = self.sb_hao2().zfill(12)
                    w = 消息ID + 消息体属性 + 设备号 + 流水号 + 报警 + 状态 + 纬度 + 经度 + 高程 + 速度 + 方向 + 时间 + 附加信息ID
                    a = get_xor(w)
                    b = get_bcc(a)
                    if b.upper() == "7E":
                        a.replace("00", "01")
                        b = get_bcc(a)
                    E = w + b.upper().zfill(2)
                    t = 标识位 + E.replace("7E", "01") + 标识位
                    data = get_xor(t)
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
                        s.send(bytes().fromhex(t))
                        send = s.recv(1024).hex()
                        print(send.upper())
                        print('\n' * 1)
                        tip_content = '服务器应答：\n{}\n\n'.format(send.upper())
                        self.result_data_Text2.insert(1.0, tip_content)
        except:
            return "数据解析有误，查看是否数据填写错误，修改无误后，请重新点击生成数据"
        self.result_data_Text2.insert(1.0, "总计发送成功位置数据条数:{}\n".format(str(count)))
        showinfo("发送结果", "总计发送成功位置数据条数:  {}".format(str(count)))
        return "操作已完成\n\n"

    def qdao(self, su, plsu):
        count = 0
        for i in range(int(su), int(plsu)):
            try:
                now_time = time.strftime('%Y%m%d%H%M%S', time.localtime())
                wd1 = float(self.wd()) * 60 / 0.0001
                wd2 = hex(int(wd1))
                jd1 = float(self.jd()) * 60 / 0.0001
                jd2 = hex(int(jd1))
                标识位 = '7E'
                消息ID = '0B03'
                消息体属性 = '0043'
                ISU标识 = self.sb_hao().zfill(12)[:12 - len(f'{i}')] + f'{i}'
                流水号 = f'0001'
                报警 = self.sb_bj()
                状态 = self.sb_ztai()
                纬度 = wd2[2:].zfill(8).upper()
                经度 = jd2[2:].zfill(8).upper()
                速度 = self.sdu()[2:].zfill(4).upper()
                方向 = '00'
                时间 = now_time[2:]
                企业经营许可证号 = '534E3132333435363738390000000000'  # SN123456789
                驾驶员从业资格证号 = self.driver()  # SN12345678912345678
                车牌号 = '534E31323435'  # SN1234
                开机时间 = now_time[:12]
                附加 = '01040000006E0202044C250400000000300103'
                w = 消息ID + 消息体属性 + ISU标识 + 流水号 + 报警 + 状态 + 纬度 + 经度 + 速度 + 方向 + 时间 + 企业经营许可证号 + 驾驶员从业资格证号 + 车牌号 + 开机时间 + 附加
                a = get_xor(w)
                b = get_bcc(a)
                E = w + b.upper().zfill(2)
                t = 标识位 + E.replace("7E", "00") + 标识位
                data = get_xor(t)
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
                    s.send(bytes().fromhex(t))
                    send = s.recv(1024).hex()
                    print(send.upper())
                    print('\n' * 1)
                    tip_content = '服务器应答：\n{}\n\n'.format(send.upper())
                    self.result_data_Text1.insert(1.0, tip_content)
                else:
                    continue
            except:
                return "数据解析有误，查看是否数据填写错误，修改无误后，请重新点击生成数据"
        self.result_data_Text1.insert(1.0, "总计发送成功签到数据条数:{}\n\n".format(str(count)))
        showinfo("发送结果", "总计发送成功签到数据条数:  {}".format(str(count)))
        return "操作已完成"

    def qtui(self, su, plsu):
        count = 0
        for i in range(int(su), int(plsu)):
            try:
                now_time = time.strftime('%Y%m%d%H%M%S', time.localtime())
                wd1 = float(self.wd()) * 60 / 0.0001
                wd2 = hex(int(wd1))
                jd1 = float(self.jd()) * 60 / 0.0001
                jd2 = hex(int(jd1))
                标识位 = '7E'
                消息ID = '0B04'
                消息体属性 = '0043'
                设备号 = '1357000000'
                ISU标识 = self.sb_hao().zfill(12)[:12 - len(f'{i}')] + f'{i}'
                流水号 = f'0001'
                报警 = self.sb_bj()
                状态 = self.sb_ztai()
                纬度 = wd2[2:].zfill(8).upper()
                经度 = jd2[2:].zfill(8).upper()
                速度 = self.sdu()[2:].zfill(4).upper()
                方向 = '00'
                时间 = now_time[2:]
                企业经营许可证号 = '534E3132333435363738390000000000'  # SN123456789
                驾驶员从业资格证号 = self.driver()  # SN12345678912345678
                车牌号 = '534E31323435'  # SN1235
                计价器K值 = '0012'  # 计价12
                当班开机时间 = now_time[:12]
                当班关机时间 = now_time[:12]
                当班里程 = '000120'  # 格式为XXXXX.X(km)
                当班营运里程 = '000120'  # 格式为XXXXX.X(km)
                车次 = '0012'  # 车次12
                计时时间 = now_time1
                总计金额 = '000120'
                卡收金额 = '000120'
                卡次 = '0012'
                班间里程 = '0120'
                总计里程 = '00000120'
                总营运里程 = '00000120'
                单价 = '1200'  # 12.00块
                总营运次数 = '0000001A'  # 高位在前就是在后面
                if (i % 2) == 0:
                    签退方式 = '01'
                else:
                    签退方式 = '00'
                附加 = '01040000006E0202044C250400000000300103'
                w = 消息ID + 消息体属性 + ISU标识 + 流水号 + 报警 + 状态 + 纬度 + 经度 + 速度 + 方向 + 时间 + 企业经营许可证号 + 驾驶员从业资格证号 + 车牌号 + 计价器K值 + 当班开机时间 + 当班关机时间 + 当班里程 + 当班营运里程 + 车次 + 计时时间 + 总计金额 + 卡收金额 + 卡次 + 班间里程 + 总计里程 + 总营运里程 + 单价 + 总营运次数 + 签退方式 + 附加
                a = get_xor(w)
                b = get_bcc(a)
                E = w + b.upper().zfill(2)
                t = 标识位 + E.replace("7E", "00") + 标识位
                data = get_xor(t)
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
                    s.send(bytes().fromhex(t))
                    send = s.recv(1024).hex()
                    print(send.upper())
                    print('\n' * 1)
                    tip_content = '服务器应答：\n{}\n\n'.format(send.upper())
                    self.result_data_Text1.insert(1.0, tip_content)
                else:
                    continue
            except:
                return "数据解析有误，查看是否数据填写错误，修改无误后，请重新点击生成数据"
        self.result_data_Text1.insert(1.0, "总计发送成功签退数据条数:{}\n\n".format(str(count)))
        showinfo("发送结果", "总计发送成功签退数据条数:  {}".format(str(count)))
        return "操作已完成"

    def yyun(self, su, plsu):
        count = 0
        for i in range(int(su), int(plsu)):
            try:
                now_time = time.strftime('%Y%m%d%H%M%S', time.localtime())
                wd1 = float(self.wd()) * 60 / 0.0001
                wd2 = 32.330217 * 60 / 0.0001
                wd3 = hex(int(wd1))
                wd4 = hex(int(wd2))

                jd1 = 114.903551 * 60 / 0.0001
                jd2 = float(self.jd()) * 60 / 0.0001
                jd3 = hex(int(jd1))
                jd4 = hex(int(jd2))
                空转重 = '00000020'
                重转空 = '00000040'
                标识位 = '7E'
                消息ID = '0B05'
                消息体属性 = '0073'

                ISU标识 = self.sb_hao().zfill(12)[:12 - len(f'{i}')] + f'{i}'
                流水号 = f'0001'
                报警 = self.sb_bj()
                状态 = self.sb_ztai()
                纬度 = wd3[2:].zfill(8).upper()
                经度 = jd3[2:].zfill(8).upper()
                速度 = self.sdu()[2:].zfill(4).upper()
                方向 = '01'
                时间 = now_time[2:]

                报警1 = self.sb_bj()
                状态1 = self.sb_ztai()
                纬度1 = wd4[2:].zfill(8).upper()
                经度1 = jd4[2:].zfill(8).upper()
                速度1 = self.sdu()[2:].zfill(4).upper()
                方向1 = '01'
                时间1 = now_time[2:]

                营运ID = '3590AA28'  # 001101  0110  01000  01010 101000 101000
                评价ID = '3590AA28'
                评价选项 = '01'
                评价选项扩展 = '0000'
                电召订单ID = '200'.zfill(8)
                车牌号 = '534E31323535'  # SN1255
                企业经营许可证号 = '534E3132333435363738393100000000'  # SN1234567891
                驾驶员从业资格证号 = self.driver()  # SN12345678912345679
                上车时间 = 时间[:10]
                上车时间1 = 时间[:10].replace(f'{上车时间}', f'{int(上车时间) - 30}')
                下车时间 = 上车时间[6:]
                计程公里数 = '000010'
                空驶里程 = '0035'
                附加费 = '000020'
                等待计时时间 = '0200'
                交易金额 = '000120'
                当前车次 = f'{i}'.zfill(8)
                交易类型 = '09'  # 0x00:现金交易：0x01:M1卡交易：0x03：CPU卡交易：0x09:其他
                附加 = '01040000006E0202044C250400000000300103'

                w = 消息ID + 消息体属性 + ISU标识 + 流水号 + 报警 + 状态 + 纬度 + 经度 + 速度 + 方向 + 时间 + 报警1 + 状态1 + 纬度1 + 经度1 + 速度1 + 方向1 + 时间1 + 营运ID + 评价ID + 评价选项 + 评价选项扩展 + 电召订单ID + 车牌号 + 企业经营许可证号 + 驾驶员从业资格证号 + 上车时间1 + 下车时间 + 计程公里数 + 空驶里程 + 附加费 + 等待计时时间 + 交易金额 + 当前车次 + 交易类型 + 附加
                a = get_xor(w)
                b = get_bcc(a)
                E = w + b.upper().zfill(2)
                t = 标识位 + E.replace("7E", "00") + 标识位
                data = get_xor(t)
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
                    s.send(bytes().fromhex(t))
                    send = s.recv(1024).hex()
                    print(send.upper())
                    print('\n' * 1)
                    tip_content = '服务器应答：\n{}\n\n'.format(send.upper())
                    self.result_data_Text1.insert(1.0, tip_content)
                else:
                    continue
            except:
                return "数据解析有误，查看是否数据填写错误，修改无误后，请重新点击生成数据"
        self.result_data_Text1.insert(1.0, "总计发送成功营运数据条数:{}\n\n".format(str(count)))
        showinfo("发送结果", "总计发送成功营运数据条数:  {}".format(str(count)))
        return "操作已完成"

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
                # print(i)
                # qw=hex(int(i))
                # 业务ID=f'{qw[2:]}'.zfill(8).upper()
                业务ID = f'{self.yewid()}'.zfill(8).upper()

                # 附加='01040000006E0202044C250400000000300103'

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
                    s.send(bytes().fromhex(t))
                    send = s.recv(1024).hex()
                    print(send.upper())
                    print('\n' * 1)
                    tip_content = '服务器应答：\n{}\n\n'.format(send.upper())
                    self.result_data_Text3.insert(1.0, tip_content)
                else:
                    continue
            except:
                return "数据解析有误，查看是否数据填写错误，修改无误后，请重新点击生成数据"
        self.result_data_Text3.insert(1.0, "总计发送成功抢单数据条数:{}\n\n".format(str(count)))
        showinfo("发送结果", "总计发送成功抢单数据条数:  {}".format(str(count)))
        return "操作已完成"

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

                # 附加='01040000006E0202044C250400000000300103'

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
                    s.send(bytes().fromhex(t))
                    send = s.recv(1024).hex()
                    print(send.upper())
                    print('\n' * 1)
                    tip_content = '服务器应答：\n{}\n\n'.format(send.upper())
                    self.result_data_Text3.insert(1.0, tip_content)
                else:
                    continue
            except:
                return "数据解析有误，查看是否数据填写错误，修改无误后，请重新点击生成数据"
        self.result_data_Text3.insert(1.0, "总计发送成功完成订单数据条数:{}\n\n".format(str(count)))
        showinfo("发送结果", "总计发送成功完成订单数据条数:  {}".format(str(count)))
        return "操作已完成"

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
                    s.send(bytes().fromhex(t))
                    send = s.recv(1024).hex()
                    print(send.upper())
                    print('\n' * 1)
                    tip_content = '服务器应答：\n{}\n\n'.format(send.upper())
                    self.result_data_Text3.insert(1.0, tip_content)
                else:
                    continue
            except:
                return "数据解析有误，查看是否数据填写错误，修改无误后，请重新点击生成数据"
            self.result_data_Text3.insert(1.0, "总计发送成功取消订单数据条数:{}\n\n".format(str(count)))
            showinfo("发送结果", "总计发送成功取消订单数据条数:  {}".format(str(count)))
            return "操作已完成"

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
                # 伪ip = '58D8D858'
                # 伪ip = '81828CA2'
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
                data = get_xor(t)
                count += 1

                tip_content = '\n位置数据：\n{}\n源数据：\n{}\n'.format(data, t)
                self.result_data_Text4.insert(1.0, tip_content)
                time.sleep(float(self.times4()))
                if self.ip_on4() == '是':
                    s = socket(AF_INET, SOCK_DGRAM)
                    s.settimeout(5)
                    s.connect((f'{self.ip4()}', int(self.port4())))  # 生产
                    s.send(bytes().fromhex(t))
                    send = s.recv(1024).hex()
                    print(send.upper())
                    print('\n' * 1)
                    tip_content = '服务器应答：\n{}\n\n'.format(send.upper())
                    self.result_data_Text4.insert(1.0, tip_content)
                else:
                    continue
            except:
                return "数据解析有误，查看是否数据填写错误，修改无误后，请重新点击生成数据"
        self.result_data_Text4.insert(1.0, "总计发送成功位置数据条数:{}\n".format(str(count)))
        showinfo("发送结果", "总计发送成功位置数据条数:  {}".format(str(count)))
        return "操作已完成"

    def sb_hao4(self):
        sb = self.sbei_Text4.get().strip()
        return sb

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

        wd1 = get_latitude(base_lat=float(self.wd4()), radius=15000)
        jd1 = get_longitude(base_log=float(self.jd4()), radius=15000)
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

    def 标志位(self):
        标志位=self.init_data4_Text7.get().strip()
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

    def sdu2(self):
        sdu = self.sdu_Text2.get().strip()
        sdu1 = hex(int(sdu) * 10)
        return sdu1

    def times2(self):
        times = self.times_Text2.get().strip()
        return times

    def ip_on2(self):
        ip_on = self.ip_on_Text2.get().strip()
        return ip_on

    def button_mode2(self):
        global is_on
        # 确定它是开启还是关闭状态

        # if is_on:
        #     self.on_.config(text="随机关闭")
        wd1 = get_latitude(base_lat=float(self.wd部标()), radius=100000)
        jd1 = get_longitude(base_log=float(self.jd部标()), radius=100000)
        self.wd_Text2.delete(0, END)
        self.wd_Text2.insert(0, wd1)
        self.jd_Text2.delete(0, END)
        self.jd_Text2.insert(0, jd1)

    def getMon(self, items):
        inits = self.init_data_Text1.get()
        if inits == "2" or inits == "3" or inits == "4":
            items = ("534E3132333435363738393132333435363739", "534E3132333435363738393132333435363738")
        else:
            pass
        self.driver_Text["values"] = items

    def getMon1(self, items):
        inits = self.init_data2_Text7.get()
        if inits == "苏标" :
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

        wd1 = get_latitude(base_lat=float(self.wd()), radius=100000)
        jd1 = get_longitude(base_log=float(self.jd()), radius=100000)
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
        for i in range(1):
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
            data = w
            a = get_xor(data)
            t = a + ''
            q = w
            print(t)
            tip_content = 'V3登录包数据：\n{}\n\n设备号：{}\n\n源数据：{}\n'.format(t, t[12:-30], q)
            self.result_data_Text5.insert(1.0, tip_content)
            if self.ip_on5() == '是':
                s = socket(AF_INET, SOCK_STREAM)
                s.connect((f'{self.ip5()}', int(self.port5())))  # 生产
                s.send(bytes().fromhex(q))
                send = s.recv(1024).hex()
                print(send.upper())
                print('\n' * 1)
                tip_content = '服务器应答：\n{}\n\n'.format(send.upper())
                self.result_data_Text5.insert(1.0, tip_content)
            else:
                continue

    def dwei5(self):
        for i in range(1):
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
            print(w)
            data = w
            a = get_xor(data)
            t = a + ''
            q = w
            print(t)

            tip_content = 'V3定位包数据：{}\n\n源数据：{}\n'.format(t, w)
            self.result_data_Text5.insert(1.0, tip_content)
            if self.ip_on5() == '是':
                s = socket(AF_INET, SOCK_STREAM)
                s.connect((f'{self.ip5()}', int(self.port5())))  # 生产
                s.send(bytes().fromhex(q))
                send = s.recv(1024).hex()
                print(send.upper())
                print('\n' * 1)
                tip_content = '服务器应答：\n{}\n\n'.format(send.upper())
                self.result_data_Text5.insert(1.0, tip_content)
            else:
                continue

            # tip_content = 'V3定位包数据：{}\n\n源数据：{}\n服务器应答：\n{}\n\n'.format(t, w, send.upper())

    def beep5(self):
        for i in range(1):
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
            bjs = ["03", "00", "02", "04", "05", "06", "0D", "0E", "09", "01", "11", "12", "10", "0A", "0C", "0F", "40",
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
            q = w
            print(t)
            tip_content = 'V3报警包数据：{}\n\n源数据：{}\n'.format(t, w)
            self.result_data_Text5.insert(1.0, tip_content)
            if self.ip_on5() == '是':
                s = socket(AF_INET, SOCK_STREAM)
                s.connect((f'{self.ip5()}', int(self.port5())))  # 生产
                s.send(bytes().fromhex(q))
                send = s.recv(1024).hex()
                print(send.upper())
                print('\n' * 1)
                tip_content = '服务器应答：\n{}\n\n'.format(send.upper())
                self.result_data_Text5.insert(1.0, tip_content)
            else:
                continue

    def pant5(self):
        for i in range(1):
            qsw = '7878'
            cwjy = '0A1377060300010003'
            cwjy1 = crc1(cwjy)[2:].upper()
            tzw = '0D0A'
            w = qsw + cwjy + cwjy1 + tzw
            a = get_xor(w)
            t = a + ''
            q = w
            print(t)
            tip_content = 'V3心跳包数据：{}\n\n源数据：{}'.format(t, w)
            self.result_data_Text5.insert(1.0, tip_content)
            if self.ip_on5() == '是':
                s = socket(AF_INET, SOCK_STREAM)
                s.connect((f'{self.ip5()}', int(self.port5())))  # 生产
                s.send(bytes().fromhex(q))
                send = s.recv(1024).hex()
                print(send.upper())
                print('\n' * 1)
                tip_content = '服务器应答：\n{}\n\n'.format(send.upper())
                self.result_data_Text5.insert(1.0, tip_content)
            else:
                continue

    def str_trans_to_md6(self):
        src = self.init_data1_Text6.get(1.0, END).strip()
        return src

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
                                           f'\n      企业经营许可证号：{data[76:108]}\n   驾驶员从业资格证号：{data[108:146]}'
                                           f'\n      车牌号：{data[146:158]}'
                                           f'\n    开机时间：{data[158:170][:4]}年{data[158:170][4:6]}月{data[158:170][6:8]}日 {data[158:170][8:10]}时{data[158:170][10:12]}分'
                                           f'\n      附加信息（未解）{data[170:-4]}')
        elif data[2:6] == '0B04':
            self.result_data1_Text6.delete(1.0, END)
            self.result_data1_Text6.insert(1.0,
                                           f'签退数据包:{data[2:6]}\n设备号：{data[10:22]}\n{报警标志(data)},\n{车辆状态(data)},\n      {经纬度(data)}'
                                           f'\n      {速度(data)},\n      方向：{data[62:64]}'
                                           f'\n      时间：20{data[64:76][:2]}年{data[64:76][2:4]}月{data[64:76][4:6]}日 {data[64:76][6:8]}时{data[64:76][8:10]}分{data[64:76][10:12]}秒'
                                           f'\n      企业经营许可证号：{data[76:108]}\n   驾驶员从业资格证号：{data[108:146]}'
                                           f'\n    车牌号：{data[146:158]}'
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
                                           f'\n      车牌号：{data[156:168]}'
                                           f'\n企业经营许可证号：{data[168:200]}'
                                           f'\n驾驶员从业资格证号：{data[200:238]}'
                                           f'\n上车时间：20{data[238:248][:2]}年{data[238:248][2:4]}月{data[238:248][4:6]}日 {data[238:248][6:8]}时{data[238:248][8:10]}分'
                                           f'\n下车时间：{data[248:252][:2]}时{data[248:252][2:4]}分'
                                           f'\n计程公里数：{int(data[252:258]) * 0.1}  空驶里程：{int(data[258:262]) * 0.1}  附加费：{int(data[262:268]) * 0.1}'
                                           f'\n等待计时时间：{data[268:272][:2]}时{data[268:272][2:4]}分   交易金额：{int(data[272:278]) * 0.1}  当前车次：{int(bin(int(data[278:286], 16))[2:], 2)}'
                                           f'\n交易类型：{交易类型(data)}'
                                           f'\n附加：{data[288:-4]}')
        else:
            self.result_data1_Text6.delete(1.0, END)
            self.result_data1_Text6.insert(1.0, "请输入905原始数据")
            return 0

    def xieyihao(self):
        data = self.str_trans_to_md5()
        data1 = get_xor(data)
        sjutji = []

        # 7878110101234135484845480100320000016D3F0D0A
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
            # self.write_log_to_Text5("INFO:原始数据解析 False")
            return 0
        self.result_data1_Text5.delete(1.0, END)
        # self.result_data_Text.insert(1.0,data1)
        for line in sjutji:
            print(line)
            self.result_data1_Text5.insert(1.0, line)
        # self.write_log_to_Text5("INFO:原始数据解析 success")

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
                self.login5()
        elif src == '2':
            self.result_data_Text5.delete(1.0, END)
            self.dwei5()
        elif src == '3':
            self.result_data_Text5.delete(1.0, END)
            self.beep5()
        elif src == '4':
            self.result_data_Text5.delete(1.0, END)
            self.pant5()
        else:
            self.result_data_Text5.delete(1.0, END)
            self.result_data_Text5.insert(1.0,
                                          "请输入数字(登录数据包请按1,定位数据包请按2,报警数据包请按3,心跳数据包请按4")

    def 苏粤标生成808(self):
        设备号 = self.init_data1_Text7.get().strip()
        协议 = self.init_data2_Text7.get().strip()
        标志位 = self.init_data4_Text7.get().strip()
        now_time = time.strftime('%Y%m%d%H%M%S', time.localtime())
        wd1 = get_latitude(base_lat=23.012173, radius=15000)
        wd2 = float(wd1) / 0.000001
        wd3 = hex(int(wd2))
        jd1 = get_longitude(base_log=114.340462, radius=10000)
        jd2 = float(jd1) / 0.000001
        jd3 = hex(int(jd2))
        纬度 = wd3[2:].zfill(8).upper()
        经度 = jd3[2:].zfill(8).upper()
        速度 = '0010'
        时间 = now_time[2:]
        标志状态 = self.标志位()
        报警事件类型 = self.主动报警()
        if 协议 == '苏标':
            附加信息65 = f'652F00000001{标志状态}{报警事件类型}010500000000100000{纬度}{经度}{时间}000030303030303030{时间}000100'
            data = f'0200004D0{设备号}00010000000000000000{纬度}{经度}0000{速度}000C{时间}' + 附加信息65
            a = get_xor(data)
            b = get_bcc(a)
            if b.upper() == "7E":
                a.replace("00", "01")
                b = get_bcc(a)
            E = data + b.upper().zfill(2)
            t = '7E' + E.replace("7E", "01") + '7E'
            data1 = get_xor(t)
            self.result_data1_Text7.delete(1.0, END)
            self.result_data1_Text7.insert(1.0, f'\n\n{data1}')
            self.result_data1_Text7.insert(1.0, t, '\n')
        else:
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
            data = get_xor(t)
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

    def qo_send4(self):
        src = self.data_Text4.get().strip()
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

    # 设置窗口
    def set_init_window(self):
        import os
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
        self.init_window_name.title("协议整合工具_v8  作者 : 姚子奇")
        self.init_window_name.geometry('1100x618+450+200')
        # self.init_window_name.geometry('1100x655+450+200')

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
        items = ("47.119.168.112", "120.79.74.223", "120.79.176.183")
        self.ip_Text = Combobox(pane1, width=50, height=2, values=items)
        self.ip_Text.current(0)
        self.ip_Text.grid(row=1, column=0, sticky=W)
        #
        self.port_Text_label = Label(pane1, text="服务器Port")
        self.port_Text_label.grid(row=2, columnspan=2, sticky=N)
        items = ("17700", "17800")
        self.port_Text = Combobox(pane1, width=50, height=2, values=items)
        self.port_Text.current(1)
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
        items = ("101356000000", "101351000000")
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
        items = ("32.330217", "23.012173")
        self.wd_Text = Combobox(pane1, width=50, height=2, values=items)
        self.wd_Text.current(1)
        self.wd_Text.grid(row=9, column=0, sticky=N, columnspan=10)
        #
        self.jd_Text_label = Label(pane1, text="经度")
        self.jd_Text_label.grid(row=10, column=0)
        items = ("114.340462", "104.903551")
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
        self.sdu_Text_label.grid(row=16, column=11)
        items = ("10", "20", "30", "40")
        self.sdu_Text = Combobox(pane1, width=60, height=20, values=items)
        self.sdu_Text.current(1)
        self.sdu_Text.grid(row=17, column=11)
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

        items = ("47.119.168.112", "120.79.74.223", "120.79.176.183")
        self.ip_Text2 = Combobox(pane2, width=50, height=2, values=items)
        self.ip_Text2.current(0)
        self.ip_Text2.grid(row=1, column=0, sticky=W)
        #
        self.port_Text_label2 = Label(pane2, text="服务器Port")
        self.port_Text_label2.grid(row=2, columnspan=2, sticky=N)
        items = ("17700", "17800", "7788")
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
        items = ("10356000000", "10351000000")
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
        items = ("32.330217", "23.012173")
        self.wd_Text2 = Combobox(pane2, width=50, height=2, values=items)
        self.wd_Text2.current(1)
        self.wd_Text2.grid(row=9, column=0, sticky=N, columnspan=1)
        #
        self.jd_Text_label2 = Label(pane2, text="经度")
        self.jd_Text_label2.grid(row=10, column=0, columnspan=1, sticky=N)
        items = ("114.398462", "104.903551")
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
        self.sdu_Text_label2.grid(row=14, column=0, columnspan=1, sticky=N)
        items = ("10", "20", "30", "40")
        self.sdu_Text2 = Combobox(pane2, width=50, height=12, values=items)
        self.sdu_Text2.current(1)
        self.sdu_Text2.grid(row=15, column=0, )
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
        items = ("120.79.74.223", "47.119.168.112")
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
        items = ("101356000000", "101351000000")
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
        self.result_data_Text3 = Text(pane3, width=85, height=30, relief='solid')
        self.result_data_Text3.grid(row=1, column=11, rowspan=30, columnspan=15)
        #         # self.result_data_Text3.bind("<Button-3>", lambda x: rightKey(x, self.result_data_Text3))
        # 按钮
        self.str_trans_to_md5_button3 = Button(pane3, text="订单905发送", width=10,
                                               command=lambda: self.thread_it(self.qo_ddan))  # 调用内部方法  加()为直接调用
        self.str_trans_to_md5_button3.grid(row=5, column=10)

        pane4 = Frame()

        self.ip_Text_label4 = Label(pane4, text="服务器ip")
        self.ip_Text_label4.grid(row=2, column=0, columnspan=10, sticky=N)
        items = ("47.107.222.141", "47.119.168.112", "120.79.176.183")
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
        items = ("2", "10")
        self.su_Text4 = Combobox(pane4, width=50, height=2, values=items)
        self.su_Text4.current(0)
        self.su_Text4.grid(row=12, column=0, columnspan=10, sticky=N)

        # 2929组成数据
        self.sbei_Text_label4 = Label(pane4, text="2929伪ip设备8位")
        self.sbei_Text_label4.grid(row=13, column=0, columnspan=10, sticky=N)
        items = ("58D8D858", "81828CA2")
        self.sbei_Text4 = Combobox(pane4, width=50, height=2, values=items)
        self.sbei_Text4.current(0)
        self.sbei_Text4.grid(row=14, column=0, sticky=N, columnspan=10)
        # self.sbei_Text4.bind("<Button-3>", lambda x: rightKey(x, self.sbei_Text4))

        # 经纬度随机
        self.on_ = Button(pane4, text="随机经纬度", width=10, command=self.button_mode4)
        self.on_.grid(row=15, column=10)

        self.wd_Text_label4 = Label(pane4, text="纬度")
        self.wd_Text_label4.grid(row=15, column=0, columnspan=10, sticky=N)
        items = ("32.33021", "23.01217")
        self.wd_Text4 = Combobox(pane4, width=50, height=2, values=items)
        self.wd_Text4.current(1)
        self.wd_Text4.grid(row=16, column=0, sticky=N, columnspan=10)
        # self.wd_Text4.bind("<Button-3>", lambda x: rightKey(x, self.wd_Text4))

        self.jd_Text_label4 = Label(pane4, text="经度")
        self.jd_Text_label4.grid(row=17, column=0, columnspan=10, sticky=N)
        items = ("114.39846", "104.90355")
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
        self.fx_Text = Combobox(pane4, width=69, height=20, values=items)
        self.fx_Text.current(1)
        self.fx_Text.grid(row=22, column=11, sticky=N, columnspan=3)

        self.times_Text_label = Label(pane4, text="发送停顿时间")
        self.times_Text_label.grid(row=19, column=11)
        items = ("1", "0.5", "1.5", "2")
        self.times_Text4 = Combobox(pane4, width=69, height=20, values=items)
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
        items = ()
        self.data_Text4 = Combobox(pane4, width=50, height=2, values=items)
        self.data_Text4.grid(row=24, column=0, sticky=N)
        # self.data_Text4.bind("<Button-3>", lambda x: rightKey(x, self.init_data_Text4))

        self.result_Text4 = Button(pane4, text="发送", command=lambda: self.thread_it(self.qo_send4))
        self.result_Text4.grid(row=24, column=10, )
        # self.result_Text4.bind("<Button-3>", lambda x: rightKey(x, self.init_data_Text4))

        self.result_data_label4 = Label(pane4, text="输出结果：有返回，即发送成功")
        self.result_data_label4.grid(row=2, column=11)
        self.result_data_Text4 = Text(pane4, width=85, height=20, relief='solid')
        self.result_data_Text4.grid(row=4, column=11, rowspan=15, columnspan=15)
        # self.result_data_Text4.bind("<Button-3>", lambda x: rightKey(x, self.result_data_Text4))
        # 按钮
        self.str_trans_to_md5_button4 = Button(pane4, text="2929生成", width=10,
                                               command=lambda: self.thread_it(self.qo_login2929))
        self.str_trans_to_md5_button4.grid(row=12, column=10)

        pane5 = Frame()

        # v3组成数据
        self.sbei_Text_label5 = Label(pane5, text="设备号(V3设备号15位)")
        self.sbei_Text_label5.grid(row=0, sticky=N, columnspan=2)

        items = ("154854744888745", "145263966554789")
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
        items = ("47.52.50.49", "47.119.168.112", "120.79.176.183")
        self.ip_Text5 = Combobox(pane5, width=32, height=3, values=items)
        self.ip_Text5.current(0)
        self.ip_Text5.grid(row=5, column=0, columnspan=1, sticky=N)

        self.port_Text_label5 = Label(pane5, text="\n服务器Port")
        self.port_Text_label5.grid(row=4, column=1, columnspan=1)
        items = ("17700", "6695", "17800")
        self.port_Text5 = Combobox(pane5, width=32, height=3, values=items)
        self.port_Text5.current(1)
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

        #         # self.init_data_Text5.bind("<Button-3>", lambda x: rightKey(x, self.init_data_Text1))
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
        items = ("13829622585", "15263526699")
        self.init_data1_Text7 = Combobox(pane7, width=50, height=20, values=items)
        self.init_data1_Text7.current(0)
        self.init_data1_Text7.grid(row=0, column=1, columnspan=2, sticky=W)

        self.init_data2_label7 = Label(pane7, text="协议:")
        self.init_data2_label7.grid(row=1, column=0)
        items = ("苏标", "粤标")
        self.init_data2_Text7 = Combobox(pane7, width=50, height=20, values=items)
        self.init_data2_Text7.current(0)
        self.init_data2_Text7.grid(row=1, column=1, columnspan=2, sticky=W)
        self.init_data2_Text7.bind("<<ComboboxSelected>>", self.getMon1)

        self.init_data3_label7 = Label(pane7, text="主动报警:")
        self.init_data3_label7.grid(row=2, column=0)
        items=()
        self.init_data3_Text7 = Combobox(pane7, width=50, height=20, values=items)
        self.init_data3_Text7.grid(row=2, column=1, columnspan=2, sticky=W)

        self.init_data4_label7 = Label(pane7, text="标志位:")
        self.init_data4_label7.grid(row=3, column=0)
        items = ("开始", "结束")
        self.init_data4_Text7 = Combobox(pane7, width=50, height=20, values=items)
        self.init_data4_Text7.current(0)
        self.init_data4_Text7.grid(row=3, column=1, columnspan=2, sticky=W)

        self.result_data_label7 = Label(pane7, text="解析结果:")
        self.result_data_label7.grid(row=4, column=0, rowspan=2)
        self.result_data1_Text7 = Text(pane7, width=67, height=18, relief='solid')  # 处理结果展示
        self.result_data1_Text7.grid(row=4, column=1, sticky=W)
        # # 按钮
        self.str1_trans_to_md5_button7 = Button(pane7, text="苏粤标生成", width=10,
                                                command=lambda: self.thread_it(self.苏粤标生成808))  # 调用内部方法  加()为直接调用
        self.str1_trans_to_md5_button7.grid(row=1, column=11, sticky=W)

        def play_animation():
            # 打开GIF图像文件
            giffilename = []
            for filename in os.listdir(current_directory):
                # 如果文件名与MP3模式匹配，则打印文件名
                if fnmatch.fnmatch(filename, gif_pattern):
                    giffilename.append(filename)
            print(giffilename)
            image = Image.open(giffilename[2])
            image1 = Image.open(giffilename[0])
            frames = []
            frames1 = []
            for frame in ImageSequence.Iterator(image):
                frames.append(ImageTk.PhotoImage(frame))
            for frame in ImageSequence.Iterator(image1):
                frames1.append(ImageTk.PhotoImage(frame))

            # 创建一个标签显示GIF图像
            label = tk.Label(pane3, image=frames[0])
            label.grid(row=22, column=11, rowspan=10)

            label1 = tk.Label(pane3, image=frames[0])
            label1.grid(row=22, column=12, rowspan=10)

            label2 = tk.Label(pane3, image=frames[0])
            label2.grid(row=22, column=13, rowspan=10)

            label3 = tk.Label(pane4, image=frames1[0])
            label3.grid(row=21, column=11, rowspan=10)

            label4 = tk.Label(pane4, image=frames1[0])
            label4.grid(row=21, column=12, rowspan=10)
            #
            label5 = tk.Label(pane4, image=frames1[0])
            label5.grid(row=21, column=13, rowspan=10)

            # 播放动画
            def update_frame(frame_index):
                # 更新标签的图像
                label.configure(image=frames[frame_index])
                label1.configure(image=frames[frame_index])
                label2.configure(image=frames[frame_index])

                label3.configure(image=frames1[frame_index])
                label4.configure(image=frames1[frame_index])
                label5.configure(image=frames1[frame_index])

                # 获取下一帧的索引
                next_frame_index = (frame_index + 1) % len(frames)
                next_frame_index1 = (frame_index + 1) % len(frames1)

                # 在固定的时间间隔后调用更新函数
                pane3.after(50, update_frame, next_frame_index)
                # pane3.after(100, update_frame, next_frame_index1)

            # 开始动画
            update_frame(1)

        # play_animation()
        note.add(pane1, text='出租车905TCP发送')
        note.add(pane2, text='部标808TCP发送')
        note.add(pane3, text='抢答回复订单')
        note.add(pane4, text='2929协议UDP发送')
        note.add(pane5, text='V3协议解析生成')
        note.add(pane6, text='905协议解析')
        note.add(pane7, text='苏标粤标生成')
        note.grid()


# def mess():
#     # 创建askyesno()会话框
#     boo = askyesno("真的要走了吗", "臣退了，这一退就是一辈子！")
#     if boo == True:
#         init_window.quit()
def play_audio(filename):
    mixer.init()
    mixer.music.load(filename)
    mixer.music.play(4)


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


if __name__ == '__main__':
    gui4_start()
