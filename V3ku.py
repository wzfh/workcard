# 日期时间
def tim(data):
    a = data[8:-12][:12]
    n = int(a[:2], 16)
    y = int(a[2:4], 16)
    r = int(a[4:6], 16)
    s = int(a[6:8], 16)
    f = int(a[8:10], 16)
    m = int(a[10:12], 16)
    return '20{}年{}月{}日{}时{}分{}秒'.format(n, y, r, s, f, m)


# 卫星信息
def wx(data):
    a = data[8:-12][12:14]
    wxcd = int(a[:1], 16)
    wxs = int(a[1:3], 16)
    return '卫星长度：{}，卫星数：{}'.format(wxcd, wxs)


# 经纬度
def jwdu(data):
    wd = data[8:-12][14:22]
    jd = data[8:-12][22:30]
    wd1 = int(int(wd, 16) / 30000 / 60)
    jd1 = int(int(jd, 16) / 30000 / 60)
    return '纬度:{},经度:{}'.format(wd1, jd1)


# 速度
def sdu(data):
    a = data[8:-12][30:32]
    return '{}'.format(int(a, 16))


# 状态航向
def hx(data):
    a = data[8:-12][32:36]
    a1 = bin(int(a[:2], 16))[2:].zfill(8)
    a2 = bin(int(a[2:], 16))[2:].zfill(8)
    hxzt = int(a1[-2:] + a2, 2)
    if a1[2:6][0] == '0':
        b = '实时GPS'
    else:
        b = '差分定位'
    if a1[2:6][1] == '1':
        c = 'GPS已定位'
    else:
        c = 'GPS没有定位'
    if a1[2:6][2] == '0':
        d = '东经'
    else:
        d = '西经'
    if a1[2:6][3] == '1':
        e = '北纬'
    else:
        e = '南纬'
    return '状态：{},{},{},{},航向：{}°'.format(b, c, d, e, hxzt)


# ACC状态
def acc(data):
    a = data[8:-12][52:54]
    if a == '00':
        b = '关'
    else:
        b = '开'
    return 'ACC状态：{}'.format(b)


# 数据上报模式
def sjusb(data):
    a = data[8:-12][54:56]
    if a == '00':
        b = '定时上传'
    elif a == '01':
        b = '定距上传'
    elif a == '02':
        b = '拐点上传'
    elif a == '03':
        b = 'ACC状态改变上传'
    elif a == '04':
        b = '静止最后位置上传'
    elif a == '05':
        b = '上电登录成功后直接上传'
    return '数据上报模式：{}'.format(b)


# GPS传输
def gpsbc(data):
    a = data[8:-12][56:58]
    if a == '00':
        b = '实时上传'
    elif a == '01':
        b = '补传'
    return 'GPS传输：{}'.format(b)


# 终端状态（报警数据包）
def bjzdxx(data):
    a = data[8:-12][54:56]
    b = bin(int(a, 16))[2:].zfill(8)
    print(a)
    print(b)
    if b[0] == '0':
        c = '油电接通'
    else:
        c = '油电断开'
    if b[1] == '1':
        d = 'GPS 已定位'
    else:
        d = 'GPS 未定位'
    if b[2:5] == '110':
        e = '超速报警'
    elif b[2:5] == '101':
        e = '超时报警（疲劳驾驶）'
    elif b[2:5] == '100':
        e = 'SOS 求救'
    elif b[2:5] == '011':
        e = '低电报警'
    elif b[2:5] == '010':
        e = '断电报警'
    elif b[2:5] == '001':
        e = '震动报警'
    elif b[2:5] == '000':
        e = '正常'
    if b[5] == '1':
        f = '已接电源充电'
    else:
        f = '未接电源充电'
    if b[6] == '0':
        g = 'ACC 低'
    else:
        g = 'ACC 高'
    if b[7] == '0':
        h = '撤防'
    else:
        h = '设防'
    # print('终端状态：{}，{}，{}，{}，{}，{}'.format(c, d, e, f, g, h))
    return '终端状态：{}，{}，{}，{}，{}，{}'.format(c, d, e, f, g, h)

# 终端状态（心跳数据包）
def xtzdxx(data):
    a = data[8:-12][:2]
    b = bin(int(a, 16))[2:].zfill(8)
    if b[0] == '0':
        c = '油电接通'
    else:
        c = '油电断开'
    if b[1] == '1':
        d = 'GPS 已定位'
    else:
        d = 'GPS 未定位'
    if b[2:5] == '110':
        e = '超速报警'
    elif b[2:5] == '101':
        e = '超时报警'
    elif b[2:5] == '100':
        e = '预留'
    elif b[2:5] == '011':
        e = '低电报警'
    elif b[2:5] == '010':
        e = '断电报警'
    elif b[2:5] == '001':
        e = '震动报警'
    elif b[2:5] == '000':
        e = '正常'
    if b[5] == '1':
        f = '已接电源充电'
    else:
        f = '未接电源充电'
    if b[6] == '0':
        g = 'ACC 低'
    else:
        g = 'ACC 高'
    if b[7] == '0':
        h = '撤防'
    else:
        h = '设防'
    return '终端状态：{}，{}，{}，{}，{}，{}'.format(c, d, e, f, g, h)

