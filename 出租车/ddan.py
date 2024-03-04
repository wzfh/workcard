import time
import random
import math

from socket import *
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
# coding=utf-8
import binascii
import re
import tkinter as tk
from tkinter.colorchooser import askcolor

LOG_LINE_NUM = 0
init_window = Tk()  # 实例化出一个父窗口
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


class MY_GUI(tk.Tk):

    def __init__(self, init_window_name):
        self.init_window_name = init_window_name

    def qda(self, su):
        datas = []
        ts = []
        for i in range(int(su)):
            try:
                标识位 = '7E'
                消息ID = '0B01'
                消息体属性 = '002F'
                ISU标识 = self.sb_hao()
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
                ts.append(t)
                datas.append(data)
                s = socket(AF_INET, SOCK_STREAM)
                s.connect((f'{self.ip()}', int(self.port())))  # 生产
                s.send(bytes().fromhex(t))
                print('\n' * 1)
                time.sleep(2)
            except:
                return "数据解析有误，查看是否数据填写错误，修改无误后，请重新点击生成数据"
        return '抢单数据：\n\n{}\n\n\n源数据：\n\n{}'.format(datas[0], ts[0])

    def qr(self, su):
        datas = []
        ts = []
        for i in range(int(su)):
            try:
                标识位 = '7E'
                消息ID = '0B07'
                消息体属性 = '002F'
                ISU标识 = self.sb_hao()
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
                ts.append(t)
                datas.append(data)
                s = socket(AF_INET, SOCK_STREAM)
                s.connect((f'{self.ip()}', int(self.port())))  # 生产
                s.send(bytes().fromhex(t))
                print('\n' * 1)
                time.sleep(2)
                s.close()
            except:
                return "数据解析有误，查看是否数据填写错误，修改无误后，请重新点击生成数据"
        return '完成订单数据：\n\n{}\n\n\n源数据：\n\n{}'.format(datas[0], ts[0])

    def qx(self, su):
        datas = []
        ts = []
        for i in range(int(su)):
            try:
                标识位 = '7E'
                消息ID = '0B08'
                消息体属性 = '002F'
                ISU标识 = self.sb_hao()
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
                ts.append(t)
                datas.append(data)
                s = socket(AF_INET, SOCK_STREAM)
                s.connect((f'{self.ip()}', int(self.port())))  # 生产
                s.send(bytes().fromhex(t))
                print('\n' * 1)
                time.sleep(2)
            except:
                return "数据解析有误，查看是否数据填写错误，修改无误后，请重新点击生成数据"
        return '取消订单数据：\n\n{}\n\n\n源数据：\n\n{}'.format(datas[0], ts[0])


    def sb_hao(self):
        sb = self.sbei_Text.get().strip()
        return sb


    def ip(self):
        ip = self.ip_Text.get().strip()
        return ip

    def port(self):
        port = self.port_Text.get().strip()
        return port

    def su(self):
        su = self.su_Text.get().strip()
        return su

    def yewid(self):
        yewid=self.yewid_Text.get().strip()
        yewid=hex(int(yewid))[2:]
        return yewid


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

    def tm(self):
        def confirm():
            value = input_entry.get().strip()
            if value:
                value = int(value) * float("0.1")
                self.init_window_name.attributes('-alpha', value)  # 设置窗口透明度
        input_dialog = Toplevel(self.init_window_name)
        input_dialog.title("窗口透明度设置")
        input_dialog.geometry('380x70+10+10')
        input_label = Label(input_dialog, text="透明度值：(%)")
        input_label.grid(row=0, column=0)
        items = ("1", "2", "3", "4", "5", "6", "7", "8", "9")
        input_entry = Combobox(input_dialog, width=50, values=items)
        input_entry.grid(row=1, column=0)
        input_entry.current(5)
        confirm_button = tk.Button(input_dialog, text="确认", command=confirm)
        confirm_button.grid(row=2, column=0)



    def qo_ddan(self):
        src = self.init_data_Text1.get().strip()
        print(src)
        if src == '1':
            sbb1 = self.sb_hao()
            if not sbb1:
                self.result_data_Text1.delete(1.0, END)
                self.result_data_Text1.insert(1.0, "请输入订单类型")
            else:
                self.result_data_Text1.delete(1.0, END)
                self.result_data_Text1.insert(END, self.qda(self.su()))
            # return 0
        elif src == '2':
            sbb1 = self.sb_hao()
            if not sbb1:
                self.result_data_Text1.delete(1.0, END)
                self.result_data_Text1.insert(1.0, "请输入订单类型")
            else:
                self.result_data_Text1.delete(1.0, END)
                self.result_data_Text1.insert(END, self.qx(self.su()))
        elif src == '3':
            sbb1 = self.sb_hao()
            if not sbb1:
                self.result_data_Text1.delete(1.0, END)
                self.result_data_Text1.insert(1.0, "请输入订单类型")
            else:
                self.result_data_Text1.delete(1.0, END)
                self.result_data_Text1.insert(END, self.qr(self.su()))


    def qo_send(self):
        src = self.data_Text.get(1.0, END).strip()
        print(src)
        if not src:
            self.result_data_Text1.delete(1.0, END)
            self.result_data_Text1.insert(1.0, "请输入自定义数据")
        else:
            s = socket(AF_INET, SOCK_STREAM)
            s.connect((f'{self.ip()}', int(self.port())))  # 生产
            s.send(bytes().fromhex(src))
            print('\n' * 1)
            time.sleep(10)
            self.result_data_Text1.delete(1.0, END)
            self.result_data_Text1.insert(END, src)

    # 设置窗口
    def set_init_window(self):
        # 905解析数据
        self.init_window_name.title("905订单工具_v1.3  作者 : 姚子奇")
        self.init_window_name.geometry('1060x500+10+10')

        self.init_window_name.menu = Menu(self.init_window_name, tearoff=0)
        self.init_window_name.menu.add_command(label="退出应用", command=self.init_window_name.quit)
        # 添加“置顶”子菜单
        self.init_window_name.menu.add_command(label="窗口置顶", command=self.topmost_on)
        # 添加“改变颜色”子菜单
        self.init_window_name.menu.add_command(label="修改颜色", command=self.choose_color)
        # 添加“窗口透明度设置”子菜单
        self.init_window_name.menu.add_command(label="窗口透明度设置", command=self.tm)
        self.init_window_name.bind("<Button-3>", self.show_menu)

        self.ip_Text_label = Label(self.init_window_name, text="服务器ip")
        self.ip_Text_label.grid(row=2, column=0)
        items = ("120.79.74.223", "47.119.168.112")
        self.ip_Text = Combobox(self.init_window_name, width=50, height=2, values=items)
        self.ip_Text.current(0)
        self.ip_Text.grid(row=4, column=0, columnspan=10, sticky=N)

        self.port_Text_label = Label(self.init_window_name, text="服务器Port")
        self.port_Text_label.grid(row=6, column=0)
        items = ("17700", "17800")
        self.port_Text = Combobox(self.init_window_name, width=50, height=2, values=items)
        self.port_Text.current(1)
        self.port_Text.grid(row=8, column=0, columnspan=10, sticky=N)

        self.su_Text_label = Label(self.init_window_name, text="循环次数")
        self.su_Text_label.grid(row=10, column=0)
        items = ("1", "10")
        self.su_Text = Combobox(self.init_window_name, width=50, height=2, values=items)
        self.su_Text.current(0)
        self.su_Text.grid(row=12, column=0, columnspan=10, sticky=N)

        # 905组成数据
        self.sbei_Text_label = Label(self.init_window_name, text="设备号(905设备号12位)")
        self.sbei_Text_label.grid(row=13, column=0)
        items = ("101356000000", "101351000000")
        self.sbei_Text = Combobox(self.init_window_name, width=50, height=2, values=items)
        self.sbei_Text.current(0)
        self.sbei_Text.grid(row=14, column=0, sticky=N, columnspan=10)



        self.init_data_label1 = Label(self.init_window_name,
                                      text="抢单请按1,取消订单请按2,完成订单请按3")
        self.init_data_label1.grid(row=21, column=0, sticky=N)
        items = ("1", "2", "3")
        self.init_data_Text1 = Combobox(self.init_window_name, width=50, height=12, values=items)
        self.init_data_Text1.current(0)
        self.init_data_Text1.grid(row=22, column=0, columnspan=10, sticky=N)

        self.driver_Text_label = Label(self.init_window_name, text="业务ID")
        self.driver_Text_label.grid(row=23, column=0)
        items = ()
        self.yewid_Text = Combobox(self.init_window_name, width=50, height=2, values=items)
        self.yewid_Text.grid(row=24, column=0, sticky=N, columnspan=10)

        self.data_label = Label(self.init_window_name, text="自定义发送(选择服务器ip和port端口)")
        self.data_label.grid(row=25, column=0, sticky=N)
        self.data_Text = Text(self.init_window_name, width=52, height=2, relief='solid')
        self.data_Text.grid(row=26, column=0, sticky=N)
        self.data_Text.bind("<Button-3>", lambda x: rightKey(x, self.init_data_Text1))

        self.result_Text = Button(self.init_window_name, text="发送", command=self.qo_send)
        self.result_Text.grid(row=26, column=10)
        self.result_Text.bind("<Button-3>", lambda x: rightKey(x, self.init_data_Text1))

        self.result_data_label1 = Label(self.init_window_name, text="输出结果")
        self.result_data_label1.grid(row=2, column=11)

        self.init_data_Text1.bind("<Button-3>", lambda x: rightKey(x, self.init_data_Text1))
        self.result_data_Text1 = Text(self.init_window_name, width=85, height=20)
        self.result_data_Text1.grid(row=4, column=11, rowspan=15, columnspan=15)
        self.result_data_Text1.bind("<Button-3>", lambda x: rightKey(x, self.result_data_Text1))
        # 按钮
        self.str_trans_to_md5_button = Button(self.init_window_name, text="订单905发送", width=10,
                                              command=self.qo_ddan)  # 调用内部方法  加()为直接调用
        self.str_trans_to_md5_button.grid(row=12, column=10)


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
