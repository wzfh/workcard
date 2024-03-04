#报警标志
from tkinter import END
from tkinter.ttk import Notebook, Frame
from 出租车.V905ku import 报警标志,车辆状态,经纬度,速度,签退方式,报警标志1,车辆状态1,经纬度1,速度1,评价选项,电召订单ID,交易类型
import tkinter as tk
import ttkbootstrap as ttk
init_window = ttk.Window()

class MY_GUI(tk.Tk):

    def __init__(self, init_window_name):
        self.init_window_name = init_window_name


    def set_init_window(self):
        data = '7E0B0500731013560000000001000000000000030000D2AEC7041BF93200C80123120714340600000000000003000127FDF20416D17500C8012312071434063590AA283590AA2801000000000200534E31323535534E3132333435363738393100000000534E31323334353637383931323334353637392312071404143400001000350000200200000120000000010101040000006E0202044C250400000000300103E47E'
        # 905解析数据
        self.init_window_name.title("协议整合工具_v4  作者 : 姚子奇")
        self.init_window_name.geometry('1100x923+450+200')

        note = Notebook(self.init_window_name)
        pane1 = Frame()


        self.result_data_label1 = ttk.Label(pane1, text="输出结果")
        self.result_data_label1.grid(row=0, column=1)

        self.result_data_Text1 = ttk.Text(pane1, width=85, height=120, relief='solid')
        self.result_data_Text1.delete(1.0,END)
        self.result_data_Text1.insert(1.0,
                                      f'营运数据包:{data[2:6]}\n设备号：{data[10:22]}'
                                      f'\n空转重时车位置信息：\n      {报警标志(data)},\n      {车辆状态(data)},\n      {经纬度(data)}'
                                      f'\n      {速度(data)}\n      方向：{data[62:64]}'
                                      f'\n      时间：20{data[64:76][:2]}年{data[64:76][2:4]}月{data[64:76][4:6]}日 {data[64:76][6:8]}时{data[64:76][8:10]}分{data[64:76][10:12]}秒'
                                      
                                      f'\n\n重转空时车位置信息：\n      {报警标志1(data)},\n      {车辆状态1(data)},\n      {经纬度1(data)}'
                                      f'\n      {速度1(data)}\n      方向：{data[112:114]}'
                                      f'\n      时间：20{data[114:126][:2]}年{data[114:126][2:4]}月{data[114:126][4:6]}日 {data[114:126][6:8]}时{data[114:126][8:10]}分{data[114:126][10:12]}秒'
                                      f'\n      营运ID：{data[126:134]}   评价ID：{data[134:142]}  评价选项：{评价选项(data)}'
                                      f'\n      评价选项扩展：{data[144:148]}\n      电召订单ID：{电召订单ID(data)}'
                                      f'\n      车牌号：{data[156:168]}'
                                      f'\n企业经营许可证号：{data[168:200]}'
                                      f'\n驾驶员从业资格证号：{data[200:238]}'
                                      f'\n上车时间：20{data[238:248][:2]}年{data[238:248][2:4]}月{data[238:248][4:6]}日 {data[238:248][6:8]}时{data[238:248][8:10]}分'
                                      f'\n下车时间：{data[248:252][:2]}时{data[248:252][2:4]}分'
                                      f'\n计程公里数：{int(data[252:258])*0.1}  空驶里程：{int(data[258:262])*0.1}  附加费：{int(data[262:268])*0.1}'
                                      f'\n等待计时时间：{data[268:272][:2]}时{data[268:272][2:4]}分   交易金额：{int(data[272:278])*0.1}  当前车次：{bin(int(data[278:286],16))[2:]}'
                                      f'\n交易类型：{交易类型(data)}'
                                      f'\n附加：{data[288:-4]}')

        self.result_data_Text1.grid(row=1, column=1)
        note.add(pane1, text='V3协议解析生成')
        note.grid()
    def str_trans_to_md6(self):
        src = self.init_data1_Text6.get(1.0, END).strip()
        return src

    def 解析905(self):
        data = self.str_trans_to_md6()
        if data[2:6] == '0200':
            self.result_data_Text1.insert(1.0,
                                           f'位置数据包:{data[2:6]}\n设备号：{data[10:22]}\n{报警标志(data)},\n{车辆状态(data)},\n      {经纬度(data)}'
                                           f'\n      {速度(data)},\n      方向：{data[62:64]}'
                                           f'\n      时间：20{data[64:76][:2]}年{data[64:76][2:4]}月{data[64:76][4:6]}日 {data[64:76][6:8]}时{data[64:76][8:10]}分{data[64:76][10:12]}秒'
                                           f'\n      附加信息（未解）{data[76:-4]}')
        elif data[2:6] == '0B03':
            self.result_data_Text1.insert(1.0,
                                          f'签到数据包:{data[2:6]}\n设备号：{data[10:22]}\n{报警标志(data)},\n{车辆状态(data)},\n      {经纬度(data)}'
                                          f'\n      {速度(data)},\n      方向：{data[62:64]}'
                                          f'\n      时间：20{data[64:76][:2]}年{data[64:76][2:4]}月{data[64:76][4:6]}日 {data[64:76][6:8]}时{data[64:76][8:10]}分{data[64:76][10:12]}秒'
                                          f'\n      企业经营许可证号：{data[76:108]}\n   驾驶员从业资格证号：{data[108:146]}'
                                          f'\n      车牌号：{data[146:158]}'
                                          f'\n    开机时间：{data[158:170][:4]}年{data[158:170][4:6]}月{data[158:170][6:8]}日 {data[158:170][8:10]}时{data[158:170][10:12]}分'
                                          f'\n      附加信息（未解）{data[170:-4]}')
        elif data[2:6] == '0B04':
            self.result_data_Text1.insert(1.0,
                                          f'签退数据包:{data[2:6]}\n设备号：{data[10:22]}\n{报警标志(data)},\n{车辆状态(data)},\n      {经纬度(data)}'
                                          f'\n      {速度(data)},\n      方向：{data[62:64]}'
                                          f'\n      时间：20{data[64:76][:2]}年{data[64:76][2:4]}月{data[64:76][4:6]}日 {data[64:76][6:8]}时{data[64:76][8:10]}分{data[64:76][10:12]}秒'
                                          f'\n      企业经营许可证号：{data[76:108]}\n   驾驶员从业资格证号：{data[108:146]}'
                                          f'\n      车牌号：{data[146:158]}'
                                          f'\n      计价器K值：{int(str("0012"))}')
        else:
            self.result_data1_Text6.delete(1.0, END)
            self.result_data1_Text6.insert(1.0, "请输入905原始数据")
            return 0

        # self.result_data_Text.insert(1.0,data1)

        # self.write_log_to_Text5("INFO:原始数据解析 success")










