# coding=utf-8
import binascii
import csv
import os
import re
import time
from socket import socket, AF_INET, SOCK_STREAM

import diaoyongjar
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
    test=hex(crc).upper()
    return  test

def get_xor(data):
    result = re.sub(r"(?<=\w)(?=(?:\w\w)+$)", " ", data)
    return result

class dwei:
    def get(self, nob, noc):
        # path = os.path.dirname(os.path.dirname(__file__))
        # file_path = path + '/excelFile/boyunshikong/boxbox/dingwei.csv'
        # fCase = open(file_path, 'r', encoding='gbk')
        # datas = csv.reader(fCase)
        # data1 = []
        # o = 0
        # for line in datas:
        #     data1.append(line)
        #     print(line)
        # print(data1)
        # for nob1 in range(1, nob):
        #     t = data1[nob1]
        #     o += 1
            # print('发送第%d条' % o)

            # 起始位
            # qsw=t[0].zfill(4)
            qsw = '7878'

            # 包长度(5+信息内容长度)
            bcd1 = '34'
            bcd = hex(int(bcd1))[2:].upper()
            # bcd='1F'
            # print('包长度'+bcd)

            # 协议号
            # xyh = t[2].zfill(2).upper()
            # xyh='12'

            # 日期时间
            ti = time.strftime("%Y%m%d%H%M%S")
            ti2 = str(ti)
            ti3 = 2 * '' + ti2[2:]
            ti4 = (hex(int(ti3[0:2]))[2:4]).zfill(2)
            ti5 = (hex(int(ti3[2:4]))[2:4]).zfill(2)
            ti6 = (hex(int(ti3[4:6]))[2:4]).zfill(2)
            ti7 = (hex(int(ti3[6:8])-8)[2:4]).zfill(2)
            ti8 = (hex(int(ti3[8:10]))[2:4]).zfill(2)
            ti9 = (hex(int(ti3[10:12]))[2:4]).zfill(2)
            ti10 = ti4 + ti5 + ti6 + ti7 + ti8 + ti9
            ti10 = ti10.upper()
            # ti10='16081007141E'
            print(ti10)

            # GPS信息长度
            # gpscd = t[4]
            # gpscd1 = hex(int(gpscd))[2:].upper()
            # print('信息长度' + gpscd1)

            # 卫星个数
            # gpsgs = t[5]
            # gpsgs1 = hex(int(gpsgs))[2:].upper()
            # print(gpsgs1)

            # GPS信息卫星
            # gps = gpscd1 + gpsgs1
            # print(gps)



            # # 36、纬度
            # # wd = t[3]
            # wd = '23.014743'
            # wd1 = float(wd) * 1000000
            # # print(weidu1)
            # wd2 = hex(int(wd1))[2:].zfill(8).upper()
            # print('纬度' + wd2)

            # # 37、经度
            # # jd = t[4]
            # jd = '113.398502'
            # jd1 = float(jd) * 1000000
            # jd2 = hex(int(jd1))[2:].zfill(8).upper()
            # print('经度' + jd2)

            # # # 纬度
            # wd=t[6].zfill(8).upper()
            # wd='015F2DBB'
            wd = '027AC7EB'
            # wd='CF02C64D'

            # # 经度
            # jd=t[7].zfill(8).upper()
            jd = '06C247F6'
            # jd='06C247F6'

            # 速度
            # sd1 = t[8]
            # sd = hex(int(sd1))[2:].zfill(2).upper()
            # print(sd)

            # 航向状态
            # hxzt=t[9].zfill(4)
            # hxzt='14F9'
            hxzt = '15B5'

            # MCC
            mcc1 = '460'
            mcc = hex(int(mcc1))[2:].zfill(4).upper()

            # MNC
            # mnc = t[11].zfill(2).upper()
            mnc = '01CC'

            # LAC
            # lac = t[12].zfill(4).upper()
            lac = '262C'

            # Cell ID
            # cellid = t[13].zfill(6).upper()
            cellid = '000EBA'

            # ACC
            # acc=t[14].zfill(2).upper()
            acc = '00'
            print(acc)

            # 数据上报模式
            # sjms = t[15].zfill(2).upper()

            # GPS实时补传
            # gpsbc = t[16].zfill(2).upper()

            # 信息序列号
            # xxxlh = t[17].zfill(4)
            xxxlh = '0007'
            # xxxlh='0003'

            # 错误校验
            # cwjy=t[18].zfill(4)
            # cwjy=bcd+xyh+ti10+gps+wd+jd+sd+hxzt+mcc+mnc+lac+cellid+acc+sjms+gpsbc+xxxlh
            # cwjy=bcd+xyh+ti10+gps+wd2+jd2+sd+hxzt+mcc+mnc+lac+cellid+acc+sjms+gpsbc+xxxlh
            # cwjy = '22' + '22' + ti10 + 'CF' + wd + jd + '10148F01CC00287D001FB80001'  # ACC 开
            # cwjy='1F'+'12'+ti10+'CF'+wd+jd+'00148F01CC00287D001FB80001'   #ACC 开,速度0
            # cwjy='22'+'22'+ti10+f'CF027AC7EB0C46584900D54C01CC00287D001FB8{acc}00000007'
            cwjy='22'+'22'+ti10+f'CF027AC7EB0C46584911D54C01CC00287D001FB8{acc}01000007'
            # cwjy='1F12160809073509CF02D364B809581B7C2C14F6019508037D006D13019D'
            # print(cwjy)
            # cwjy=bcd+xyh+ti10+'CF'+wd+jd+'001561019508036A0063ED0001'
            cwjy1 = crc1(cwjy)[2:].zfill(4).upper()
            # print(cwjy)
            print('错误校验'+cwjy1)

            # 停止位
            # tzw=t[19].zfill(4)
            tzw = '0D0A'

            w = qsw + cwjy + cwjy1 + tzw
            # print(w)

            # 组合校验
            data = w
            a = get_xor(data)
            print(a)
            t = a + ''
            q=w
            print(t)
            # return '定位包数据：{}\n\n原始数据：{}'.format(t,q)

            s = socket(AF_INET, SOCK_STREAM)
            # s.connect(('47.52.50.49', 6695))
            s.connect(('120.77.133.46', 6695))
            s.send(bytes().fromhex(t))

            send = s.recv(1024).hex()
            print(send.upper())
            print('\n' * 1)
            # time.sleep(2)
            # s.close()


if __name__ == '__main__':
    ll = dwei()
    ll.get(2, 1)
