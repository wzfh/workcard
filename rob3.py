# -*- coding: utf-8 -*-
import tkinter
from tkinter import ttk
import pymysql
# 导入消息对话框子模块
import tkinter.messagebox








def main3():
    root = tkinter.Tk()
    root.title('告警查询')
    # 设置窗口大小
    root.minsize(500, 500)



    monty3 = ttk.LabelFrame(root, text='GPRS参数设置')
    monty3.grid(column=0, row=0, sticky='W', padx=8, pady=4)



    input_name1 = ttk.Label(monty3, text='服务器TCP地址:').grid(column=0, row=0, sticky='W', pady=5)
    label1 = tkinter.StringVar()
    entry1 = tkinter.Entry(monty3, bg='#ffffff', width=20, textvariable=label1).grid(column=1, row=0, sticky='W')

    input_name2 = ttk.Label(monty3, text='TCP端口号').grid(column=3, row=0, sticky='W')
    label2 = tkinter.StringVar()
    entry2 = tkinter.Entry(monty3, bg='#ffffff', width=20, textvariable=label2).grid(column=4, row=0, sticky='W')

    input_name3 = ttk.Label(monty3, text='服务器UDP地址').grid(column=0, row=1, sticky='W', pady=5)
    label3 = tkinter.StringVar()
    entry3 = tkinter.Entry(monty3, bg='#ffffff', width=20, textvariable=label3).grid(column=1, row=1, sticky='W')

    input_name4 = ttk.Label(monty3, text='UDP端口号').grid(column=3, row=1, sticky='W')
    label4 = tkinter.StringVar()
    entry4 = tkinter.Entry(monty3, bg='#ffffff', width=20, textvariable=label4).grid(column=4, row=1, sticky='W')

    input_name5 = ttk.Label(monty3, text='本机号').grid(column=0, row=2, sticky='W', pady=5)
    label5 = tkinter.StringVar()
    entry5 = tkinter.Entry(monty3, bg='#ffffff', width=20, textvariable=label5).grid(column=1, row=2, sticky='W')

    input_name6 = ttk.Label(monty3, text='连接方式').grid(column=0, row=3, sticky='W', pady=5)
    label6 = tkinter.StringVar()
    entry6 = tkinter.Entry(monty3, bg='#ffffff', width=20, textvariable=label6).grid(column=1, row=3, sticky='W')




    select_button = tkinter.Button(monty3, bg='white', text='连接', width=10, height=1,)
    select_button.grid(column=3, row=3, sticky='W',pady=5)
    insert_button = tkinter.Button(monty3, bg='white', text='断开', width=10, height=1)
    insert_button.grid(column=4, row=3, sticky='W',padx=5, pady=5)
    #
    # delete_button = tkinter.Button(monty3, bg='white', text='删除', width=10, height=1,command=lambda: delete(monty3, label7))
    # delete_button.grid(column=2, row=7, sticky='W', pady=5)
    root.mainloop()

main3()
