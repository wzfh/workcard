import os
import uiautomator2 as u2
import time
import io
from PIL import Image
from apscheduler.schedulers.blocking import BlockingScheduler

print("正在连接设备")
device = os.popen("adb devices").readlines()
device_id = device[1]
print(device_id.split()[0])

d = u2.connect_usb(f'{device_id.split()[0]}')
# print(d.info)
print("设备连接成功")
def countdown(t):
    for i in range(t):
        print("\r休眠倒计时：%d" % (t - i) + '秒', end='')
        time.sleep(1)
def click_text(self,str, sq=0):  # 对于无法直接点击的控件写了个函数
    path = d(text=str)[sq]
    x, y = path.center()
    d.click(x, y)
class MY():
    def __init__(self):
        self.file_path=r'C:\Users\rjcsyb2\Desktop\comic-Lee\region.png'

    def 截图(self):
        imge=d.screenshot(format='raw')
        # screen_size = d.window_size()
        # x1, y1, x2, y2 = 699, 1385, 951, 1527
        x1, y1, x2, y2 = 261, 1388, 951, 1527
        io_image = io.BytesIO(imge)
        image = Image.open(io_image)
        region_image = image.crop((x1, y1, x2, y2))
        if os.path.exists(self.file_path):
            os.remove(self.file_path)
            print(f"\n文件 {self.file_path} 已被成功删除.")
        time.sleep(3)
        # imge.save('text.png')
        region_image.save('region.png')
        print('重新截取屏幕')





    def 识别图片(self):
        from PIL import Image
        import pytesseract

        pytesseract.pytesseract.tesseract_cmd = r'C:\Users\rjcsyb2\Desktop\Tesseract-OCR\tesseract.exe'

        file_path = r'C:\Users\rjcsyb2\Desktop\comic-Lee\region.png'
        img = Image.open(file_path)
        config = r'-c tessedit_char_whitelist=0123456789 --psm 6'
        self.count1 = pytesseract.image_to_string(img, config=config)
        self.image_text = pytesseract.image_to_string(Image.open(file_path), lang='chi_sim')
        # 打印结果
        print(f'识别到排行榜第一名：{self.image_text[:8]}')
        print(f'识别到第一名步数：{self.count1}')

    def 步数(self):
        countdown(5)
        if self.image_text[:7] != '姚子奇 (锋)':
            d.press('recent')
            print('\n查看最近浏览过的程序')
            countdown(2)
            d.click(40,1136)
            countdown(10)
            d.click(881,1917)
            print('\n点击跳转')
            countdown(10)
            d.click(40,1136)
            countdown(10)
            d.click(551,727)
            print('\n点击输入框')
            d.clear_text()
            d.set_fastinput_ime(True)
            d.send_keys(f"{int(self.count1)+250}", True)
            print(f'修改步数：{int(self.count1)+250}')
            d.press("back")
            d.click(538,888)
            print('执行')
            countdown(2)
            d.click(547,1750)
            print('\n立即观看')
            countdown(40)
            if d(text='查看详情').exists(timeout=5):
                d(text='查看详情').click()
                print('查看详情')
            if d(text='前往小游戏').exists(timeout=5):
                d(text='前往小游戏').click()
                print('前往小游戏')
            if d(text='进入游戏').exists(timeout=5):
                d(text='进入游戏').click()
                print('进入游戏')
            # elif d(text='已获得奖励').exists(timeout=5):
            #     d.click()
            else:
                d(text='关闭').click(timeout=2)
            countdown(5)
            d.press("back")
            countdown(2)
            d(text='关闭').click(timeout=2)
            d.set_fastinput_ime(False)
        else:
            print(f'\n当前第一名：{self.image_text[:7]}')

    def run(self):
        try:
            d.app_start("com.tencent.mm")
            print('启动微信')
            countdown(5)
            d(text="微信运动").click(timeout=10)
            click_text(d,"微信运动")
            click_text(d,"步数排行榜")
            countdown(5)
            for i in range(10):
                self.截图()
                self.识别图片()
                self.步数()
                countdown(5)
                d.press("back")
                if self.image_text[:7] != '姚子奇 (锋)':
                    d.press('recent')
                    print('\n查看最近浏览过的程序')
                    countdown(2)
                    d.click(40, 1136)
                    d.press("back")
                countdown(500)
                click_text(d, "步数排行榜")
                countdown(5)
        except:
            pass

        # d.app_stop("com.tencent.mm")


if __name__ == '__main__':
    ll=MY()
    # ll.截图()
    ll.run()
    sched = BlockingScheduler()  # 设置定时任务，周一至周五 上午8.50自动打上班卡，下午6.10自动打下班卡

    sched.add_job(ll.run, 'cron', day_of_week='mon-sat', hour='9', minute='00')
    sched.add_job(ll.run, 'cron', day_of_week='mon-sat', hour='10', minute='00')
    sched.add_job(ll.run, 'cron', day_of_week='mon-sat', hour='11', minute='00')
    sched.add_job(ll.run, 'cron', day_of_week='mon-sat', hour='12', minute='00')
    sched.add_job(ll.run, 'cron', day_of_week='mon-sat', hour='13', minute='00')
    sched.add_job(ll.run, 'cron', day_of_week='mon-sat', hour='14', minute='00')
    sched.add_job(ll.run, 'cron', day_of_week='mon-sat', hour='15', minute='00')
    sched.add_job(ll.run, 'cron', day_of_week='mon-sat', hour='16', minute='00')
    sched.add_job(ll.run, 'cron', day_of_week='mon-sat', hour='17', minute='00')
    sched.add_job(ll.run, 'cron', day_of_week='mon-sat', hour='18', minute='00')
    sched.add_job(ll.run, 'cron', day_of_week='mon-sat', hour='19', minute='00')
    sched.add_job(ll.run, 'cron', day_of_week='mon-sat', hour='20', minute='00')
    sched.add_job(ll.run, 'cron', day_of_week='mon-sat', hour='21', minute='00')
    sched.add_job(ll.run, 'cron', day_of_week='mon-sat', hour='22', minute='00')
    sched.add_job(ll.run, 'cron', day_of_week='mon-sat', hour='23', minute='00')
    sched.start()