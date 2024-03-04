def 报警标志(data):
    a=data[26:34]
    print(a)
    a2 = bin(int(a, 16))[2:].zfill(32)
    print(a2)
    baojin=[]
    if  a2[-1:] == '1':
        b='紧急报警'
        baojin.append(b)
    if a2[-2:-1] == '1':
        b='预警'
        baojin.append(b)
    if a2[-3:-2] == '1':
        b='卫星定位模块发生故障'
        baojin.append(b)
    if a2[-4:-3] == '1':
        b='卫星定位天线未接或被剪断'
        baojin.append(b)
    if a2[-5:-4] == '1':
        b='卫星定位天线短路'
        baojin.append(b)
    if a2[-6:-5] == '1':
        b='ISU主电源欠压'
        baojin.append(b)
    if a2[-7:-6] == '1':
        b='ISU主电源掉电'
        baojin.append(b)
    if a2[-8:-7] == '1':
        b='液晶(LCD)显示ISU故障'
        baojin.append(b)
    if a2[-9:-8] == '1':
        b='语音合成(TIS)模块故障'
        baojin.append(b)
    if a2[-10:-9] == '1':
        b='摄像头故障'
        baojin.append(b)
    if a2[-11:-10] == '1':
        b='计价器故障'
        baojin.append(b)
    if a2[-12:-11] == '1':
        b='服务评价器故障(前后排)'
        baojin.append(b)
    if a2[-13:-12] == '1':
        b='LED广告屏故障'
        baojin.append(b)
    if a2[-14:-13] == '1':
        b='液晶(LED)显示屏故障'
        baojin.append(b)
    if a2[-15:-14] == '1':
        b='安全访问模块故障'
        baojin.append(b)
    if a2[-16:-15] == '1':
        b='LED顶灯故障'
        baojin.append(b)
    if a2[-17:-16] == '1':
        b='超速报警'
        baojin.append(b)
    if a2[-18:-17] == '1':
        b='连续驾驶超时'
        baojin.append(b)
    if a2[-19:-18] == '1':
        b='当天累计驾驶超时'
        baojin.append(b)
    if a2[-20:-19] == '1':
        b='超时停车'
        baojin.append(b)
    if a2[-21:-20] == '1':
        b='进出区域/路线'
        baojin.append(b)
    if a2[-22:-21] == '1':
        b='路段行驶时间不足/过长'
        baojin.append(b)
    if a2[-23:-22] == '1':
        b='禁行路段行驶'
        baojin.append(b)
    if a2[-24:-23] == '1':
        b='车速传感器故障'
        baojin.append(b)
    if a2[-25:-24] == '1':
        b='车辆非法点火'
        baojin.append(b)
    if a2[-26:-25] == '1':
        b='车辆非法位移'
        baojin.append(b)
    if a2[-27:-26] == '1':
        b='ISU存储异常'
        baojin.append(b)
    if a2[-28:-27] == '1':
        b='录音设备故障'
        baojin.append(b)
    if a2[-29:-28] == '1':
        b='计价器实时时钟超过规定的误差范围'
        baojin.append(b)
    if a2 == '0'.zfill(32):
        baojin='正常'
    print(baojin)
    return '报警标志：{}'.format(baojin)

