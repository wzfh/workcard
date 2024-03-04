#coding=utf-8
import binascii
import csv
import os.path
import random
import re
import time
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


class beep:
    def get(self,nob,noc):
        # path = os.path.dirname(__file__)
        # file_path= path + '/excelFile/beeper.csv'
        # fCase=open(file_path,'r',encoding='gbk')
        # datas=csv.reader(fCase)
        # data1=[]
        # o=0
        # for line in datas:
        #     data1.append(line)
        # for nob1 in range(1,nob):
        #     t=data1[nob1]
        #     o +=1
        #     print('发送第%d条'% o)
        #     print(t[23])

            # 起始位
            # qsw = t[0].zfill(4).upper()
            qsw='7878'

            # 包长度(5+信息内容长度)
            bcd1 = '37'
            bcd = hex(int(bcd1))[2:].upper()
            print('包长度'+bcd)

            # 协议号
            # xyh = t[2].zfill(2).upper()
            # xyh='26'
            xyh='26'

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
            # print(ti10)

            # GPS信息长度
            # gpscd = t[4]
            gpscd = '12'
            gpscd1 = hex(int(gpscd))[2:].upper()
            # print('信息长度'+gpscd1)

            # 卫星个数
            gpsgs = '11'
            gpsgs1 = hex(int(gpsgs))[2:].upper()
            # print(gpsgs1)

            # GPS信息卫星
            gps = gpscd1 + gpsgs1
            # print(gps)

            # 纬度
            # wd = t[6].zfill(8).upper()
            wd = '026DDEC0'
            # print(wd)

            # 经度
            # jd = t[7].zfill(8).upper()
            jd = '0C3BFEE6'
            # print(jd)

            # 速度
            # sd1 = t[8]
            sd = '25'

            # 航向状态
            # hxzt=t[9].zfill(4)
            hxzt = '1400'

            # LBS长度
            lbscd='08'
            # print(lbscd)

            # MCC
            mcc = '01CC'
            # print(mcc)

            # MNC
            mnc = '00'
            # print(mnc)

            # LAC
            lac = '262C'
            # print(lac)

            # Cell ID
            cellid = '000EBA'
            # print(cellid)

            # 终端信息内容
            zdxxnrs=["4C","54","64","44","74"]
            zdxxnr=random.choice(zdxxnrs)

            print(zdxxnr)

            # 电压等级
            dydj='03'
            # print(dydj)

            # GSM信号强度
            gsm = '03'
            # print(gsm)

            # 报警扩展口
            bjs=["03","00","02","04","05","06","0D","0E","09","01","11","12","10","0A","0C","0F","40","41","42","43","44"]
            bj=random.choice(bjs)
            print(bj)


            # 语言扩展口
            yy='01'
            # print(yy)

            # 信息序列号
            # xxxlh = t[20].zfill(4).upper()
            # print(xxxlh)
            xxxlh = '0003'

            # 报警语言扩展口
            bjyy=bj+yy
            # print(bjyy)

            # 错误校验
            # cwjy=t[21].zfill(4)
            cwjy = bcd + xyh +ti10+gps+wd+jd+sd+hxzt+lbscd+mcc+mnc+lac+cellid+ zdxxnr + dydj + gsm + bjyy + xxxlh
            # cwjy = bcd + xyh +'16080B0E'+'1222CF030E9AE708495E660A1541019464009B004454000C811702B9'
            cwjy1 = crc1(cwjy)[2:].upper().zfill(4)
            print('错误校验' + cwjy1)

            # 停止位
            # tzw = t[22].zfill(4).upper()
            tzw = '0D0A'

            # w=qsw+bcd+xyh+ti10+gps+wd+jd+sd+hxzt+lbscd+mcc+mnc+lac+cellid+zdxxnr + dydj + gsm + bjyy + xxxlh +cwjy1+tzw
            w=qsw+cwjy +cwjy1+tzw
            # print(w)

            data=w
            a= get_xor(data)

            t=a+''
            q=w
            print(t)
            return '报警包数据：{}\n\n原始数据：{}'.format(t, q)

            # s = socket(AF_INET, SOCK_STREAM)
            # s.connect(('47.52.50.49', 6695))
            # s.send(bytes().fromhex(t))
            # print('\n' * 1)
            # time.sleep(2)
            # s.close()



if __name__ == '__main__':
    ll=beep()
    ll.get(14,1)





