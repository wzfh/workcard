import threading
import time
import random
import math
from dingwei import dwei
from beeper import beep
from pant import pant
from V3ku import *
from socket import *
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
# coding=utf-8
import binascii
import re
import tkinter as tk
from tkinter.colorchooser import askcolor

import ttkbootstrap as ttk
LOG_LINE_NUM = 0
init_window = ttk.Window()  # 实例化出一个父窗口

s=ttk.Style() #实例化Style
s.theme_use("superhero")
menubar = Menu(init_window, tearoff=False)

now_time = time.strftime('%Y%m%d%H%M%S', time.localtime())
now_time1 = time.strftime('%H%M%S', time.localtime())


def copy(editor, event=None):
    editor.event_generate("<<Copy>>")


def paste(editor, event=None):
    editor.event_generate('<<Paste>>')


def selectAll(editor, event=None):
    editor.tag_add('sel', '1.0', END)


def rightKey(event, editor):
    menubar.delete(0, END)
    menubar.add_command(label='复制', command=lambda: copy(editor))
    menubar.add_command(label='粘贴', command=lambda: paste(editor))
    menubar.add_command(label='全选', command=lambda: selectAll(editor))
    menubar.post(event.x_root, event.y_root)


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


class MY_GUI(tk.Tk):

    def __init__(self, init_window_name):
        self.init_window_name = init_window_name

    def wzhi905(self, su):
        count = 0
        for i in range(int(su)):
            try:
                now_time = time.strftime('%Y%m%d%H%M%S', time.localtime())
                wd1 = float(self.wd()) * 60 / 0.0001
                wd2 = hex(int(wd1))
                jd1 = float(self.jd()) * 60 / 0.0001
                jd2 = hex(int(jd1))
                标识位 = '7E'
                消息ID = '0200'
                消息体属性 = '002F'
                ISU标识 = self.sb_hao().zfill(12)  # 10位
                流水号 = f'0001'
                报警 = self.sb_bj()
                状态 = self.sb_ztai()
                纬度 = wd2[2:].zfill(8).upper()
                经度 = jd2[2:].zfill(8).upper()
                速度 = self.sdu()[2:].zfill(4).upper()
                方向 = '00'
                时间 = now_time[2:]
                附加 = '0104000000020202044C250400000000300103'
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
                print(t)
                print(data)
                count += 1
                s = socket(AF_INET, SOCK_STREAM)
                s.connect((f'{self.ip()}', int(self.port())))  # 生产
                s.send(bytes().fromhex(t))
                send = s.recv(1024).hex()
                print(send.upper())
                print('\n' * 1)
                tip_content = '位置数据：\n{}\n源数据：\n{}\n服务器应答：\n{}\n\n'.format(data, t, send.upper())
                self.result_data_Text1.insert(1.0, tip_content)
                time.sleep(float(self.times()))
                # s.close()
            except:
                return "数据解析有误，查看是否数据填写错误，修改无误后，请重新点击生成数据"
        self.result_data_Text1.insert(1.0, "总计发送成功位置数据条数:{}\n\n".format(str(count)))
        showinfo("发送结果", "总计发送成功位置数据条数:  {}".format(str(count)))

    # 部标位置
    def wzhi部标(self, su2):
        count = 0
        for i in range(int(su2)):
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
                设备号 = self.sb_hao2().zfill(12)
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
                s = socket(AF_INET, SOCK_STREAM)
                s.connect((f'{self.ip2()}', int(self.port2())))  # 生产
                s.send(bytes().fromhex(t))
                send = s.recv(1024).hex()
                print(send.upper())
                print('\n' * 1)
                tip_content = '位置数据：\n{}\n源数据：\n{}\n服务器应答：{}\n\n'.format(data, t, send.upper())
                self.result_data_Text2.insert(1.0, tip_content)
                time.sleep(float(self.times()))
                # s.close()
            except:
                return "数据解析有误，查看是否数据填写错误，修改无误后，请重新点击生成数据"
        self.result_data_Text2.insert(1.0, "总计发送成功位置数据条数:{}\n".format(str(count)))
        showinfo("发送结果", "总计发送成功位置数据条数:  {}".format(str(count)))

    def qdao(self, su):
        count = 0
        for i in range(int(su)):
            try:
                now_time = time.strftime('%Y%m%d%H%M%S', time.localtime())
                wd1 = float(self.wd()) * 60 / 0.0001
                wd2 = hex(int(wd1))
                jd1 = float(self.jd()) * 60 / 0.0001
                jd2 = hex(int(jd1))
                标识位 = '7E'
                消息ID = '0B03'
                消息体属性 = '0043'
                ISU标识 = self.sb_hao()  # 12位
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
                s = socket(AF_INET, SOCK_STREAM)
                s.connect((f'{self.ip()}', int(self.port())))  # 生产
                s.send(bytes().fromhex(t))
                send = s.recv(1024).hex()
                print(send.upper())
                print('\n' * 1)
                tip_content = '签到数据：\n{}\n源数据：{}\n服务器应答：\n{}\n\n'.format(data, t, send.upper())
                self.result_data_Text1.insert(1.0, tip_content)
                time.sleep(2)
            except:
                return "数据解析有误，查看是否数据填写错误，修改无误后，请重新点击生成数据"
        self.result_data_Text1.insert(1.0, "总计发送成功签到数据条数:{}\n\n".format(str(count)))
        showinfo("发送结果", "总计发送成功签到数据条数:  {}".format(str(count)))

    def qtui(self, su):
        count = 0
        for i in range(int(su)):
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
                ISU标识 = self.sb_hao()  # 10位
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
                s = socket(AF_INET, SOCK_STREAM)
                s.connect((f'{self.ip()}', int(self.port())))  # 生产
                s.send(bytes().fromhex(t))
                send = s.recv(1024).hex()
                print(send.upper())
                print('\n' * 1)
                tip_content = '签退数据：\n{}\n源数据：{}\n服务器应答：\n{}\n\n'.format(data, t, send.upper())
                self.result_data_Text1.insert(1.0, tip_content)
                time.sleep(2)
                s.close()
            except:
                return "数据解析有误，查看是否数据填写错误，修改无误后，请重新点击生成数据"
        self.result_data_Text1.insert(1.0, "总计发送成功签退数据条数:{}\n\n".format(str(count)))
        showinfo("发送结果", "总计发送成功签退数据条数:  {}".format(str(count)))

    def yyun(self, su):
        count = 0
        for i in range(int(su)):
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

                ISU标识 = self.sb_hao()  # 10位
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
                s = socket(AF_INET, SOCK_STREAM)
                s.connect((f'{self.ip()}', int(self.port())))  # 生产
                s.send(bytes().fromhex(t))
                send = s.recv(1024).hex()
                print(send.upper())
                print('\n' * 1)
                tip_content = '营运数据：\n{}\n源数据：{}\n服务器应答：\n{}\n\n'.format(data, t, send.upper())
                self.result_data_Text1.insert(1.0, tip_content)
                time.sleep(float(self.times()))
                # s.close()
            except:
                return "数据解析有误，查看是否数据填写错误，修改无误后，请重新点击生成数据"
        self.result_data_Text1.insert(1.0, "总计发送成功营运数据条数:{}\n\n".format(str(count)))
        showinfo("发送结果", "总计发送成功营运数据条数:  {}".format(str(count)))

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
                s = socket(AF_INET, SOCK_STREAM)
                s.connect((f'{self.ip3()}', int(self.port3())))  # 生产
                s.send(bytes().fromhex(t))
                send = s.recv(1024).hex()
                print(send.upper())
                print('\n' * 1)
                tip_content = '抢单数据：\n{}\n源数据：{}\n服务器应答：\n{}\n\n'.format(data, t, send.upper())
                self.result_data_Text3.insert(1.0, tip_content)
                # time.sleep(float(self.times()))
                print('\n' * 1)
                time.sleep(2)
                count += 1
            except:
                return "数据解析有误，查看是否数据填写错误，修改无误后，请重新点击生成数据"
        self.result_data_Text3.insert(1.0, "总计发送成功抢单数据条数:{}\n\n".format(str(count)))
        showinfo("发送结果", "总计发送成功抢单数据条数:  {}".format(str(count)))

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
                s = socket(AF_INET, SOCK_STREAM)
                s.connect((f'{self.ip3()}', int(self.port3())))  # 生产
                s.send(bytes().fromhex(t))
                send = s.recv(1024).hex()
                print(send.upper())
                print('\n' * 1)
                tip_content = '完成订单数据：\n{}\n源数据：{}\n服务器应答：\n{}\n\n'.format(data, t, send.upper())
                self.result_data_Text3.insert(1.0, tip_content)
                time.sleep(2)
                s.close()
                count += 1
            except:
                return "数据解析有误，查看是否数据填写错误，修改无误后，请重新点击生成数据"
        self.result_data_Text3.insert(1.0, "总计发送成功完成订单数据条数:{}\n\n".format(str(count)))
        showinfo("发送结果", "总计发送成功完成订单数据条数:  {}".format(str(count)))

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
                s = socket(AF_INET, SOCK_STREAM)
                s.connect((f'{self.ip3()}', int(self.port3())))  # 生产
                s.send(bytes().fromhex(t))
                send = s.recv(1024).hex()
                print(send.upper())
                print('\n' * 1)
                tip_content = '取消订单数据：\n{}\n源数据：{}\n服务器应答：\n{}\n\n'.format(data, t, send.upper())
                self.result_data_Text3.insert(1.0, tip_content)
                time.sleep(2)
                s.close()
                count += 1
            except:
                return "数据解析有误，查看是否数据填写错误，修改无误后，请重新点击生成数据"
            self.result_data_Text3.insert(1.0, "总计发送成功取消订单数据条数:{}\n\n".format(str(count)))
            showinfo("发送结果", "总计发送成功取消订单数据条数:  {}".format(str(count)))

    def wzhi2929(self,su4):
        count=0
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
                s = socket(AF_INET, SOCK_DGRAM)
                s.settimeout(5)
                s.connect((f'{self.ip4()}', int(self.port4())))  # 生产
                s.send(bytes().fromhex(t))
                send = s.recv(1024).hex()
                print(send.upper())
                print('\n' * 1)
                tip_content = '位置数据：\n{}\n源数据：\n{}\n服务器应答：{}\n\n'.format(data, t,send.upper())
                self.result_data_Text4.insert(1.0, tip_content)
                time.sleep(float(self.times4()))
                # s.close()
            except:
                return "数据解析有误，查看是否数据填写错误，修改无误后，请重新点击生成数据"
        self.result_data_Text4.insert(1.0, "总计发送成功位置数据条数:{}\n".format(str(count)))
        showinfo("发送结果", "总计发送成功位置数据条数:  {}".format(str(count)))

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
        port=self.port_Text4.get().strip()
        return port

    def sdu4(self):
        sdu=self.sdu_Text4.get().strip()
        return sdu

    def fx(self):
        fx=self.fx_Text.get().strip()
        return fx

    def times4(self):
        times=self.times_Text4.get().strip()
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

    def yewid(self):
        yewid = self.yewid_Text3.get().strip()
        yewid = hex(int(yewid))[2:]
        return yewid

    def str_trans_to_md5(self):
        src = self.init_data1_Text5.get(1.0,END).strip()
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
        elif sb == "超速报警":
            return '00010000'
        elif sb == "LED顶灯故障":
            return '00008000'
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

    def sb_hao2(self):
        sb = self.sbei_Text2.get().strip()
        return sb

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
        elif sb == "进出区域报警":
            return '00100000'
        elif sb == "路段行驶时间不足":
            return '00400000'
        elif sb == "车辆非法点火":
            return '08000000'
        elif sb == "车辆非法位移":
            return '10000000'
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
        label=Label(theme_selection, text="主题选择")
        label.grid(row=0,column=0)
        theme_cbo = ttk.Combobox(
            master=theme_selection,
            text=s.theme.name,
            values=theme_names,
            width=60, height=20,
        )
        theme_cbo.grid(row=1,column=0)
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

    def write_log_to_Text5(self, logmsg):
        global LOG_LINE_NUM
        current_time = self.get_current_time5()
        logmsg_in = str(current_time) + " " + str(logmsg) + "\n"  # 换行
        if LOG_LINE_NUM <= 7:
            self.log_data_Text5.insert(END, logmsg_in)
            LOG_LINE_NUM = LOG_LINE_NUM + 1
        else:
            self.log_data_Text5.delete(1.0, 2.0)
            self.log_data_Text5.insert(END, logmsg_in)

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

    def login5(self):
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

        return '登录包数据：{}\n\n设备号：{}\n\n原始数据：{}'.format(t, t[12:-30], q)

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
            self.write_log_to_Text5("INFO:原始数据解析 False")
            return 0
        self.result_data1_Text5.delete(1.0, END)
        # self.result_data_Text.insert(1.0,data1)
        for line in sjutji:
            print(line)
            self.result_data1_Text5.insert(1.0, line)
        self.write_log_to_Text5("INFO:原始数据解析 success")

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
                self.result_data_Text2.insert(1.0, self.wzhi部标(self.su2()))

    def qo_login2929(self):
        src = self.init_data_Text4.get().strip()
        print(src)
        if src == '1':
            sbb1=self.sb_hao4()
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
                self.result_data_Text1.insert(END, self.wzhi905(self.su()))
            # return 0
        elif src == '2':
            sbb1 = self.sb_hao()
            if not sbb1:
                self.result_data_Text1.delete(1.0, END)
                self.result_data_Text1.insert(1.0, "请输入设备号")
            else:
                self.result_data_Text1.delete(1.0, END)
                self.result_data_Text1.insert(END, self.qdao(self.su()))
        elif src == '3':
            sbb1 = self.sb_hao()
            if not sbb1:
                self.result_data_Text1.delete(1.0, END)
                self.result_data_Text1.insert(1.0, "请输入设备号")
            else:
                self.result_data_Text1.delete(1.0, END)
                self.result_data_Text1.insert(END, self.qtui(self.su()))
        elif src == '4':
            sbb1 = self.sb_hao()
            if not sbb1:
                self.result_data_Text1.delete(1.0, END)
                self.result_data_Text1.insert(1.0, "请输入设备号")
            else:
                self.result_data_Text1.delete(1.0, END)
                self.result_data_Text1.insert(END, self.yyun(self.su()))

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
                self.result_data_Text5.insert(1.0, self.login5())
                self.write_log_to_Text5("INFO:数据包生成 success")
            return 0
        elif src == '2':
            ll = dwei()
        elif src == '3':
            ll = beep()
            self.result_data_Text5.delete(1.0, END)
            self.result_data_Text5.insert(1.0, ll.get(14, 1))
        elif src == '4':
            ll = pant()
        else:
            self.result_data_Text5.delete(1.0, END)
            self.result_data_Text5.insert(1.0,
                                          "请输入数字(登录数据包请按1,定位数据包请按2,报警数据包请按3,心跳数据包请按4")
            self.write_log_to_Text5(
                "ERROR:数据包生成 failed,请输入数字(登录数据包请按1,定位数据包请按2,报警数据包请按3,心跳数据包请按4")
            return 0
        self.result_data_Text5.delete(1.0, END)
        self.result_data_Text5.insert(1.0, ll.get(2, 1))
        self.write_log_to_Text5("INFO:数据包生成 success")

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
        src = self.data_Text3.get(1.0,END).strip()
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

    # 设置窗口
    def set_init_window(self):
        # 905解析数据
        self.init_window_name.title("整合工具_v1  作者 : 姚子奇")
        self.init_window_name.geometry('1100x623+450+200')

        note = Notebook(init_window)
        self.init_window_name1 = Frame()


        self.init_window_name.menu = Menu(self.init_window_name1, tearoff=0)
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

        self.ip_Text_label = Label(self.init_window_name1, text="服务器ip")
        self.ip_Text_label.grid(row=2, column=0)
        items = ("120.79.74.223", "47.119.168.112", "120.79.176.183")
        self.ip_Text = Combobox(self.init_window_name1, width=50, height=2, values=items)
        self.ip_Text.current(0)
        self.ip_Text.grid(row=4, column=0, columnspan=10, sticky=N)

        self.port_Text_label = Label(self.init_window_name1, text="服务器Port")
        self.port_Text_label.grid(row=6, column=0)
        items = ("17700", "17800")
        self.port_Text = Combobox(self.init_window_name1, width=50, height=2, values=items)
        self.port_Text.current(1)
        self.port_Text.grid(row=8, column=0, columnspan=10, sticky=N)

        self.su_Text_label = Label(self.init_window_name1, text="循环次数")
        self.su_Text_label.grid(row=10, column=0)
        items = ("2", "10")
        self.su_Text = Combobox(self.init_window_name1, width=50, height=2, values=items)
        self.su_Text.current(0)
        self.su_Text.grid(row=12, column=0, columnspan=10, sticky=N)

        # 905组成数据
        self.sbei_Text_label = Label(self.init_window_name1, text="设备号(905设备号12位)")
        self.sbei_Text_label.grid(row=13, column=0)
        items = ("101356000000", "101351000000")
        self.sbei_Text = Combobox(self.init_window_name1, width=50, height=2, values=items)
        self.sbei_Text.current(0)
        self.sbei_Text.grid(row=14, column=0, sticky=N, columnspan=10)

        # 经纬度随机
        self.on_ = Button(self.init_window_name1, text="随机经纬度", width=10, command=self.button_mode)
        self.on_.grid(row=15, column=10)

        self.wd_Text_label = Label(self.init_window_name1, text="纬度")
        self.wd_Text_label.grid(row=15, column=0)
        items = ("32.330217", "23.012173")
        self.wd_Text = Combobox(self.init_window_name1, width=50, height=2, values=items)
        self.wd_Text.current(1)
        self.wd_Text.grid(row=16, column=0, sticky=N, columnspan=10)

        self.jd_Text_label = Label(self.init_window_name1, text="经度")
        self.jd_Text_label.grid(row=17, column=0)
        items = ("114.340462", "104.903551")
        self.jd_Text = Combobox(self.init_window_name1, width=50, height=2, values=items)
        self.jd_Text.current(0)
        self.jd_Text.grid(row=18, column=0, sticky=N, columnspan=10)

        self.baoj_Text_label = Label(self.init_window_name1, text="报警")
        self.baoj_Text_label.grid(row=19, column=0)
        items = (
            "紧急报警", "超速报警", "LED顶灯故障", "进出区域路线报警", "路段行驶时间不足", "禁行路段行驶",
            "车辆非法点火",
            "车辆非法位移", "所有实时报警", "正常")
        self.baoji_Text = Combobox(self.init_window_name1, width=50, height=12, values=items)
        self.baoji_Text.current(9)
        self.baoji_Text.grid(row=20, column=0, sticky=N, columnspan=10)

        self.times_Text_label = Label(self.init_window_name1, text="发送停顿时间")
        self.times_Text_label.grid(row=19, column=11)
        items = ("1", "0.5", "1.5", "2")
        self.times_Text = Combobox(self.init_window_name1, width=60, height=20, values=items)
        self.times_Text.current(0)
        self.times_Text.grid(row=20, column=11, sticky=N)

        self.init_data_label1 = Label(self.init_window_name1,
                                      text="位置数据包请按1,签到数据包请按2,签退数据包请按3,运营数据包请按4")
        self.init_data_label1.grid(row=21, column=0, sticky=N)
        items = ("1", "2", "3", "4")
        self.init_data_Text1 = Combobox(self.init_window_name1, width=50, height=12, values=items)
        self.init_data_Text1.current(0)
        self.init_data_Text1.grid(row=22, column=0, columnspan=10, sticky=N)
        self.init_data_Text1.bind("<<ComboboxSelected>>", self.getMon)

        self.sdu_Text_label = Label(self.init_window_name1, text="速度")
        self.sdu_Text_label.grid(row=21, column=11)
        items = ("10", "20", "30", "40")
        self.sdu_Text = Combobox(self.init_window_name1, width=60, height=20, values=items)
        self.sdu_Text.current(1)
        self.sdu_Text.grid(row=22, column=11)

        self.driver_Text_label = Label(self.init_window_name1, text="驾驶员行驶证")
        self.driver_Text_label.grid(row=23, column=0)
        items = ()
        self.driver_Text = Combobox(self.init_window_name1, width=50, height=2, values=items)
        self.driver_Text.grid(row=24, column=0, sticky=N, columnspan=10)

        self.ztai_Text_label = Label(self.init_window_name1, text="车辆状态")
        self.ztai_Text_label.grid(row=23, column=11)
        items = (
            "ACC开和载客", "未卫星定位", "停运状态", "预约任务车", "南纬", "西经", "空转重", "重转空", "ACC开", "重车",
            "车辆油路断开", "车辆电路断开", "车门加锁", "车辆锁定", "已达到限制营运次数时间")
        self.ztai_Text = Combobox(self.init_window_name1, width=60, height=20, values=items)
        self.ztai_Text.grid(row=24, column=11)
        self.ztai_Text.current(0)

        self.data_label = Label(self.init_window_name1, text="自定义发送(选择服务器ip和port端口)")
        self.data_label.grid(row=25, column=0, sticky=N)
        items = ()
        self.data_Text = Combobox(self.init_window_name1, width=52, height=2, values=items)
        self.data_Text.grid(row=26, column=0, sticky=N)
        self.data_Text.bind("<Button-3>", lambda x: rightKey(x, self.init_data_Text1))

        self.result_Text = Button(self.init_window_name1, text="发送", command=lambda: self.thread_it(self.qo_send))
        self.result_Text.grid(row=26, column=10)
        self.result_Text.bind("<Button-3>", lambda x: rightKey(x, self.init_data_Text1))

        self.result_data_label1 = Label(self.init_window_name1, text="输出结果")
        self.result_data_label1.grid(row=2, column=11)

        self.init_data_Text1.bind("<Button-3>", lambda x: rightKey(x, self.init_data_Text1))
        self.result_data_Text1 = Text(self.init_window_name1, width=85, height=20,relief='solid')
        self.result_data_Text1.grid(row=4, column=11, rowspan=15, columnspan=15)
        self.result_data_Text1.bind("<Button-3>", lambda x: rightKey(x, self.result_data_Text1))
        # 按钮
        self.str_trans_to_md5_button = Button(self.init_window_name1, text="专用905生成", width=10,
                                              command=lambda: self.thread_it(self.qo_login))  # 调用内部方法  加()为直接调用
        self.str_trans_to_md5_button.grid(row=12, column=10)
        pane2 = Frame()

        self.ip_Text_label2 = Label(pane2, text="服务器ip")
        self.ip_Text_label2.grid(row=2, column=0, columnspan=10, sticky=N)
        items = ("120.79.74.223", "47.119.168.112", "120.79.176.183")
        self.ip_Text2 = Combobox(pane2, width=50, height=2, values=items)
        self.ip_Text2.current(0)
        self.ip_Text2.grid(row=4, column=0, columnspan=10, sticky=N)
        self.ip_Text2.bind("<Button-3>", lambda x: rightKey(x, self.ip_Text))

        self.port_Text_label2 = Label(pane2, text="服务器Port")
        self.port_Text_label2.grid(row=6, column=0, columnspan=10, sticky=N)
        items = ("17700", "17800", "7788")
        self.port_Text2 = Combobox(pane2, width=50, height=2, values=items)
        self.port_Text2.current(0)
        self.port_Text2.grid(row=8, column=0, columnspan=10, sticky=N)
        self.port_Text2.bind("<Button-3>", lambda x: rightKey(x, self.port_Text))

        self.su_Text_label2 = Label(pane2, text="循环发送次数")
        self.su_Text_label2.grid(row=10, column=0, columnspan=10, sticky=N)
        items = ("2", "10")
        self.su_Text2 = Combobox(pane2, width=50, height=2, values=items)
        self.su_Text2.current(0)
        self.su_Text2.grid(row=12, column=0, columnspan=10, sticky=N)

        # 905组成数据
        self.sbei_Text_label2 = Label(pane2, text="808部标设备号11位")
        self.sbei_Text_label2.grid(row=13, column=0, columnspan=10, sticky=N)
        items = ("10356000000", "10351000000")
        self.sbei_Text2 = Combobox(pane2, width=50, height=2, values=items)
        self.sbei_Text2.current(0)
        self.sbei_Text2.grid(row=14, column=0, sticky=N, columnspan=10)
        self.sbei_Text2.bind("<Button-3>", lambda x: rightKey(x, self.sbei_Text))

        # 经纬度随机
        self.on_ = Button(pane2, text="随机经纬度", width=10, command=self.button_mode2)
        self.on_.grid(row=15, column=10)

        self.wd_Text_label2 = Label(pane2, text="纬度")
        self.wd_Text_label2.grid(row=15, column=0, columnspan=10, sticky=N)
        items = ("32.330217", "23.012173")
        self.wd_Text2 = Combobox(pane2, width=50, height=2, values=items)
        self.wd_Text2.current(1)
        self.wd_Text2.grid(row=16, column=0, sticky=N, columnspan=10)
        self.wd_Text2.bind("<Button-3>", lambda x: rightKey(x, self.wd_Text))

        self.jd_Text_label2 = Label(pane2, text="经度")
        self.jd_Text_label2.grid(row=17, column=0, columnspan=10, sticky=N)
        items = ("114.398462", "104.903551")
        self.jd_Text2 = Combobox(pane2, width=50, height=2, values=items)
        self.jd_Text2.current(0)
        self.jd_Text2.grid(row=18, column=0, sticky=N, columnspan=10)
        self.jd_Text2.bind("<Button-3>", lambda x: rightKey(x, self.jd_Text))

        self.baoj_Text_label2 = Label(pane2, text="报警")
        self.baoj_Text_label2.grid(row=19, column=0, columnspan=10, sticky=N)
        items = ("紧急报警", "超速报警", "疲劳驾驶", "进出区域报警", "路段行驶时间不足", "车辆非法点火", "车辆非法位移",
                 "所有实时报警", "正常")
        self.baoji_Text2 = Combobox(pane2, width=50, height=12, values=items)
        self.baoji_Text2.current(8)
        self.baoji_Text2.grid(row=20, column=0, sticky=N, columnspan=10)

        self.sdu_Text_label2 = Label(pane2, text="速度")
        self.sdu_Text_label2.grid(row=21, column=0, columnspan=10, sticky=N)
        items = ("10", "20", "30", "40")
        self.sdu_Text2 = Combobox(pane2, width=50, height=12, values=items)
        self.sdu_Text2.current(1)
        self.sdu_Text2.grid(row=22, column=0, )

        self.times_Text_label2 = Label(pane2, text="发送停顿时间")
        self.times_Text_label2.grid(row=21, column=11)
        items = ("1", "0.5", "1.5", "2")
        self.times_Text2 = Combobox(pane2, width=60, height=20, values=items)
        self.times_Text2.current(0)
        self.times_Text2.grid(row=22, column=11, sticky=N)

        self.init_data_label2 = Label(pane2, text="位置数据包请按1")
        self.init_data_label2.grid(row=23, column=0, sticky=N)
        items = ("1",)
        self.init_data_Text2 = Combobox(pane2, width=50, height=12, values=items)
        self.init_data_Text2.current(0)
        self.init_data_Text2.grid(row=24, column=0, columnspan=10, sticky=N)
        self.init_data_Text2.bind("<Button-3>", lambda x: rightKey(x, self.init_data_Text2))

        self.ztai_Text_label2 = Label(pane2, text="车辆状态")
        self.ztai_Text_label2.grid(row=23, column=11)
        items = (
            "ACC开", "ACC开和定位", "定位", "停运状态", "经纬度已经保密插件保密", "南纬", "西经",
            "车辆油路断开", "车辆电路断开", "单北斗", "单GPS", "北斗GPS双模", "ACC开定位开北斗GPS满载",
            "ACC开定位开北斗GPS空车",)
        self.ztai_Text2 = Combobox(pane2, width=60, height=20, values=items)
        self.ztai_Text2.grid(row=24, column=11)
        self.ztai_Text2.current(1)

        self.data_label2 = Label(pane2, text="自定义发送(选择服务器ip和port端口)")
        self.data_label2.grid(row=25, column=0, sticky=N)
        items = ()
        self.data_Text2 = Combobox(pane2, width=52, height=2, values=items)
        self.data_Text2.grid(row=26, column=0, sticky=N)
        self.data_Text2.bind("<Button-3>", lambda x: rightKey(x, self.init_data_Text2))

        self.result_Text2 = Button(pane2, text="发送", command=lambda: self.thread_it(self.qo_send2))
        self.result_Text2.grid(row=26, column=10, )
        self.result_Text2.bind("<Button-3>", lambda x: rightKey(x, self.init_data_Text2))

        self.result_data_label2 = Label(pane2, text="输出结果：有返回，即发送成功")
        self.result_data_label2.grid(row=2, column=11)
        self.result_data_Text2 = Text(pane2, width=85, height=20, relief='solid')
        self.result_data_Text2.grid(row=4, column=11, rowspan=15, columnspan=15)
        self.result_data_Text2.bind("<Button-3>", lambda x: rightKey(x, self.result_data_Text2))
        # 按钮
        self.str_trans_to_md5_button2 = Button(pane2, text="专用808生成", width=10,
                                               command=lambda: self.thread_it(self.qo_login部标))  # 调用内部方法  加()为直接调用
        self.str_trans_to_md5_button2.grid(row=12, column=10)
        # self.str_trans_to_md5_button.bind("<Enter>", lambda event: self.qo_login()) #滑动点击

        pane3 = Frame()

        self.ip_Text_label3 = Label(pane3, text="服务器ip")
        self.ip_Text_label3.grid(row=2, column=0)
        items = ("120.79.74.223", "47.119.168.112")
        self.ip_Text3 = Combobox(pane3, width=50, height=2, values=items)
        self.ip_Text3.current(0)
        self.ip_Text3.grid(row=4, column=0, columnspan=10, sticky=N)

        self.port_Text_label3 = Label(pane3, text="服务器Port")
        self.port_Text_label3.grid(row=6, column=0)
        items = ("17700", "17800")
        self.port_Text3 = Combobox(pane3, width=50, height=2, values=items)
        self.port_Text3.current(1)
        self.port_Text3.grid(row=8, column=0, columnspan=10, sticky=N)

        self.su_Text_label3 = Label(pane3, text="循环次数")
        self.su_Text_label3.grid(row=10, column=0)
        items = ("1", "10")
        self.su_Text3 = Combobox(pane3, width=50, height=2, values=items)
        self.su_Text3.current(0)
        self.su_Text3.grid(row=12, column=0, columnspan=10, sticky=N)

        # 905组成数据
        self.sbei_Text_label3 = Label(pane3, text="设备号(905设备号12位)")
        self.sbei_Text_label3.grid(row=13, column=0)
        items = ("101356000000", "101351000000")
        self.sbei_Text3 = Combobox(pane3, width=50, height=2, values=items)
        self.sbei_Text3.current(0)
        self.sbei_Text3.grid(row=14, column=0, sticky=N, columnspan=10)

        self.init_data_label3 = Label(pane3,
                                      text="抢单请按1,取消订单请按2,完成订单请按3")
        self.init_data_label3.grid(row=21, column=0, sticky=N)
        items = ("1", "2", "3")
        self.init_data_Text3 = Combobox(pane3, width=50, height=12, values=items)
        self.init_data_Text3.current(0)
        self.init_data_Text3.grid(row=22, column=0, columnspan=10, sticky=N)

        self.driver_Text_label3 = Label(pane3, text="业务ID")
        self.driver_Text_label3.grid(row=23, column=0)
        items = ()
        self.yewid_Text3 = Combobox(pane3, width=50, height=2, values=items)
        self.yewid_Text3.grid(row=24, column=0, sticky=N, columnspan=10)

        self.data_label3 = Label(pane3, text="自定义发送(选择服务器ip和port端口)")
        self.data_label3.grid(row=25, column=0, sticky=N)
        self.data_Text3 = Text(pane3, width=52, height=2, relief='solid')
        self.data_Text3.grid(row=26, column=0, sticky=N)
        self.data_Text3.bind("<Button-3>", lambda x: rightKey(x, self.init_data_Text3))

        self.result_Text3 = Button(pane3, text="发送", command=lambda: self.thread_it(self.qo_send3))
        self.result_Text3.grid(row=26, column=10)
        self.result_Text3.bind("<Button-3>", lambda x: rightKey(x, self.init_data_Text3))

        self.result_data_label3 = Label(pane3, text="输出结果")
        self.result_data_label3.grid(row=2, column=11)

        self.init_data_Text3.bind("<Button-3>", lambda x: rightKey(x, self.init_data_Text3))
        self.result_data_Text3 = Text(pane3, width=85, height=20,relief='solid')
        self.result_data_Text3.grid(row=4, column=11, rowspan=15, columnspan=15)
        self.result_data_Text3.bind("<Button-3>", lambda x: rightKey(x, self.result_data_Text3))
        # 按钮
        self.str_trans_to_md5_button3 = Button(pane3, text="订单905发送", width=10,
                                               command=lambda: self.thread_it(self.qo_ddan))  # 调用内部方法  加()为直接调用
        self.str_trans_to_md5_button3.grid(row=12, column=10)

        pane4 = Frame()

        self.ip_Text_label4 = Label(pane4, text="服务器ip")
        self.ip_Text_label4.grid(row=2, column=0, columnspan=10, sticky=N)
        items = ("47.107.222.141", "47.119.168.112", "120.79.176.183")
        self.ip_Text4 = Combobox(pane4, width=50, height=2, values=items)
        self.ip_Text4.current(0)
        self.ip_Text4.grid(row=4, column=0, columnspan=10, sticky=N)
        self.ip_Text4.bind("<Button-3>", lambda x: rightKey(x, self.ip_Text4))

        self.port_Text_label4 = Label(pane4, text="服务器Port")
        self.port_Text_label4.grid(row=6, column=0, columnspan=10, sticky=N)
        items = ("6688", "6690", "17800",)
        self.port_Text4 = Combobox(pane4, width=50, height=2, values=items)
        self.port_Text4.current(0)
        self.port_Text4.grid(row=8, column=0, columnspan=10, sticky=N)
        self.port_Text4.bind("<Button-3>", lambda x: rightKey(x, self.port_Text4))

        self.su_Text_label4 = Label(pane4, text="循环发送次数")
        self.su_Text_label4.grid(row=10, column=0, columnspan=10, sticky=N)
        items = ("2", "10")
        self.su_Text4 = Combobox(pane4, width=50, height=2, values=items)
        self.su_Text4.current(0)
        self.su_Text4.grid(row=12, column=0, columnspan=10, sticky=N)

        # 905组成数据
        self.sbei_Text_label4 = Label(pane4, text="2929伪ip设备8位")
        self.sbei_Text_label4.grid(row=13, column=0, columnspan=10, sticky=N)
        items = ("58D8D858", "81828CA2")
        self.sbei_Text4 = Combobox(pane4, width=50, height=2, values=items)
        self.sbei_Text4.current(0)
        self.sbei_Text4.grid(row=14, column=0, sticky=N, columnspan=10)
        self.sbei_Text4.bind("<Button-3>", lambda x: rightKey(x, self.sbei_Text4))

        # 经纬度随机
        self.on_ = Button(pane4, text="随机经纬度", width=10, command=self.button_mode4)
        self.on_.grid(row=15, column=10)

        self.wd_Text_label4 = Label(pane4, text="纬度")
        self.wd_Text_label4.grid(row=15, column=0, columnspan=10, sticky=N)
        items = ("32.33021", "23.01217")
        self.wd_Text4 = Combobox(pane4, width=50, height=2, values=items)
        self.wd_Text4.current(1)
        self.wd_Text4.grid(row=16, column=0, sticky=N, columnspan=10)
        self.wd_Text4.bind("<Button-3>", lambda x: rightKey(x, self.wd_Text4))

        self.jd_Text_label4 = Label(pane4, text="经度")
        self.jd_Text_label4.grid(row=17, column=0, columnspan=10, sticky=N)
        items = ("114.39846", "104.90355")
        self.jd_Text4 = Combobox(pane4, width=50, height=2, values=items)
        self.jd_Text4.current(0)
        self.jd_Text4.grid(row=18, column=0, sticky=N, columnspan=10)
        self.jd_Text4.bind("<Button-3>", lambda x: rightKey(x, self.jd_Text4))

        self.sdu_Text_label4 = Label(pane4, text="速度")
        self.sdu_Text_label4.grid(row=19, column=0, columnspan=10, sticky=N)
        items = ("10", "20", "30", "40")
        self.sdu_Text4 = Combobox(pane4, width=50, height=12, values=items)
        self.sdu_Text4.current(1)
        self.sdu_Text4.grid(row=20, column=0, )

        self.fx_Text_label = Label(pane4, text="方向")
        self.fx_Text_label.grid(row=21, column=0, columnspan=10, sticky=N)
        items = ("10", "20", "30", "40")
        self.fx_Text = Combobox(pane4, width=50, height=12, values=items)
        self.fx_Text.current(1)
        self.fx_Text.grid(row=22, column=0, )

        self.times_Text_label = Label(pane4, text="发送停顿时间")
        self.times_Text_label.grid(row=19, column=11)
        items = ("1", "0.5", "1.5", "2")
        self.times_Text4 = Combobox(pane4, width=60, height=20, values=items)
        self.times_Text4.current(0)
        self.times_Text4.grid(row=20, column=11, sticky=N)

        self.init_data_label4 = Label(pane4, text="位置数据包请按1")
        self.init_data_label4.grid(row=23, column=0, sticky=N)
        items = ("1",)
        self.init_data_Text4 = Combobox(pane4, width=50, height=12, values=items)
        self.init_data_Text4.current(0)
        self.init_data_Text4.grid(row=24, column=0, columnspan=10, sticky=N)
        self.init_data_Text4.bind("<Button-3>", lambda x: rightKey(x, self.init_data_Text4))

        self.data_label = Label(pane4, text="自定义发送(选择服务器ip和port端口)")
        self.data_label.grid(row=25, column=0, sticky=N)
        items = ()
        self.data_Text4 = Combobox(pane4, width=52, height=2, values=items)
        self.data_Text4.grid(row=26, column=0, sticky=N)
        self.data_Text4.bind("<Button-3>", lambda x: rightKey(x, self.init_data_Text4))

        self.result_Text4 = Button(pane4, text="发送", command=lambda: self.thread_it(self.qo_send))
        self.result_Text4.grid(row=26, column=10, )
        self.result_Text4.bind("<Button-3>", lambda x: rightKey(x, self.init_data_Text1))

        self.result_data_label4 = Label(pane4, text="输出结果：有返回，即发送成功")
        self.result_data_label4.grid(row=2, column=11)
        self.result_data_Text4 = Text(pane4, width=85, height=20, relief='solid')
        self.result_data_Text4.grid(row=4, column=11, rowspan=15, columnspan=15)
        self.result_data_Text4.bind("<Button-3>", lambda x: rightKey(x, self.result_data_Text4))
        # 按钮
        self.str_trans_to_md5_button4 = Button(pane4, text="2929生成", width=10,
                                              command=lambda: self.thread_it(self.qo_login2929))
        self.str_trans_to_md5_button4.grid(row=12, column=10)

        pane5 = Frame()

        # v3组成数据
        self.sbei_Text_label5 = Label(pane5, text="设备号(V3设备号15位)")
        self.sbei_Text_label5.grid(row=0, column=0,sticky=N,)

        items = ("154854744888745", "145263966554789")
        self.sbei_Text5 = Combobox(pane5,width=67, height=20,values=items)
        self.sbei_Text5.current(0)
        self.sbei_Text5.grid(row=1, column=0, sticky=N,)

        self.init_data_label5 = Label(pane5,
                                      text="(登录数据包请按1,定位数据包请按2,报警数据包请按3,心跳数据包请按4)\n注意V3协议除登录包需要更改设备号，其他数据包默认通用")
        self.init_data_label5.grid(row=2, column=0, sticky=N)
        items=("1","2","3","4")
        self.init_data_Text5 = Combobox(pane5, width=67, height=20,values=items)
        self.init_data_Text5.current(0)
        self.init_data_Text5.grid(row=3, column=0, sticky=N)

        self.log_label5 = Label(pane5, text="日志")
        self.log_label5.grid(row=4, column=0)
        self.log_data_Text5 = Text(pane5, width=69, height=3,relief='solid')  # 日志框
        self.log_data_Text5.grid(row=5, column=0,  sticky=N)
        self.log_data_Text5.bind("<Button-3>", lambda x: rightKey(x, self.log_data_Text5))
        # 按钮
        self.str_trans_to_md5_button5 = Button(pane5, text="专用V3生成", width=10,
                                               command=lambda: self.thread_it(self.qo_loginV3))  # 调用内部方法  加()为直接调用
        self.str_trans_to_md5_button5.grid(row=3, column=11,sticky=N)

        self.result_data_label5= Label(pane5, text="输出结果")
        self.result_data_label5.grid(row=0, column=12)

        self.init_data_Text5.bind("<Button-3>", lambda x: rightKey(x, self.init_data_Text1))
        self.result_data_Text5 = Text(pane5, width=67, height=12,relief='solid')
        self.result_data_Text5.grid(row=1, column=12,rowspan=10,sticky=N)
        self.result_data_Text5.bind("<Button-3>", lambda x: rightKey(x, self.result_data_Text5))

        self.init_data1_label5 = Label(pane5,
                                      text="原始数据(无空格，请格式化)\n例子：7878110101234135484845480100320000016D3F0D0A")
        self.init_data1_label5.grid(row=6, column=0)
        self.init_data1_Text5 = Text(pane5, width=69, height=18,relief='solid')  # 原始数据录入框
        self.init_data1_Text5.grid(row=7, column=0,columnspan=10, sticky=N)
        self.init_data1_Text5.bind("<Button-3>", lambda x: rightKey(x, self.init_data_Text5))

        self.result_data_label5 = Label(pane5, text="解析结果")
        self.result_data_label5.grid(row=6, column=12)
        self.result_data1_Text5 = Text(pane5, width=67, height=18,relief='solid')  # 处理结果展示
        self.result_data1_Text5.grid(row=7, column=12,  rowspan=10, sticky=N)
        self.result_data1_Text5.bind("<Button-3>", lambda x: rightKey(x, self.result_data1_Text5))
        # # 按钮
        self.str1_trans_to_md5_button5 = Button(pane5, text="专用V3解析", width=10,
                                               command=lambda: self.thread_it(self.xieyihao))  # 调用内部方法  加()为直接调用
        self.str1_trans_to_md5_button5.grid(row=7, column=11, sticky=W)




        note.add(self.init_window_name1, text='出租车905TCP发送')
        note.add(pane2, text='部标808TCP发送')
        note.add(pane3, text='抢答回复订单')
        note.add(pane4, text='2929协议UDP发送')
        note.add(pane5, text='V3协议解析生成')
        note.grid()


from tkinter.messagebox import *


def mess():
    # 创建askyesno()会话框
    boo = askyesno("真的要走了吗", "臣退了，这一退就是一辈子！")
    if boo == True:
        init_window.quit()


def gui_start():
    ZMJ_PORTAL = MY_GUI(init_window)
    init_window.protocol("WM_DELETE_WINDOW", mess)
    # 设置根窗口默认属性
    ZMJ_PORTAL.set_init_window()
    init_window.iconbitmap("favicon.ico")

    init_window.mainloop()


gui_start()