def 报警标志1(data):
    a=data[76:84]
    print(a)
    a2 = bin(int(a, 16))[2:].zfill(32)
    baojin=[]
    if  a2[-1:] == '1':
        b='紧急报警'
        baojin.append(b)
    if a2[-2:-1] == '1':
        b='预警'
        baojin.append(b)
    if a2[-3:-2] == '1':
        b='卫星定位模块发生故障'
        baojin.append(b)
    if a2[-4:-3] == '1':
        b='卫星定位天线未接或被剪断'
        baojin.append(b)
    if a2[-5:-4] == '1':
        b='卫星定位天线短路'
        baojin.append(b)
    if a2[-6:-5] == '1':
        b='ISU主电源欠压'
        baojin.append(b)
    if a2[-7:-6] == '1':
        b='ISU主电源掉电'
        baojin.append(b)
    if a2[-8:-7] == '1':
        b='液晶(LCD)显示ISU故障'
        baojin.append(b)
    if a2[-9:-8] == '1':
        b='语音合成(TIS)模块故障'
        baojin.append(b)
    if a2[-10:-9] == '1':
        b='摄像头故障'
        baojin.append(b)
    if a2[-11:-10] == '1':
        b='计价器故障'
        baojin.append(b)
    if a2[-12:-11] == '1':
        b='服务评价器故障(前后排)'
        baojin.append(b)
    if a2[-13:-12] == '1':
        b='LED广告屏故障'
        baojin.append(b)
    if a2[-14:-13] == '1':
        b='液晶(LED)显示屏故障'
        baojin.append(b)
    if a2[-15:-14] == '1':
        b='安全访问模块故障'
        baojin.append(b)
    if a2[-16:-15] == '1':
        b='LED顶灯故障'
        baojin.append(b)
    if a2[-17:-16] == '1':
        b='超速报警'
        baojin.append(b)
    if a2[-18:-17] == '1':
        b='连续驾驶超时'
        baojin.append(b)
    if a2[-19:-18] == '1':
        b='当天累计驾驶超时'
        baojin.append(b)
    if a2[-20:-19] == '1':
        b='超时停车'
        baojin.append(b)
    if a2[-21:-20] == '1':
        b='进出区域/路线'
        baojin.append(b)
    if a2[-22:-21] == '1':
        b='路段行驶时间不足/过长'
        baojin.append(b)
    if a2[-23:-22] == '1':
        b='禁行路段行驶'
        baojin.append(b)
    if a2[-24:-23] == '1':
        b='车速传感器故障'
        baojin.append(b)
    if a2[-25:-24] == '1':
        b='车辆非法点火'
        baojin.append(b)
    if a2[-26:-25] == '1':
        b='车辆非法位移'
        baojin.append(b)
    if a2[-27:-26] == '1':
        b='ISU存储异常'
        baojin.append(b)
    if a2[-28:-27] == '1':
        b='录音设备故障'
        baojin.append(b)
    if a2[-29:-28] == '1':
        b='计价器实时时钟超过规定的误差范围'
        baojin.append(b)
    if a2 == '0'.zfill(32):
        baojin='正常'
    print(baojin)
    return '报警标志1：{}'.format(baojin)

def 车辆状态(data):
    a = data[34:42]
    a2 = bin(int(a, 16))[2:].zfill(32)
    if a2[-1:] =='0':
        b='已卫星定位'
    else:
        b='未卫星定位'
    if a2[-2:-1] =='0':
        c='北纬'
    else:
        c='南纬'
    if a2[-3:-2] =='0':
        d='东经'
    else:
        d='西经'
    if a2[-4:-3] =='0':
        e='运营状态'
    else:
        e='停运状态'
    if a2[-5:-4] =='0':
        f='未预约'
    else:
        f='预约（任务车）'
    if a2[-6:-5] =='0':
        g='默认'
    else:
        g='空转重'
    if a2[-7:-6] =='0':
        h='默认'
    else:
        h='重转空'
    if a2[-9:-8] =='0':
        i='ACC关'
    else:
        i='ACC开'
    if a2[-10:-9] =='0':
        j='空车'
    else:
        j='重车'
    if a2[-11:-10] =='0':
        k='车辆油路正常'
    else:
        k='车辆油路断开'
    if a2[-12:-11] =='0':
        l='车辆电路正常'
    else:
        l='车辆电路断开'
    if a2[-13:-12] =='0':
        m='车门解锁'
    else:
        m='车门加锁'
    if a2[-14:-13] =='0':
        n='车辆未锁定'
    else:
        n='车辆锁定'
    if a2[-15:-14] =='0':
        o='未到达限制营运次数#时间'
    else:
        o='已达到限制营运次数#时间'
    print('车辆状态：{}，{}，{}，{}，{}，{}，{}，{}，{}，{}，{}，{}，{}，{}'.format(b, c, d, e, f, g, h, i, j, k, l, m, n, o))
    return '车辆状态：{}，{}，{}，{}，{}，{}，{}，\n                     {}，{}，{}，{}，{}，\n                     {}，{}'.format(b,c, d, e, f, g, h,i,j,k,l,m,n,o)

