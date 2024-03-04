# coding=utf-8
import binascii
import csv
import os
import re

import diaoyongjar


def get_xor(data):
    result = re.sub(r"(?<=\w)(?=(?:\w\w)+$)", " ", data)
    return result

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

class pant:
    def get(self, nob, noc):
        # path = os.path.dirname(os.path.dirname(__file__))
        # file_path = path + '/excelFile/boyunshikong/boxbox/pant.csv'
        # fCase = open(file_path, 'r', encoding='gbk')
        # datas = csv.reader(fCase)
        # data1 = []
        # o = 0
        # for line in datas:
        #     data1.append(line)
        # for nob1 in range(1, nob):
        #     t = data1[nob1]
        #     o += 1

            # 起始位
            # qsw = t[0].zfill(4).upper()
            qsw='7878'

            # 包长度(5+信息内容长度)
            # bcd1 = t[1]
            # bcd = hex(int(bcd1))[2:].zfill(2).upper()

            # 协议号
            # xyh = t[2].zfill(2).upper()
            # xyh = '13'

            # 终端信息内容
            # zdxxnr1 = t[3]
            # zdxxnr = hex(int(zdxxnr1))[2:].upper()
            # zdxxnr = '44'#关
            zdxxnr = '77'#开
            print(zdxxnr)

            # 电压等级
            # dydj = t[4].zfill(2).upper()
            dydj = '04'

            # GSM信号强度
            # gsm = t[5].zfill(2).upper()
            gsm='04'
            # print(gsm)

            # 报警语言扩展口
            # bjyy = t[6].zfill(4).upper()
            bjyy = '0002'

            # 信息序列号
            # xxxlh=t[7].zfill(4).upper()
            xxxlh = '0003'

            # 错误校验
            # cwjy=t[8].zfill(4)
            # cwjy = bcd + xyh + zdxxnr + dydj + gsm + bjyy + xxxlh
            cwjy = '0A1377060300010003'
            cwjy1 = crc1(cwjy)[2:].upper()
            # print('错误校验' + cwjy1)

            # 停止位
            # tzw=t[9].zfill(4).upper()
            tzw = '0D0A'

            # w = qsw + bcd + xyh + zdxxnr + dydj + gsm + bjyy + xxxlh + cwjy1 + tzw
            w = qsw+cwjy + cwjy1 + tzw
            print(w)

            data=w
            a= get_xor(data)


            t=a + ''
            q=w
            print(t)
            return '心跳包数据：{}\n\n原始数据：{}'.format(t,q)

            # s = socket(AF_INET, SOCK_STREAM)
            # s.connect(('47.52.50.49', 6695))
            # s.send(bytes().fromhex(t))
            # print('\n' * 1)
            # time.sleep(2)
            # s.close()

if __name__ == '__main__':
    ll=pant()
    ll.get(2,1)