if __name__ == '__main__':
    data='7E0B0300431013560000000001000000000000030000D2AEC70416D17500C800231207160631534E3132333435363738390000000000534E3132333435363738393132333435363739534E3132343520231207160601040000006E0202044C250400000000300103EE7E'
    print(len(data))
    data1='7E0B0300431013560000000001000000000000030000D2AEC70416D17500C800231207160731534E3132333435363738390000000000534E3132343520231207160701040000006E0202044C250400000000300103CB7E'
    print(len(data1))

    data2='7E0B0400431013560000000001000000000000030000D2AEC70416D17500C800231207161051534E3132333435363738390000000000534E3132333435363738393132333435363739534E313234350012202312071610202312071610000120000120001216072100012000012000120120000001200000012012000000001A0101040000006E0202044C250400000000300103937E'
    print(len(data2))
    data3='7E0B0400431013560000000001000000000000030000D2AEC70416D17500C800231207160952534E3132333435363738390000000000534E313234350012202312071609202312071609000120000120001216072100012000012000120120000001200000012012000000001A0101040000006E0202044C250400000000300103AC7E'
    print(len(data3))

    a='0000001B'
    print(int(bin(int(a, 16))[2:],2))
    # print(data[64:76])
    # a2= bin(int(data[34:42], 16))[2:].zfill(32)
    # print(a2)
    # print(a2[-1:])

    # ZMJ_PORTAL = MY_GUI(init_window)
    #
    # ZMJ_PORTAL.set_init_window()
    # init_window.mainloop()