def 车辆状态1(data):
    a = data[84:92]
    a2 = bin(int(a, 16))[2:].zfill(32)
    if a2[-1:] =='0':
        b='已卫星定位'
    else:
        b='未卫星定位'
    if a2[-2:-1] =='0':
        c='北纬'
    else:
        c='南纬'
    if a2[-3:-2] =='0':
        d='东经'
    else:
        d='西经'
    if a2[-4:-3] =='0':
        e='运营状态'
    else:
        e='停运状态'
    if a2[-5:-4] =='0':
        f='未预约'
    else:
        f='预约（任务车）'
    if a2[-6:-5] =='0':
        g='默认'
    else:
        g='空转重'
    if a2[-7:-6] =='0':
        h='默认'
    else:
        h='重转空'
    if a2[-9:-8] =='0':
        i='ACC关'
    else:
        i='ACC开'
    if a2[-10:-9] =='0':
        j='空车'
    else:
        j='重车'
    if a2[-11:-10] =='0':
        k='车辆油路正常'
    else:
        k='车辆油路断开'
    if a2[-12:-11] =='0':
        l='车辆电路正常'
    else:
        l='车辆电路断开'
    if a2[-13:-12] =='0':
        m='车门解锁'
    else:
        m='车门加锁'
    if a2[-14:-13] =='0':
        n='车辆未锁定'
    else:
        n='车辆锁定'
    if a2[-15:-14] =='0':
        o='未到达限制营运次数#时间'
    else:
        o='已达到限制营运次数#时间'
    print('车辆状态：{}，{}，{}，{}，{}，{}，{}，{}，{}，{}，{}，{}，{}，{}'.format(b, c, d, e, f, g, h, i, j, k, l, m, n, o))
    return '车辆状态1：{}，{}，{}，{}，{}，{}，{}，\n                     {}，{}，{}，{}，{}，\n                     {}，{}'.format(b,c, d, e, f, g, h,i,j,k,l,m,n,o)

def 签退方式(data):
    a = data[256:258]
    if a =='00':
        return '正常签退'
    else:
        return '强制签退'

def 经纬度1(data):
    wd=data[92:100]
    jd=data[100:108]
    wd2=int(wd,16)*0.0001/60
    jd2 = int(jd, 16) * 0.0001 / 60
    print(str(wd2)[:9])
    print(str(jd2)[:10])
    return '纬度1：{}，经度1：{}'.format(str(wd2)[:9],str(jd2)[:10])

def 经纬度(data):
    wd=data[42:50]
    jd=data[50:58]
    wd2=int(wd,16)*0.0001/60
    jd2 = int(jd, 16) * 0.0001 / 60
    print(str(wd2)[:9])
    print(str(jd2)[:10])
    return '纬度：{}，经度：{}'.format(str(wd2)[:9],str(jd2)[:10])

def 速度(data):
    sd=data[58:62]
    sd1=int(sd,16)/10
    print(sd1)
    return '速度：{}'.format(sd1)

def 速度1(data):
    sd=data[108:112]
    sd1=int(sd,16)/10
    print(sd1)
    return '速度1：{}'.format(sd1)

def 评价选项(data):
    a=data[142:144]
    if a == '00':
        return '没有做出评价'
    elif a == '01':
        return '满意'
    elif a == '02':
        return '一般'
    elif a == '03':
        return '不满意'
    elif a == '04':
        return '投诉'

def 电召订单ID(data):
    a=data[148:156]
    if a =='0'.zfill(8):
        return f'{a}(正常营运数据)'
    else:
        a=int(a)
        return f'{a}(标识电召营运数据)'

def 交易类型(data):
    a=data[286:288]
    if a=='00':
        return '现金交易'
    elif a=='01':
        return 'M1卡交易'
    elif a=='03':
        return 'CPU卡交易'
    elif a=='09':
        return '其他'


if __name__ == '__main__':
    data='7E0B0500731013510000000001000000000000030000D2AEC7041BF93200C80123120715513900000000000003000127FDF20416D17500C8012312071551393590AA283590AA2801000000000200534E31323535534E3132333435363738393100000000534E31323334353637383931323334353637342312071521155100001000350000200200000120000000000901040000006E0202044C250400000000300103AF7E'
    print(data[26:84])
    # print(data[76:84])
    报警标志(data)
    # 速度(data)
    # a2= bin(int(data[26:34], 16))[2:].zfill(32)
    # print(a2)
    # print(a2[-3:])
    # 经纬度(data)



