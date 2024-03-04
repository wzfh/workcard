# coding=utf-8
import binascii
import csv
import os
import re
import time
from socket import *

import diaoyongjar




def get_bcc(inputStr: str) -> str:
    bcc = 0
    for i in inputStr.split(' '):
        bcc = bcc ^ int(i, 16)

    return f'{bcc:x}'
def get_xor(data):
    result = re.sub(r"(?<=\w)(?=(?:\w\w)+$)", " ", data)
    return result


# print(now_time[2:])
# wd1 = 23.330217 * 60 / 0.0001
# # print(wd1)
# wd2 = hex(int(wd1))
# # print(wd2[2:].zfill(8).upper())
#
# jd1 = 114.903551 * 60 / 0.0001
# # print(jd1)
# jd2 = hex(int(jd1))
# print(jd2[2:].zfill(8).upper())
紧急报警='00000001'
进出区域路线报警='00100000'
路段行驶时间不足='00200000'
禁行路段行驶='00400000'
车辆非法点火='01000000'
车辆非法位移='02000000'
正常='00000000'

class login:
    def get(self, nob,noc):
        count=0
        for i in range(1):
            try:
                print(i)
                wd1 = 30.520167 * 60 / 0.0001
                # print(wd1)
                wd2 = hex(int(wd1))
                # print(wd2[2:].zfill(8).upper())

                jd1 = 104.042433 * 60 / 0.0001
                # print(jd1)
                jd2 = hex(int(jd1))
                # print(jd2[2:].zfill(8).upper())

                now_time = time.strftime('%Y%m%d%H%M%S', time.localtime())
                标识位='7E'
                消息ID='0B03'
                消息体属性='0043'
                # if 1 < i < 10:
                #     设备号 = f'000000000{i}'
                # if 9 < i < 100:
                #     设备号 = f'00000000{i}'
                # if 99 < i < 1000:
                #     设备号 = f'0000000{i}'
                # if 999 < i < 10000:
                #     设备号 = f'000000{i}'
                # if 9999<i<10991:
                #     设备号 = f'00000{i}'
                # 设备号 = f'1356000000'
                # ISU标识 = '10{}'.format(设备号)  # 10位
                ISU标识 = '015265236688'  # 10位
                流水号 = f'{i}'.zfill(4)

                报警=正常
                状态='00000300'
                纬度=wd2[2:].zfill(8).upper()
                经度=jd2[2:].zfill(8).upper()
                速度='0001'
                方向='00'
                时间=now_time[2:]
                # print(时间)
                企业经营许可证号='534E3132333435363738393100000000'#SN1234567891
                驾驶员从业资格证号='534E3132333435363738393132333435363738'#SN12345678912345679
                # 驾驶员从业资格证号='534E3132333435363738393132333435363730'#SN12345678912345670
                # 驾驶员从业资格证号='534E3132333435363738393132333435363731'#SN12345678912345671
                车牌号='534E31323535'#SN1255
                # now=hex(int(now_time[:12]))[2:].zfill(12).upper()
                开机时间=now_time[:12]
                # print(开机时间)
                附加='01040000006E0202044C250400000000300103'

                w=消息ID+消息体属性+ISU标识+流水号+报警+状态+纬度+经度+速度+方向+时间+企业经营许可证号+驾驶员从业资格证号+车牌号+开机时间
                a = get_xor(w)
                b = get_bcc(a)
                E = w + b.upper().zfill(2)
                t = 标识位 + E.replace("7E", "00") + 标识位
                data=get_xor(t)
                if data[:2] != "7E":
                    print(f"错误：{data}")
                    t = t[:81] + "00" + t[82:]
                    data = get_xor(t)
                    print("修改后data：{}".format(data))
                    print('\n' * 1)
                print(t)
                print(data)
                count += 1



        # return '登录包数据：{}\n\n设备号：{}\n\n原始数据：{}'.format(t,t[12:-30],q)


        #
                s = socket(AF_INET, SOCK_STREAM)
                s.connect(('120.79.74.223', 17202))
                # # s.connect(('120.79.176.183', 17800))  # 压测
                # s.connect(('47.119.168.112', 17800))  # 生产
                s.send(bytes().fromhex(data))
                send = s.recv(1024).hex()
                print(send.upper())
                print('\n' * 1)
                time.sleep(1)
                # s.close()
            except:
                pass


if __name__ == '__main__':
    ll = login()
    # for j in range(5):
    ll.get(2,1)
