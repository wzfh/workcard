import binascii


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


# data='787811010863013865432142010032000001A38B0D0A'
# res=crc1(data)
# print(res)



def shebeihao2Vip(sSim):
    if sSim is None or sSim == "":
        return None
    try:
        sTemp = []
        sIp = []
        if len(sSim) == 11:
            sTemp.append(int(sSim[3:5]))
            sTemp.append(int(sSim[5:7]))
            sTemp.append(int(sSim[7:9]))
            sTemp.append(int(sSim[9:11]))
            iHigt = int(sSim[1:3]) - 30
            print(iHigt)
        elif len(sSim) == 10:
            sTemp.append(int(sSim[2:4]))
            sTemp.append(int(sSim[4:6]))
            sTemp.append(int(sSim[6:8]))
            sTemp.append(int(sSim[8:10]))
            iHigt = int(sSim[0:2]) - 30
            print(iHigt)
        elif len(sSim) == 9:
            sTemp.append(int(sSim[1:3]))
            sTemp.append(int(sSim[3:5]))
            sTemp.append(int(sSim[5:7]))
            sTemp.append(int(sSim[7:9]))
            iHigt = int(sSim[0:1])
            print(iHigt)
        elif len(sSim) < 9:
            sSim = "140" + sSim.zfill(8)
            sTemp.append(int(sSim[3:5]))
            sTemp.append(int(sSim[5:7]))
            sTemp.append(int(sSim[7:9]))
            sTemp.append(int(sSim[9:11]))
            iHigt = int(sSim[1:3]) - 30
            print(iHigt)
        else:
            return None
        print(sTemp)
        if (iHigt & 0x8) != 0:
            sIp.append(sTemp[0] | 128)
            print(sTemp[0] | 128)
        else:
            sIp.append(sTemp[0])
            print(sTemp[0])
        if (iHigt & 0x4) != 0:
            sIp.append(sTemp[1] | 128)
            print(sTemp[1] | 128)
        else:
            sIp.append(sTemp[1])
            print(sTemp[1])
        if (iHigt & 0x2) != 0:
            sIp.append(sTemp[2] | 128)
            print(sTemp[2] | 128)
        else:
            sIp.append(sTemp[2])
            print(sTemp[2])
        if (iHigt & 0x1) != 0:
            sIp.append(sTemp[3] | 128)
            print(sTemp[3] | 128)
        else:
            sIp.append(sTemp[3])
            print(sTemp[3])
        print(sIp)
        ipstr = ""
        for ip in sIp:
            ss = str(hex(ip))[2:].zfill(2)
            ipstr += ss
        print(ipstr.upper())
        return ipstr.upper()
    except Exception as e:
        print("设备号转伪ip失败！原因：%s" % e)
        return None

# shebeihao2Vip('13534912299')

# import os
#
# # 替换为你的文件夹路径
# folder_path = r'C:\Users\rjcsyb2\Desktop\BSJ-协议解析器'
#
# # 获取文件夹内的所有文件名
# # current_directory = os.getcwd()
# # print(current_directory)
# import subprocess
#
# # # 遍历文件名并处理每个文件
# #
# #
# exe = os.path.join(folder_path, 'BSJ_dataParser.exe')
#
# # subprocess.Popen(exe1)
# subprocess.run(exe)
