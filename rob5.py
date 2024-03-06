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
# from tkinter import ttk
# coding=utf-8
import binascii
import re
import tkinter as tk
from tkinter.colorchooser import askcolor
from pygame import mixer

import ttkbootstrap as ttk
LOG_LINE_NUM = 0
init_window = ttk.Window()  # 实例化出一个父窗口

s=ttk.Style() #实例化Style
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

    def wzhi905(self, su,plsu):
        count = 0
        for i in range(int(su),int(plsu)):
            try:
                now_time = time.strftime('%Y%m%d%H%M%S', time.localtime())
                wd1 = float(self.wd()) * 60 / 0.0001
                wd2 = hex(int(wd1))
                jd1 = float(self.jd()) * 60 / 0.0001
                jd2 = hex(int(jd1))
                标识位 = '7E'
                消息ID = '0200'
                消息体属性 = '002F'
                ISU标识 = self.sb_hao().zfill(12)[:12 - len(f'{i}')] + f'{i}'
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
                    continue
            except:
                return "数据解析有误，查看是否数据填写错误，修改无误后，请重新点击生成数据"
        self.result_data_Text1.insert(1.0, "总计发送成功位置数据条数:{}\n\n".format(str(count)))
        showinfo("发送结果", "总计发送成功位置数据条数:  {}".format(str(count)))
        return "操作已完成"




    def qdao(self,su,plsu):
        count = 0
        for i in range(int(su),int(plsu)):
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
        ip_on=self.ip_on_Text.get().strip()
        return ip_on

    def getMon(self, items):
        inits = self.init_data_Text1.get()
        if inits == "2" or inits == "3" or inits == "4":
            items = ("534E3132333435363738393132333435363739", "534E3132333435363738393132333435363738")
        else:
            pass
        self.driver_Text["values"] = items




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
                self.result_data_Text1.insert(END, self.wzhi905(self.su(),self.plsu()))
            # return 0
        elif src == '2':
            sbb1 = self.sb_hao()
            if not sbb1:
                self.result_data_Text1.delete(1.0, END)
                self.result_data_Text1.insert(1.0, "请输入设备号")
            else:
                self.result_data_Text1.delete(1.0, END)
                self.result_data_Text1.insert(END, self.qdao(self.su(),self.plsu()))
        elif src == '3':
            sbb1 = self.sb_hao()
            if not sbb1:
                self.result_data_Text1.delete(1.0, END)
                self.result_data_Text1.insert(1.0, "请输入设备号")
            else:
                self.result_data_Text1.delete(1.0, END)
                self.result_data_Text1.insert(END, self.qtui(self.su(),self.plsu()))
        elif src == '4':
            sbb1 = self.sb_hao()
            if not sbb1:
                self.result_data_Text1.delete(1.0, END)
                self.result_data_Text1.insert(1.0, "请输入设备号")
            else:
                self.result_data_Text1.delete(1.0, END)
                self.result_data_Text1.insert(END, self.yyun(self.su(),self.plsu()))


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





    # 设置窗口
    def set_init_window(self):

        # 905解析数据
        self.init_window_name.title("协议整合工具_v4  作者 : 姚子奇")
        self.init_window_name.geometry('1100x618+450+200')

        note = Notebook(self.init_window_name)
        pane1 = Frame()

        self.ip_Text_label = Label(pane1, text="服务器ip")
        self.ip_Text_label.grid(row=0, columnspan=2, sticky=N)
        items = ("120.79.74.223", "47.119.168.112", "120.79.176.183")
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
        self.baoj_Text_label = Label(pane1, text="报警")
        self.baoj_Text_label.grid(row=12, column=0)
        items = (
            "紧急报警", "超速报警", "LED顶灯故障", "进出区域路线报警", "路段行驶时间不足", "禁行路段行驶",
            "车辆非法点火",
            "车辆非法位移", "所有实时报警", "正常")
        self.baoji_Text = Combobox(pane1, width=50, height=12, values=items)
        self.baoji_Text.current(9)
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
        self.result_data_Text1 = Text(pane1, width=85, height=20,relief='solid')
        self.result_data_Text1.grid(row=1, column=11, rowspan=13, columnspan=15)
#         # self.result_data_Text1.bind("<Button-3>", lambda x: rightKey(x, self.result_data_Text1))
        # 按钮
        self.str_trans_to_md5_button = Button(pane1, text="专用905生成", width=10,
                                              command=lambda: self.thread_it(self.qo_login))  # 调用内部方法  加()为直接调用
        self.str_trans_to_md5_button.grid(row=5, column=10)
#
#         # play_animation()
        note.add(pane1, text='出租车905TCP发送')
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
