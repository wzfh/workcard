import binascii


def crc1(data):
    crc = 0xFFFF
    data = binascii.unhexlify(data)
    print(data)
    for pos in data:
        crc ^= pos
        for i in range(8):
            lsb = crc & 0x0001
            crc >>= 1
            if lsb == 1:
                crc ^= 0x8408
    crc ^= 0xffff
    test = hex(crc).upper()
    print(test)
    return test


# data='292980009FB49F12D92206161836410285869110809726000000007F000000FFF750FFFFFFFFFFFFFFFF00001000243436303B30303B333B34323431300005000429930000040008047F001800A342534A4135433857522042534A5F585556312E323BFE000600A5000000B200060089FFFFFFFF002400A900000000000000000000000000000000000000000000000000000000000000000000000600C500001000780D'
# res=crc1(data)
# print(res)


import time


def countdown(hours):
    seconds = hours * 3600
    while seconds > 0:
        print(f"\r{seconds // 3600}小时{seconds % 3600 // 60}分钟{seconds % 60}秒", end='')
        time.sleep(1)
        seconds -= 1
    print("倒计时结束！")


# 调用倒计时函数，传入需要倒计时的小时数
countdown(1)
