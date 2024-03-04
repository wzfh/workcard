import os

import uiautomator2 as u2
import time

from PIL import Image


def countdown(t):
    for i in range(t):
        print("\r休眠倒计时：%d" % (t - i) + '秒', end='')
        time.sleep(1)


from apscheduler.schedulers.blocking import BlockingScheduler

print("正在连接设备")
device = os.popen("adb devices").readlines()
device_id = device[1]
print(device_id.split()[0])


def click_text(self, str, sq=0):  # 对于无法直接点击的控件写了个函数
    path = d(text=str)[sq]
    x, y = path.center()
    d.click(x, y)


def click(text1):
    # d.app_stop_all()
    d.app_stop("com.tencent.mm")
    d.app_stop("com.tencent.wework")
    countdown(5)
    d.app_start("com.tencent.wework")  # 启动应用
    print("\n企业微信应用启动成功")
    d(text="工作台").click()
    print('找到工作台')
    countdown(2)
    d.swipe(930, 1480, 980, 480)
    click_text(d, '打卡')
    print('\n找到打卡页面')
    # d(scrollable=True).scroll.to(text='17:30下班打卡')
    print('等待打卡')
    countdown(90)
    if d(text="今日打卡已完成，好好休息").exists(timeout=2):
        print('\n今日打卡已完成，好好休息')
    elif d(text="下班·正常").exists(timeout=2):
        print('\n下班·正常')
    elif d(text="上班·正常").exists(timeout=2):
        print('\n上班·正常')
    elif d(text="上班自动打卡·正常").exists(timeout=2):
        print('\n上班自动打卡·正常')
    elif d(text="下班自动打卡·正常").exists(timeout=2):
        print('\n下班自动打卡·正常')
    else:
        d(text=text1).click(timeout=10)
    countdown(5)


def send_info():  # 将打卡信息截图利用小号发送给自己大号
    d.app_start("com.tencent.mm")  # 启动应用
    print("\n微信应用启动成功")
    countdown(3)
    click_text(d, "鱼溪")
    print('\n选择发送人')
    countdown(3)
    d.click(0.338, 0.953)
    time.sleep(2)
    d.click(0.289, 0.815)
    time.sleep(1)
    d.click(0.105, 0.817)
    time.sleep(1)
    d.click(0.787, 0.815)
    time.sleep(1)
    d.click(0.286, 0.686)
    time.sleep(1)
    d.click(0.927, 0.943)
    print('\n已发送打卡短信')


def lya():
    d.app_start("no.nordicsemi.android.mcp")  # 启动应用
    print("应用启动成功")
    # size = d.window_size()
    # print(size)
    # x1 = int(size[0] * 0.5)
    # y1 = int(size[1] * 0.9)
    # y2 = int(size[1] * 0.15)

    while True:
        # d.swipe(x1, y1, x1, y2)
        # d(scrollable=True).scroll.toEnd()
        d(scrollable=True).scroll.to(text='MJ01_BLE_1260')
        # if d(text="MJ01_BLE_1260"):
        time.sleep(2)
        d(text="MJ01_BLE_1260").click()
        time.sleep(7)
        d(text="CLONE").click()
        d(text="OK").click()
        break
    time.sleep(7)
    click_text(d, "ADVERTISER")
    time.sleep(1)
    d.click(0.881, 0.211)
    time.sleep(2)
    d(text="OK").click()
    time.sleep(2)
    # d.app_stop("no.nordicsemi.android.mcp")
    # d.app_clear("no.nordicsemi.android.mcp")


def job1():
    for i in range(3):
        try:
            print('打开蓝牙')
            os.system('adb shell svc bluetooth enable')
            print('打开定位')
            os.system('adb shell settings put secure location_mode 1')
            print(f'循环次数：{i + 1}')
            click("上班打卡")
            print('\n已打上班卡')
            countdown(5)
            send_info()
            # d.app_stop_all()
            d.app_stop("com.tencent.mm")
            d.app_stop("com.tencent.wework")
            print('关闭蓝牙')
            os.system('adb shell svc bluetooth disable')
            print('关闭定位')
            os.system('adb shell settings put secure location_mode 0')
            break
        except:
            continue


def job2():
    import os
    for i in range(3):
        try:
            print('打开蓝牙')
            os.system('adb shell svc bluetooth enable')
            print('打开定位')
            os.system('adb shell settings put secure location_mode 1')
            print(f'循环次数：{i + 1}')
            click("下班打卡")
            print('\n已打下班卡')
            countdown(5)
            send_info()
            # d.app_stop_all()
            d.app_stop("com.tencent.mm")
            d.app_stop("com.tencent.wework")
            print('关闭蓝牙')
            os.system('adb shell svc bluetooth disable')
            print('关闭定位')
            os.system('adb shell settings put secure location_mode 0')
            break
        except:
            continue


if __name__ == "__main__":
    d = u2.connect_usb(f'{device_id.split()[0]}')
    # print(d.info)
    print("设备连接成功")
    # job2()
    sched = BlockingScheduler()  # 设置定时任务，周一至周五 上午8.50自动打上班卡，下午6.10自动打下班卡
    sched.add_job(job1, 'cron', day_of_week='mon-sat', hour='09', minute='06')
    # sched.add_job(job1, 'cron', day_of_week='mon-fri', hour='08', minute='55')
    # sched.add_job(job2, 'cron', day_of_week='sat', hour='12', minute='00')
    # sched.add_job(job2, 'cron', day_of_week='mon-fri', hour='19', minute='29')
    sched.add_job(job2, 'cron', day_of_week='mon-fri', hour='17', minute='30')
    sched.start()
