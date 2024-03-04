import time
from diaoyongjar import *
from dingwei import dwei
from beeper import beep
from socket import *
from pant import pant
from V3ku import *
from tkinter import *
from tkinter.ttk import *
# coding=utf-8
import binascii
import re
LOG_LINE_NUM = 0

# menubar = Menu(init_window, tearoff=False)



def copy(editor, event=None):
    editor.event_generate("<<Copy>>")


def paste(editor, event=None):
    editor.event_generate('<<Paste>>')


def selectAll(editor, event=None):
    editor.tag_add('sel', '1.0', END)


# # def rightKey(event, editor):
#     menubar.delete(0, END)
#     menubar.add_command(label='复制', command=lambda: copy(editor))
#     menubar.add_command(label='粘贴', command=lambda: paste(editor))
#     menubar.add_command(label='全选', command=lambda: selectAll(editor))
#     menubar.post(event.x_root, event.y_root)

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
    test = hex(crc).upper()
    return test

class MY_GUI():
    def __init__(self, init_window_name):

        self.init_window_name = init_window_name


    def login(self,nob, noc):
        qsw = '7878'
        bcd1 = '17'
        bcd = hex(int(bcd1))[2:].upper()
        xyh = '01'
        zdid = '0'+self.sb_hao()
        lxsbh = '0100'
        sqyy = '3200'
        xxxlh = '0001'
        cwjy = bcd + xyh + zdid + lxsbh + sqyy + xxxlh
        cwjy1 = crc1(cwjy)[2:].zfill(4).upper()
        tzw = '0D0A'
        w = qsw + cwjy + cwjy1 + tzw
        data = w
        a = get_xor(data)
        t = a + ''
        q = w
        print(t)

        return '登录包数据：{}\n\n设备号：{}\n\n原始数据：{}'.format(t, t[12:-30], q)

    def xieyihao(self):
        data = self.str_trans_to_md5()
        data1=get_xor(data)
        sjutji = []

        # 7878110101234135484845480100320000016D3F0D0A
        if data[6:8] == '01':
            a = '01：{}\n\n'.format('登录数据包')
            b = '设备号：{}\n类型识别码：{}\n时区语言：{}\n'.format(data[8:-12][1:16], '固定为0100', data[8:-12][-4:])
            sjutji.append(a)
            sjutji.append(b)

        elif data[6:8] == '22':
            a = '22：{}\n\n'.format('定位数据包')
            b = 'GPS信息：\n日期时间：{}\n{}\n{}\n速度:{}\n{}\n'.format(tim(data), wx(data), jwdu(data), sdu(data),
                                                                      hx(data))
            c = 'LBS信息：[MCC:{},MNC:{},LAC:{},Cell ID:{}]\n{}\n{}\n{}\n'.format(data[8:-12][36:40], data[8:-12][40:42],
                                                                                 data[8:-12][42:46], data[8:-12][46:52],
                                                                                 acc(data), sjusb(data), gpsbc(data))
            sjutji.append(a), sjutji.append(b), sjutji.append(c)

        elif data[6:8] == '26':
            a = '26：{}\n\n'.format('报警数据包')
            b = '日期时间：{}\n'.format(tim(data))
            c = 'GPS信息：\n{}\n{}\n速度:{}\n{}\n'.format(wx(data), jwdu(data), sdu(data), hx(data))
            d = 'LBS信息：LBS长度：{},MCC:{},MNC:{},LAC:{},Cell ID:{}\n'.format(data[8:-12][36:38], data[8:-12][38:42],
                                                                              data[8:-12][42:44], data[8:-12][44:48],
                                                                              data[8:-12][48:54])
            e = '状态信息：\n{}\n{}\n{}\n{}\n'.format(bjzdxx(data), bjdydji(data), bjgsmqd(data), bjbjyy(data))
            sjutji.append(a), sjutji.append(b), sjutji.append(c), sjutji.append(d), sjutji.append(e)

        elif data[6:8] == '13':
            a = '13：{}\n\n'.format('心跳状态数据包')
            b = '状态信息：\n{}\n{}\n{}\n{}\n'.format(xtzdxx(data), xtdydji(data), xtgsmqd(data), xtbjyy(data))
            sjutji.append(a), sjutji.append(b)

        elif data[6:8] == '15':
            a = '15：{}'.format('终端返回字符串信息包')
            sjutji.append(a)

        elif data[6:8] == '80':
            a = '80：{}'.format('服务器向终端发送指令信息')
            sjutji.append(a)
        else:
            self.result_data_Text.delete(1.0, END)
            self.result_data_Text.insert(1.0, "请输入V3原始数据")
            self.write_log_to_Text("INFO:原始数据解析 False")
            return 0
        self.result_data_Text.delete(1.0, END)
        # self.result_data_Text.insert(1.0,data1)
        for line in sjutji:
            print(line)
            self.result_data_Text.insert(1.0, line)
        self.write_log_to_Text("INFO:原始数据解析 success")





    def str_trans_to_md5(self):
        src = self.init_data_Text.get(1.0, END).strip()
        return src

    def sb_hao(self):
        sb = self.sbei_Text.get().strip()
        print(sb)
        return sb

    def qo_login(self):
        src = self.init_data_Text1.get(1.0, END).strip()
        print(src)
        if src == '1':
            # print(self.login(2,1))
            sbb1=self.sb_hao()
            print(sbb1)
            if not sbb1:
                self.result_data_Text1.delete(1.0, END)
                self.result_data_Text1.insert(1.0, "请输入设备号")
            else:
                self.result_data_Text1.delete(1.0, END)
                self.result_data_Text1.insert(1.0, self.login(2,1))
                self.write_log_to_Text("INFO:数据包生成 success")
            return 0
        elif src == '2':
            ll = dwei()
        elif src == '3':
            ll = beep()
            self.result_data_Text1.delete(1.0, END)
            self.result_data_Text1.insert(1.0, ll.get(14, 1))
        elif src == '4':
            ll = pant()
        else:
            self.result_data_Text1.delete(1.0, END)
            self.result_data_Text1.insert(1.0, "请输入数字(登录数据包请按1,定位数据包请按2,报警数据包请按3,心跳数据包请按4")
            self.write_log_to_Text(
                "ERROR:数据包生成 failed,请输入数字(登录数据包请按1,定位数据包请按2,报警数据包请按3,心跳数据包请按4")
            return 0
        self.result_data_Text1.delete(1.0, END)
        self.result_data_Text1.insert(1.0, ll.get(2, 1))
        self.write_log_to_Text("INFO:数据包生成 success")

    # 获取当前时间
    def get_current_time(self):
        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        return current_time

    # 日志动态打印
    def write_log_to_Text(self, logmsg):
        global LOG_LINE_NUM
        current_time = self.get_current_time()
        logmsg_in = str(current_time) + " " + str(logmsg) + "\n"  # 换行
        if LOG_LINE_NUM <= 7:
            self.log_data_Text.insert(END, logmsg_in)
            LOG_LINE_NUM = LOG_LINE_NUM + 1
        else:
            self.log_data_Text.delete(1.0, 2.0)
            self.log_data_Text.insert(END, logmsg_in)

    def send1(self):
        s = socket(AF_INET, SOCK_STREAM)
        src = self.fwq_Text.get().strip()
        src1 = self.fwq_Text1.get().strip()
        print(f"'{src}'")
        print(int(src1))

        s.connect((src, int(src1)))
        t=self.sj_Text.get(0.0,END)
        print(t)
        a=bytes().fromhex(t)
        # s.send(t)
        print('数据发送：{}'.format(s.send(a)))
        data=s.recv(2000)
        self.res_Text.delete(1.0,END)
        self.res_Text.insert(1.0,str(data))
        # print('数据接收：{}'.format(str(data).encode('ISO-8859-1').decode('gbk')))
        print('数据接收：{}'.format(str(data)))
        time.sleep(2)
        s.close()



    # 设置窗口
    def set_init_window(self):
        # v3解析数据
        self.init_window_name.title("V3解析工具_v1.2  作者 : 姚子奇")
        self.init_window_name.geometry('1090x800+10+10')


        self.init_data_label = Label(self.init_window_name,
                                     text="原始数据(无空格，请格式化)\n例子：7878110101234135484845480100320000016D3F0D0A")

        self.init_data_label.grid(row=0, column=0)

        self.result_data_label = Label(self.init_window_name, text="解析结果")
        self.result_data_label.grid(row=0, column=12)
        self.init_data_Text = Text(self.init_window_name, width=67, height=20)  # 原始数据录入框
        self.init_data_Text.grid(row=1, column=0, rowspan=10, columnspan=10,sticky=E)
        # self.init_data_Text.bind("<Button-3>", lambda x: rightKey(x, self.init_data_Text))
        self.result_data_Text = Text(self.init_window_name, width=75, height=20)  # 处理结果展示
        self.result_data_Text.grid(row=1, column=12, rowspan=15, columnspan=10,sticky=N+W)
        # self.result_data_Text.bind("<Button-3>", lambda x: rightKey(x, self.result_data_Text))
        # 按钮
        self.str_trans_to_md5_button = Button(self.init_window_name, text="专用V3解析",width=10,
                                              command=self.xieyihao)  # 调用内部方法  加()为直接调用
        self.str_trans_to_md5_button.grid(row=5, column=11,sticky=W)

        # v3组成数据
        self.sbei_Text_label = Label(self.init_window_name, text="设备号(V3设备号15位)")
        self.sbei_Text_label.grid(row=13, column=0)

        items=("154854744888745","145263966554789")
        self.sbei_Text = Combobox(self.init_window_name, width=64, height=2,values=items)
        self.sbei_Text.grid(row=14, column=0,sticky=N,columnspan=10)


        self.init_data_label1 = Label(self.init_window_name,
                                      text="(登录数据包请按1,定位数据包请按2,报警数据包请按3,心跳数据包请按4)\n注意V3协议除登录包需要更改设备号，其他数据包默认通用")
        self.init_data_label1.grid(row=15, column=0,sticky=N)
        self.init_data_Text1 = Text(self.init_window_name, width=67, height=15)
        self.init_data_Text1.grid(row=16, column=0, rowspan=10, columnspan=10,sticky=N)




        self.result_data_label1 = Label(self.init_window_name, text="输出结果")
        self.result_data_label1.grid(row=13, column=12)

        # self.init_data_Text1.bind("<Button-3>", lambda x: rightKey(x, self.init_data_Text1))
        self.result_data_Text1 = Text(self.init_window_name, width=75, height=20)
        self.result_data_Text1.grid(row=14, column=12, rowspan=10, columnspan=10)
        # self.result_data_Text1.bind("<Button-3>", lambda x: rightKey(x, self.result_data_Text1))

        self.log_label = Label(self.init_window_name, text="日志")
        self.log_label.grid(row=31, column=0)
        self.log_data_Text = Text(self.init_window_name, width=140, height=9)  # 日志框
        self.log_data_Text.grid(row=38, column=0, columnspan=38)
        # self.log_data_Text.bind("<Button-3>", lambda x: rightKey(x, self.log_data_Text))
        # 按钮
        self.str_trans_to_md5_button = Button(self.init_window_name, text="专用V3生成",width=10,
                                              command=self.qo_login)  # 调用内部方法  加()为直接调用
        self.str_trans_to_md5_button.grid(row=16, column=11)





from tkinter.messagebox import *
# def mess():
#     # 创建askyesno()会话框
#     boo=askyesno("真的要走了吗","臣退了，这一退就是一辈子！")
#     if boo==True:
#         init_window.quit()


def gui3_start():
    init_window = Tk()  # 实例化出一个父窗口
    ZMJ_PORTAL = MY_GUI(init_window)
    # init_window.protocol("WM_DELETE_WINDOW", mess)
    # 设置根窗口默认属性
    ZMJ_PORTAL.set_init_window()
    init_window.iconbitmap("favicon.ico")

    init_window.mainloop()

if __name__ == '__main__':
    gui3_start()
