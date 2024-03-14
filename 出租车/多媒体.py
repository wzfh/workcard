# -*- coding: utf-8 -*-
"""
@Time ： 2024/3/8 11:01
@Auth ： 锋
@File ：多媒体.py
@IDE ：PyCharm
@Motto：ABC(Always Be Coding)

"""
import os
import time
from socket import socket, AF_INET, SOCK_STREAM


# def my_function():
#     time.sleep(10)
#     os.makedirs(r'C:\Users\rjcsyb2\Desktop\workcard\123')


def countdown(t):
    for i in range(t):
        print("\r休眠倒计时：%02d" % (t - i) + '秒', end='')
        time.sleep(1)


#     atexit.register(my_function)


path = r'C:\Users\rjcsyb2\Desktop'
file_path = os.path.join(path, "多媒体1.txt")
with open(file_path, "r") as file:
    for line in file:
        print(line.strip())
        s = socket(AF_INET, SOCK_STREAM)
        s.connect(('120.79.74.223', 17201))  # 测试
        # s.connect(('120.79.176.183', 17800))#压测
        # s.connect(('47.119.168.112', 17800))#生产
        s.send(bytes().fromhex(line.strip()))
        send = s.recv(1024).hex()
        print('服务器应答：' + send.upper())
        print('\n' * 1)
        countdown(10)
