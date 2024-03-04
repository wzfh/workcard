# _*_ coding:utf-8 _*_

import re
import time
def get_bcc(inputStr: str) -> str:
    bcc = 0
    for i in inputStr.split(' '):
        bcc = bcc ^ int(i, 16)

    return f'{bcc:x}'

def get_xor(data):
    result = re.sub(r"(?<=\w)(?=(?:\w\w)+$)", " ", data)
    return result

if __name__ == '__main__':

    data = '0200004D1013560000000001000000000000000004168C6F00D2F2BF00000010000C230627162554642F00000001010101102000000010000004168C6F00D2F2BF230627162554000030303030303030230627162554000100'
    q='7e0b03003f1033057751830002000000000000000000000000000000000000002306271723003131313131313131313131313131313132323232323232323232323232323232323232c66666747e'
    # print(q.upper())
    a = get_xor(data)
    b = get_bcc(a)
    # print(b)
    # print(a)
    # now_time = time.strftime('%Y%m%d%H%M%S', time.localtime())
    # print(now_time[2:])
