import threading
import time
import random
import math
from PIL import ImageTk,Image
import pandas as pd
from socket import *
from tkinter import *
import tkinter.font as tkFont
from tkinter import messagebox
from tkinter.ttk import *
# coding=utf-8
import binascii
import re
import tkinter as tk
from tkinter import ttk
from tkinter.colorchooser import askcolor
import pymysql as MySQLdb

from 出租车.hbing import gui1_start
from 出租车.bubiao import gui2_start
from v3 import gui3_start
from rob1 import gui4_start

LOG_LINE_NUM = 0
init_window1 = Tk()  # 实例化出一个父窗口
menubar = Menu(init_window1, tearoff=False)

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
is_on = True


## 其他界面
class OtherFrame(tk.Toplevel):
    def __init__(self, title):
        tk.Toplevel.__init__(self)
        self.title(title)
        self.iconbitmap('favicon.ico')
        self.geometry('400x80+500+100')
        self.attributes('-alpha', 0.92)

class user_login(object):
    def __init__(self, init_window_name1):
        self.init_window_name1= init_window_name1
        self.init_window_name1.title('登录页')
        self.init_window_name1.iconbitmap('favicon.ico')
        self.init_window_name1.geometry('300x270+500+100')
        self.init_window_name1.attributes('-alpha', 0.92)
        self.var1 = tk.StringVar()
        self.conn = MySQLdb.Connection(host='localhost', port=3306, user='root', passwd='admin', db='yaoziqi',
                                       charset='utf8')  # 获取管理员权限可见的账户信息，提取出账户和密码存入字典便于验证
        self.cursor = self.conn.cursor()
        self.cursor.execute('select user,pwd from user_yh')
        login_inf = self.cursor.fetchall()
        user_inf = [str(ii[0]) for ii in login_inf]
        passwd_inf = [str(ii[1]) for ii in login_inf]
        self.dict_inf = dict(zip(user_inf, passwd_inf))

        tk.Label(self.init_window_name1, text='用户名', bd=4).grid(row=0)
        tk.Label(self.init_window_name1, text='密码', bd=4).grid(row=1)
        self.e1 = tk.Entry(self.init_window_name1)
        self.e1.grid(row=0, column=1, padx=10, pady=5)
        self.e2 = tk.Entry(self.init_window_name1, show='*')
        self.e2.grid(row=1, column=1, padx=10, pady=5)
        self.e1.insert(0, '1')
        self.e2.insert(0, '1')
        b1 = tk.Button(self.init_window_name1, text='登陆', command=self.login, width=10, fg='white', bg='blue')
        b1.grid(row=3, column=0, sticky=tk.W, padx=10, pady=5)
        b2 = tk.Button(self.init_window_name1, text='免费注册', command=self._register, width=10, fg='blue', highlightcolor='blue')
        b2.grid(row=3, column=1, sticky=tk.E, padx=10, pady=5)
        self.init_window_name1.grid()

    def _register(self):
        self.init_window_name1.withdraw()
        self.top_register = OtherFrame('你好')
        self.top_register.title('账号注册')
        top_pic = tk.Frame(self.top_register)
        top = tk.Frame(self.top_register)
        tk.Label(top, text='用户名').grid(row=1)
        tk.Label(top, text='密码').grid(row=3)
        tk.Label(top, text='确认密码').grid(row=5)
        self.v1 = tk.StringVar()
        self.v2 = tk.StringVar()
        self.v3 = tk.StringVar()
        e1 = tk.Entry(top, width=20,textvariable=self.v1) # 设置你的用户名
        e2 = tk.Entry(top,  width=20,show='*',textvariable=self.v2) # 设置你的密码
        e3 = tk.Entry(top,  width=20, show='*',textvariable=self.v3) # 确认你的密码
        e1.grid(row=1, column=1, padx=1, pady=1)
        e2.grid(row=3, column=1, padx=1, pady=1)
        e3.grid(row=5, column=1, padx=1, pady=1)
        #
        handle = lambda: self.close_open(self.top_register,self.init_window_name1)
        tk.Button(top, text='<<返回登陆界面',fg='white',bg='blue',command=handle).grid(row=11, column=0, padx=10, pady=1)
        tk.Button(top, text='>>注册你的账号',bg='blue',fg='white',command=self.save_inf).grid(row=11, column=1, padx=10, pady=1)
        self.register_var = tk.StringVar()
        self.register_var.set('')
        tk.Label(top,textvariable=self.register_var,fg='red').grid(row=13,column=1)
        top_pic.grid()
        top.grid()
        self.top_register.mainloop()## 存储用户的注册信息

    def login(self):
        global top_login
        if self.e1.get() in self.dict_inf.keys():
            if self.e2.get() == self.dict_inf[self.e1.get()]:
                self.init_window_name1.withdraw()
                self.top_register.withdraw()
                top_login = OtherFrame('登陆成功,欢迎您:%s' % (self.e1.get()))
                b1 = tk.Button(top_login, text='905协议', command=self.login_905, width=10, fg='blue',highlightcolor='blue')
                b1.grid(row=3, column=0, sticky=tk.W, padx=10, pady=5)
                # top_login.withdraw()
                b2 = tk.Button(top_login, text='808协议', command=self.login_808, width=10, fg='blue',highlightcolor='blue')
                b2.grid(row=3, column=1, sticky=tk.E, padx=10, pady=5)
                # top_login.withdraw()
                b3 = tk.Button(top_login, text='V3协议', command=self.login_V3, width=10, fg='blue', highlightcolor='blue')
                b3.grid(row=3, column=2, sticky=tk.E, padx=10, pady=5)
                b4 = tk.Button(top_login, text='整合协议', command=self.login_he, width=10, fg='blue',
                               highlightcolor='blue')
                b4.grid(row=3, column=3, sticky=tk.E, padx=10, pady=5)
                top_login.mainloop()

    def save_inf(self):
        if self.v2.get() != self.v3.get():
            self.register_var.set('两次密码输入不一致')
        elif self.v1.get() in self.dict_inf.keys():
            self.register_var.set('用户名已经存在')
        elif self.v1.get()=='' or self.v2.get()=='' or self.v3.get()=='' :
            self.register_var.set('信息输入不完整')
        else:
            try:
                sql_insert = "insert into user_yh values('%s','%s')"%(self.v1.get(),self.v2.get())
                self.cursor.execute(sql_insert)
                self.conn.commit()
                self.register_var.set('注册成功，返回登录页登录')
                time.sleep(1)
                # register_to_login = lambda: self.close_open(self.top_register, self.login())
                # tk.Button(self.top_register,text='注册成功，点击跳转',command=register_to_login).grid(row=13, column=0, padx=10, pady=1)
            except MySQLdb.Error as e:
                self.conn.rollback()
                print ('写入错误'+str(e))## 用户选忘记密码的响应，这里为了简便不提供支持，其实很简单



    def close_open(self,close_window,open_window):
        close_window.withdraw()
        # self.login()
        open_window.update()
        open_window.deiconify()


                # top_login.withdraw()

    def login_905(self):
        top_login.withdraw()
        top_login.update()
        top_login.deiconify()
        gui1_start()

    def login_808(self):
        top_login.withdraw()
        top_login.update()
        top_login.deiconify()
        gui2_start()

    def login_V3(self):
        top_login.withdraw()
        top_login.update()
        top_login.deiconify()
        gui3_start()

    def login_he(self):
        top_login.withdraw()
        top_login.update()
        top_login.deiconify()
        gui4_start()


    def show_menu(self, event):
        self.init_window_name1.menu.post(event.x_root, event.y_root)



    # 设置窗口
    # def set_init_window1(self):
    #     # 905解析数据
    #     self.init_window_name1.title("主页  作者 : 姚子奇")
    #     self.init_window_name1.geometry('260x400+10+10')
    #     self.init_window_name1.menu = Menu(self.init_window_name1, tearoff=0)
    #     self.init_window_name1.menu.add_command(label="退出应用", command=self.init_window_name1.quit)
    #     self.init_window_name1.bind("<Button-3>", self.show_menu)





# from tkinter.messagebox import *
#
#
#
#
# def mess():
#     # 创建askyesno()会话框
#     boo = askyesno("真的要走了吗", "臣退了，这一退就是一辈子！")
#     if boo == True:
#         init_window1.quit()


def gui_start():
    user_login(init_window1)
    init_window1.iconbitmap("xku.ico")
    init_window1.mainloop()


gui_start()