# 电压等级(报警数据包)
def bjdydji(data):
    a = data[8:-12][56:58]
    if a[1] == '0':
        b = '无电关机'
    elif a[1] == '1':
        b = '电量极低(不足以打电话发短信等)'
    elif a[1] == '2':
        b = '电量很低'
    elif a[1] == '3':
        b = '电量低(可正常使用)'
    elif a[1] == '4':
        b = '电量中'
    elif a[1] == '5':
        b = '电量高'
    elif a[1] == '6':
        b = '电量极高'
    return '电压等级：{}'.format(b)

# 电压等级(心跳数据包)
def xtdydji(data):
    a = data[8:-12][2:4]
    if a[1] == '0':
        b = '无电关机'
    elif a[1] == '1':
        b = '电量极低(不足以打电话发短信等)'
    elif a[1] == '2':
        b = '电量很低'
    elif a[1] == '3':
        b = '电量低(可正常使用)'
    elif a[1] == '4':
        b = '电量中'
    elif a[1] == '5':
        b = '电量高'
    elif a[1] == '6':
        b = '电量极高'
    return '电压等级：{}'.format(b)

# GSM 信号强度等级(报警数据包)
def bjgsmqd(data):
    a = data[8:-12][58:60]
    if a[1] == '0':
        b = '无信号'
    elif a[1] == '1':
        b = '信号极弱'
    elif a[1] == '2':
        b = '信号较弱'
    elif a[1] == '3':
        b = '信号良好'
    elif a[1] == '4':
        b = '信号强'

    return 'GSM信息强度：{}'.format(b)

# GSM 信号强度等级(心跳数据包)
def xtgsmqd(data):
    a = data[8:-12][4:6]
    if a[1] == '0':
        b = '无信号'
    elif a[1] == '1':
        b = '信号极弱'
    elif a[1] == '2':
        b = '信号较弱'
    elif a[1] == '3':
        b = '信号良好'
    elif a[1] == '4':
        b = '信号强'

    return 'GSM信息强度：{}'.format(b)

# 报警语言(报警数据包)
def bjbjyy(data):
    a = data[8:-12][60:64]
    if a[1:2] == '0':
        b = '正常'
    elif a[1:2] == '1':
        b = 'SOS 求救'
    elif a[1:2] == '2':
        b = '断电报警'
    elif a[1:2] == '3':
        b = '震动报警'
    elif a[1:2] == '4':
        b = '进围栏报警'
    elif a[1:2] == '5':
        b = ' 出围栏报警'
    elif a[1:2] == '6':
        b = '超速报警'
    elif a[1:2] == '9':
        b = '位移报警'
    elif a[1:2] == 'A':
        b = '伪基站报警'
    elif a[1:2] == 'D':
        b = '碰撞报警'
    elif a[1:2] == 'E':
        b = '非法启动报警'
    elif a[1:2] == 'F':
        b = '寻车报警'
    if a[2:4] == '01':
        c = '中文'
    elif a[2:4] == '02':
        c = '英文'
    return '报警/语言：{}/{}'.format(b, c)

# 报警语言(心跳数据包)
def xtbjyy(data):
    a = data[8:-12][6:10]
    if a[1:2] == '0':
        b = '正常'
    elif a[1:2] == '1':
        b = 'SOS 求救'
    elif a[1:2] == '2':
        b = '断电报警'
    elif a[1:2] == '3':
        b = '震动报警'
    elif a[1:2] == '4':
        b = '进围栏报警'
    elif a[1:2] == '5':
        b = ' 出围栏报警'
    elif a[1:2] == '6':
        b = '超速报警'
    elif a[1:2] == '9':
        b = '位移报警'
    elif a[1:2] == 'A':
        b = '伪基站报警'
    elif a[1:2] == 'D':
        b = '碰撞报警'
    elif a[1:2] == 'E':
        b = '非法启动报警'
    elif a[1:2] == 'F':
        b = '寻车报警'
    if a[2:4] == '01':
        c = '中文'
    elif a[2:4] == '02':
        c = '英文'
    return '报警/语言：{}/{}'.format(b, c)


if __name__ == '__main__':
    data = '78782526170306061808C002780E9B0C4472620004000801CC0025540000000900040302007A4F740D0A'
    # data='78780A13770603000100033F5A0D0A'
    bjzdxx(data)
