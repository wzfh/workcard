"""
贴吧信息
"""
# import requests as req
# import html
#
#
# headers = {
#     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
# }
# proxies = {'http': 'http://192.168.10.60:808', 'https': 'http://192.168.10.60:808'}
# # 获取贴吧信息：
# #   排名序号|标题|摘要|热度|链接图片
# def tieba_hot():
#     url='https://jump.bdimg.com/hottopic/browse/topicList'
#     # JSON数据接口
#     resp = req.get(url)
#     data = resp.json()
#     print(data)
#     # topic_list = data['data']['bang_topic']['topic_list']
#     # for topic in topic_list:
#     #     topic_url = html.unescape(topic['topic_url'])
#     #     print('{} |{}|{}\n'.format(topic['idx_num'],topic['topic_name'],topic_url))
#
# if __name__ == '__main__':
#     tieba_hot()
# import datetime
# import json
# import time
#
# import pandas as pd
# import requests
# import xlwt
# from attr import assoc

"""
百度贴吧作者名
"""
# import requests as rq
# from lxml import etree
#
# url='https://tieba.baidu.com/'
# headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36','Referer': 'https://tieba.baidu.com/'}
#
# def get_data(url):
#     response=rq.get(url,headers=headers)
#     response.encoding='utf-8'
#     selector=etree.HTML(response.text)
#     content = selector.xpath('//*[@id="new_list"]/li/div/div[3]/a')
#     print(type(content))
#     print(content)
#     a=[]
#     for line in content:
#         a.append(line.text)
#     print(f'百度贴吧作者：{a}')
#
#
# if __name__ == '__main__':
#     get_data(url)


"""
豆瓣电影名
"""
# import requests
# from bs4 import BeautifulSoup
#
# url='https://movie.douban.com/top250'
# headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}
# data=requests.get(url,headers=headers)
# # print(data)
# soup =BeautifulSoup(data.text,'lxml')
# # print(soup)
# name=soup.select('#content > div > div.article > ol > li > div > div.info > div.hd > a > span:nth-child(1)')
# print(name)


"""
selenium
"""
# from selenium import webdriver
#
# url='https://movie.douban.com/top250?filter=249'
# opts = webdriver.ChromeOptions()
# opts.add_argument('--headless') # 浏览器不提供可视化页面
# opts.add_argument('--no-sandbox') # 解决DevToolsActivePort文件不存在的报错
# opts.add_argument('blink-settings=imagesEnabled=false') # 禁止网页加载图片
#
# browser=webdriver.Chrome(options=opts)
# browser.get(url)
# selector = '#content > div > div.article > ol > li > div > div.info > div.hd > a > span:nth-child(1)'
# movie_names = browser.find_elements_by_css_selector(selector)
# for movie_name in movie_names:
#     print(movie_name.text)


"""
查询豆瓣电影排行榜所有电影
xlwt保存数据
"""
# import xlwt
# import requests
# from bs4 import BeautifulSoup
# time=datetime.datetime.now().strftime('%F')
# urls=['https://movie.douban.com/top250?start={}'.format(str(i)) for i in range(0,250,25)]
# headers={
#      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
# }
# def get_data():
#      book = xlwt.Workbook(encoding='UTF-8')
#      sheet1=book.add_sheet('sheet1',cell_overwrite_ok=True)
#      sheet1.col(0).width=6400
#      n=0
#      for url in urls:
#           data= requests.get(url,headers=headers)
#           soup = BeautifulSoup(data.text,'lxml')
#           titles=soup.select('#content > div > div.article > ol > li > div > div.info > div.hd > a > span:nth-child(1)')
#           m=0
#           for title in titles:
#                print(title.get_text())
#                sheet1.write(m+n, 0 , title.get_text())
#                m=m+1
#           n=n+25
#      book.save('C:\\Users\Administrator\Desktop\{}电影.xls'.format(time))
# if __name__ == '__main__':
#     get_data()

"""
获取京东物品评价
"""
# import requests
# import xlwt
# style = xlwt.XFStyle()
# style.alignment.wrap = 1  # 设置自动换行
# book = xlwt.Workbook(encoding='UTF-8')
# urls = ['https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98&productId=100016672406&score=0&sortType=5&page={}&pageSize=10&isShadowSku=0&rid=0&fold=1'.format(str(n)) for n in range(0, 100)]
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
# }
# sheet1 = book.add_sheet('sheet1', cell_overwrite_ok=True)
# num = 0
# for url in urls:
#     data = requests.get(url, headers=headers).text
#     # soup=BeautifulSoup(data.text,'lxml')
#     content = data.replace('fetchJSON_comment98(', '').replace(');', '')
#     wb = json.loads(content)
#     # print(wb)
#     for c in range(0, 10):
#          # sheet1.write(c + num, 0, wb['comments'][c]['content'], style)
#          # sheet1.col(0).width = 50000
#          print('评论{}：\n'.format(c + num + 1) + wb['comments'][c]['content'])
#     num += 10
#     time.sleep(1)


"""
淘宝评价未完成
"""
# from lxml import etree
# urls=['https://rate.tmall.com/list_detail_rate.htm?itemId=617716089924&spuId=1650289398&sellerId=3446378602&order=3&currentPage=2&append=0&content=1&tagId=&posi=&picture=&groupId=&ua=098%23E1hvkvv9vkIvUvCkvvvvvjiWRLLhsj3vRs5UAjthPmP9gj3RPL5vgji8PLFh0jEh9vhv2nsGxltAzYswj53z7uQCvvyvvaqffvmmP8T%2BvpvEvUmZy2OvvSIsdvhvjIuCJ5DdvvhOMFy3xXcB%2BbWw5jwI1W9OVEkOwhfO3OvCvvswPj1a8rMwzPstxxIgvpvhvvCvpUvCvCLwMHiaYnMwznQ%2FTxSNjSQBzva448QCvvyv9v%2BUk9vvknIgvpvhvvCvpUvCvCLwM8lanaMwznAamDS50PQPzvx4k4QCvvyv9HXx5Qvv3d4VvpvhvUCvp29CvvpvvhCv29hvCvvvMM%2FUvpvVvpCmp%2F2OuvhvmvvvpwnvqpZnKvhv8vvvphvvvvvvvvChRpvv9JpvvhNjvvvmjvvvBGwvvvUUvvCj1Qvvv99UvpCWvpQkU3llDf8r5C61D76fdigXaZmOD464d3ODNrCl5FKzrmphQbmAdXAKNB3r08g7%2Bul08MLUVBy7%2B3%2BuQj7Jd4g7Ecqh18TJ%2BultEvvCvvOv9hCvvvmevpvhvvCCB8QCvvyvvFhs59vv9tOgvpvhvvCvp8QCvvyv9jXlF9vvmDRvvpvZzPAXcJLNznsw5kift%2F2GhaQH7ek%2Bvpvp9QVdumUv9PP4%2BoYC6XZzRuQCvvyv9aSNIQmCrO8%2BvpvEvUjRArOvve%2F89vhv2nQwpl02zYswNhMk7IvCvvswPW1a7nMwzEA%2BODuvvpvWz21McLSNznQJtxt49vhv2nQwlDtBzYswjS2L7IvCvvswjbCa8YMwzCTx8HI%3D&needFold=0&_ksTS=1658136050107_1061&callback=jsonp1062'.format(str(n)) for n in range(0,100)]
# headers={
#      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
# }
# cookies={
# 'cookie': 'yunpk=1421828480512719; sca=ef84daa6; tbsa=1ce1b71a48cfe020e06578ba_1658133471_4; cnaui=2209261399824; aui=2209261399824; cna=hQpcG628+y0CATsnhr4CybGr; cdpid=UUphw2ebpmKph2WACg%253D%253D; atpsida=ac0efa74d100fac616e1bdfe_1658133693_20'
# }
# for url in urls:
#      response=requests.get(url,headers=headers,cookies=cookies)
#      response.encoding='utf-8'
#      selector=etree.HTML(response.text)
#      content=selector.xpath('//*[@id="J_Reviews"]/div/div[6]/table/tbody/tr[6]/td[1]/div/div[1]')
#      print(type(content))
#      print(content)


"""
今日头条
"""
# import requests
# from bs4 import BeautifulSoup
# from lxml import etree
# url='https://www.toutiao.com/'
# headers={
#      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
#      'cookie': '__ac_nonce=062d62444000027d07d68; msToken=z6FX_GIwv084S0Ov9pQ-U3RoMqOR0x4jcTF0Ui1gqlYW72XZI82VET2FY8cD7Fb3VcE_PvN2qvzgEjWDgrjtVvUBiV5wpp3EHUSKeT_TNejp; __ac_signature=_02B4Z6wo00f01MDEAaAAAIDDcDXtaW7b0rjA5AUAAFLsd1; tt_webid=7121919726116980237; ttcid=87baaaa266484dbba17adac225da43f520; local_city_cache=%E6%83%A0%E5%B7%9E; _tea_utm_cache_24=undefined; s_v_web_id=verify_l5rm5rdp_AqUqZKW9_tYAo_4F26_AESC_Q68WWGj201Aw; csrftoken=7c0228233ffa5727edd55908dcb0b82f; ttwid=1%7C3AyHg4d0LEotdu2cPG-j6CsarlbKgeHnZErY8ysa6wY%7C1658201193%7C3d126710e68f4d4e0fd45002d88ce2f38a8edc08e1f50d1bb6bc9a43b159d215; tt_scid=6dYsgrirom4DKiwSo4BBLCMl0JcRCI91T5D1puu3b4oS5.m2pfpzppUHg3QcjHmfc560; MONITOR_WEB_ID=28b0200e-4096-4d26-ba99-a5874a73eb03'
# }
# data=requests.get(url,headers=headers)
# data.encoding='utf-8'
# soup=etree.HTML(data.text)
# selector=soup.xpath('//*[@id="root"]/div/div[5]/div[1]/div/div/div/div[2]/div/div/div/a')
# for line in selector:
#      print(line.text)


"""
热搜
"""
# import requests
# from bs4 import BeautifulSoup
# from lxml import etree
#
# url = 'https://top.baidu.com/board?tab=realtime'
# headers = {
#     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
#     'Cookie': 'BIDUPSID=E9B6BA0755A51C7D711E90194D5F215E; PSTM=1653449092; BAIDUID=ACF8CE8B49C9DD1DF939D1E3D790BE11:FG=1; BDUSS=EN5ZUhkQVN0MlJPVmhHZ0pJbDZxaDdTV3luMXZFNG1FSGF5VHl6Y3VlQjZUNzFpSVFBQUFBJCQAAAAAAAAAAAEAAADcQZby1~nA17TvNjUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHrClWJ6wpVid; BDUSS_BFESS=EN5ZUhkQVN0MlJPVmhHZ0pJbDZxaDdTV3luMXZFNG1FSGF5VHl6Y3VlQjZUNzFpSVFBQUFBJCQAAAAAAAAAAAEAAADcQZby1~nA17TvNjUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHrClWJ6wpVid; MCITY=-301%3A; delPer=0; ZFY=DcI7o4buT2FkPg23I4aIwFUHpPW:AFsVCtPGhJ9xxlEs:C; BAIDUID_BFESS=57D5324FD703891C779C74749C9F81BE:FG=1; H_PS_PSSID=26350; BDORZ=FFFB88E999055A3F8A630C64834BD6D0; BDRCVFR[D2FIJh4TnDm]=mk3SLVN4HKm; ZD_ENTRY=baidu; BCLID=8620944682005354376; BDSFRCVID=PyuOJexroG06rjvDcCWjJ6WvgeKKvV3TDYLEOwXPsp3LGJLVcKvVEG0Pt8lgCZu-2ZlgogKK3gOTHxtF_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF=tbkD_C-MfIvDqTrP-trf5DCShUFsWbbiB2Q-XPoO3Kt-MR3_Q-bUMtPpjRJqK-QiWbRM2MbgylRp8P3y0bb2DUA1y4vpKbjP0eTxoUJ2XMKVDq5mqfCWMR-ebPRiJ-b9QgbOLpQ7tt5W8ncFbT7l5hKpbt-q0x-jLTnhVn0MBCK0hI0ljj82e5PVKgTa54cbb4o2WbCQ3Ibz8pcN2b5oQTOBjxJZ0PJRyDbZ_f3K5b5vOIJTXpOUWfAkXpJvQnJjt2JxaqRC5-olEl5jDh3MBpQDhtoJexIO2jvy0hvctb3cShn95MjrDRLbXU6BK5vPbNcZ0l8K3l02V-bIe-t2XjQhDG0qtTkjJbusQJ5e24oqHP-kKPrV-4oH5MQy5toyHD7yWCkEbT6cOR5Jj65KX-_Y0HJR5-IH2gLq--Qj5xJvJDT43MA--t40BUQq5xDDMjRehlcuLhQjsq0x0MRYe-bQypoaBtrh-IOMahkb5h7xO-nmQlPK5JkgMx6MqpQJQeQ-5KQN3KJmfbL9bT3YjjTyjaAfq6LetR3H0RbV-J5jf5rRMtcD-DC3-fna544XKKOLVhOMtp7keq8CD4c40PIXDPO2ajjrWJcULJ3bMD51fKO2y5jHhP04yJ6qapTtWaRaL-optP5psIJMXq_WbT8ULtcg0pOJaKviaKOjBMb1J-bDBT5h2M4qMxtOLR3pWDTm_q5TtUJMeCnTD-Dhe65WeaDHt6tsKjAX3JjV5PK_Hn7zep3B5f4pbq7H2M-jJjrBLqbJ0M38OCQ554JqyUPB3Gbn0pcr3mOfhUJb-IOdspcs34bv5lKkQN3T-TvQ527zL6C-yJRJDn3oyTbJXp0n2hOly5jtMgOBBJ0yQ4b4OR5JjxonDh83bG7MJUutfD7H3KC2JI0MhU5; BCLID_BFESS=8620944682005354376; BDSFRCVID_BFESS=PyuOJexroG06rjvDcCWjJ6WvgeKKvV3TDYLEOwXPsp3LGJLVcKvVEG0Pt8lgCZu-2ZlgogKK3gOTHxtF_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF_BFESS=tbkD_C-MfIvDqTrP-trf5DCShUFsWbbiB2Q-XPoO3Kt-MR3_Q-bUMtPpjRJqK-QiWbRM2MbgylRp8P3y0bb2DUA1y4vpKbjP0eTxoUJ2XMKVDq5mqfCWMR-ebPRiJ-b9QgbOLpQ7tt5W8ncFbT7l5hKpbt-q0x-jLTnhVn0MBCK0hI0ljj82e5PVKgTa54cbb4o2WbCQ3Ibz8pcN2b5oQTOBjxJZ0PJRyDbZ_f3K5b5vOIJTXpOUWfAkXpJvQnJjt2JxaqRC5-olEl5jDh3MBpQDhtoJexIO2jvy0hvctb3cShn95MjrDRLbXU6BK5vPbNcZ0l8K3l02V-bIe-t2XjQhDG0qtTkjJbusQJ5e24oqHP-kKPrV-4oH5MQy5toyHD7yWCkEbT6cOR5Jj65KX-_Y0HJR5-IH2gLq--Qj5xJvJDT43MA--t40BUQq5xDDMjRehlcuLhQjsq0x0MRYe-bQypoaBtrh-IOMahkb5h7xO-nmQlPK5JkgMx6MqpQJQeQ-5KQN3KJmfbL9bT3YjjTyjaAfq6LetR3H0RbV-J5jf5rRMtcD-DC3-fna544XKKOLVhOMtp7keq8CD4c40PIXDPO2ajjrWJcULJ3bMD51fKO2y5jHhP04yJ6qapTtWaRaL-optP5psIJMXq_WbT8ULtcg0pOJaKviaKOjBMb1J-bDBT5h2M4qMxtOLR3pWDTm_q5TtUJMeCnTD-Dhe65WeaDHt6tsKjAX3JjV5PK_Hn7zep3B5f4pbq7H2M-jJjrBLqbJ0M38OCQ554JqyUPB3Gbn0pcr3mOfhUJb-IOdspcs34bv5lKkQN3T-TvQ527zL6C-yJRJDn3oyTbJXp0n2hOly5jtMgOBBJ0yQ4b4OR5JjxonDh83bG7MJUutfD7H3KC2JI0MhU5; BA_HECTOR=21210ka40h05a0802k06ekts1hdc92317; PSINO=6'
# }
# data = requests.get(url, headers=headers)
# data.encoding = 'utf-8'
# soup = BeautifulSoup(data.text, 'lxml')
# selector = soup.select('#sanRoot > main > div.container.right-container_2EFJr > div > div:nth-child(2) > div > div.content_1YWBm > a > div.c-single-text-ellipsis')
# soup1 = etree.HTML(data.text)
# selector1 = soup1.xpath('//*[@id="sanRoot"]/main/div[2]/div/div[2]/div/div[2]/div[1]/text()')
# # print(selector1)
# n = 0
# for line in selector:
#     m = n + 1
#     print(f'热搜：{m}')
#     print(line.text)
#     n += 1
#     # print(selector1[n])
#     # if selector1[n] == ' ':
#     #     continue


"""
热搜标题内容地址
"""
# import requests
# url='https://top.baidu.com/api/board?platform=wise&tab=realtime'
# headers={
#     'Cookie': 'BIDUPSID=E9B6BA0755A51C7D711E90194D5F215E; PSTM=1653449092; BAIDUID=ACF8CE8B49C9DD1DF939D1E3D790BE11:FG=1; BDUSS=EN5ZUhkQVN0MlJPVmhHZ0pJbDZxaDdTV3luMXZFNG1FSGF5VHl6Y3VlQjZUNzFpSVFBQUFBJCQAAAAAAAAAAAEAAADcQZby1~nA17TvNjUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHrClWJ6wpVid; BDUSS_BFESS=EN5ZUhkQVN0MlJPVmhHZ0pJbDZxaDdTV3luMXZFNG1FSGF5VHl6Y3VlQjZUNzFpSVFBQUFBJCQAAAAAAAAAAAEAAADcQZby1~nA17TvNjUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHrClWJ6wpVid; delPer=0; ZFY=DcI7o4buT2FkPg23I4aIwFUHpPW:AFsVCtPGhJ9xxlEs:C; BAIDUID_BFESS=57D5324FD703891C779C74749C9F81BE:FG=1; BDRCVFR[D2FIJh4TnDm]=mk3SLVN4HKm; ZD_ENTRY=baidu; BCLID=8620944682005354376; BDSFRCVID=PyuOJexroG06rjvDcCWjJ6WvgeKKvV3TDYLEOwXPsp3LGJLVcKvVEG0Pt8lgCZu-2ZlgogKK3gOTHxtF_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF=tbkD_C-MfIvDqTrP-trf5DCShUFsWbbiB2Q-XPoO3Kt-MR3_Q-bUMtPpjRJqK-QiWbRM2MbgylRp8P3y0bb2DUA1y4vpKbjP0eTxoUJ2XMKVDq5mqfCWMR-ebPRiJ-b9QgbOLpQ7tt5W8ncFbT7l5hKpbt-q0x-jLTnhVn0MBCK0hI0ljj82e5PVKgTa54cbb4o2WbCQ3Ibz8pcN2b5oQTOBjxJZ0PJRyDbZ_f3K5b5vOIJTXpOUWfAkXpJvQnJjt2JxaqRC5-olEl5jDh3MBpQDhtoJexIO2jvy0hvctb3cShn95MjrDRLbXU6BK5vPbNcZ0l8K3l02V-bIe-t2XjQhDG0qtTkjJbusQJ5e24oqHP-kKPrV-4oH5MQy5toyHD7yWCkEbT6cOR5Jj65KX-_Y0HJR5-IH2gLq--Qj5xJvJDT43MA--t40BUQq5xDDMjRehlcuLhQjsq0x0MRYe-bQypoaBtrh-IOMahkb5h7xO-nmQlPK5JkgMx6MqpQJQeQ-5KQN3KJmfbL9bT3YjjTyjaAfq6LetR3H0RbV-J5jf5rRMtcD-DC3-fna544XKKOLVhOMtp7keq8CD4c40PIXDPO2ajjrWJcULJ3bMD51fKO2y5jHhP04yJ6qapTtWaRaL-optP5psIJMXq_WbT8ULtcg0pOJaKviaKOjBMb1J-bDBT5h2M4qMxtOLR3pWDTm_q5TtUJMeCnTD-Dhe65WeaDHt6tsKjAX3JjV5PK_Hn7zep3B5f4pbq7H2M-jJjrBLqbJ0M38OCQ554JqyUPB3Gbn0pcr3mOfhUJb-IOdspcs34bv5lKkQN3T-TvQ527zL6C-yJRJDn3oyTbJXp0n2hOly5jtMgOBBJ0yQ4b4OR5JjxonDh83bG7MJUutfD7H3KC2JI0MhU5; BCLID_BFESS=8620944682005354376; BDSFRCVID_BFESS=PyuOJexroG06rjvDcCWjJ6WvgeKKvV3TDYLEOwXPsp3LGJLVcKvVEG0Pt8lgCZu-2ZlgogKK3gOTHxtF_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF_BFESS=tbkD_C-MfIvDqTrP-trf5DCShUFsWbbiB2Q-XPoO3Kt-MR3_Q-bUMtPpjRJqK-QiWbRM2MbgylRp8P3y0bb2DUA1y4vpKbjP0eTxoUJ2XMKVDq5mqfCWMR-ebPRiJ-b9QgbOLpQ7tt5W8ncFbT7l5hKpbt-q0x-jLTnhVn0MBCK0hI0ljj82e5PVKgTa54cbb4o2WbCQ3Ibz8pcN2b5oQTOBjxJZ0PJRyDbZ_f3K5b5vOIJTXpOUWfAkXpJvQnJjt2JxaqRC5-olEl5jDh3MBpQDhtoJexIO2jvy0hvctb3cShn95MjrDRLbXU6BK5vPbNcZ0l8K3l02V-bIe-t2XjQhDG0qtTkjJbusQJ5e24oqHP-kKPrV-4oH5MQy5toyHD7yWCkEbT6cOR5Jj65KX-_Y0HJR5-IH2gLq--Qj5xJvJDT43MA--t40BUQq5xDDMjRehlcuLhQjsq0x0MRYe-bQypoaBtrh-IOMahkb5h7xO-nmQlPK5JkgMx6MqpQJQeQ-5KQN3KJmfbL9bT3YjjTyjaAfq6LetR3H0RbV-J5jf5rRMtcD-DC3-fna544XKKOLVhOMtp7keq8CD4c40PIXDPO2ajjrWJcULJ3bMD51fKO2y5jHhP04yJ6qapTtWaRaL-optP5psIJMXq_WbT8ULtcg0pOJaKviaKOjBMb1J-bDBT5h2M4qMxtOLR3pWDTm_q5TtUJMeCnTD-Dhe65WeaDHt6tsKjAX3JjV5PK_Hn7zep3B5f4pbq7H2M-jJjrBLqbJ0M38OCQ554JqyUPB3Gbn0pcr3mOfhUJb-IOdspcs34bv5lKkQN3T-TvQ527zL6C-yJRJDn3oyTbJXp0n2hOly5jtMgOBBJ0yQ4b4OR5JjxonDh83bG7MJUutfD7H3KC2JI0MhU5; BA_HECTOR=21210ka40h05a0802k06ekts1hdc92317; PSINO=6; BDRCVFR[dG2JNJb_ajR]=mk3SLVN4HKm; BDRCVFR[-pGxjrCMryR]=mk3SLVN4HKm; H_PS_PSSID=26350; BDORZ=FFFB88E999055A3F8A630C64834BD6D0; MCITY=-%3A; ab_sr=1.0.1_NmIyYTcyYjhhOTJkYzRiMTZmNTUzOGU3ZDliYTc2YWU4YzBlOGI0NmFjZjdjNmYwOWVkZjAxZTI4MThjNzZjMTA4MzMyZjFlNTBhOWFlNDEzN2I4YjRiYmQxMWYyMTI4ODFhOGYxMWU4ZTU2NDExYzlmNzU2YmM3MTAyYmIxMjQ3MTRhNWY1ZjRmMTA4ZmNmYjQ2OWQ1ZDFkZGQ0OGE0Zg==',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
# }
# web=requests.get(url,headers=headers)
# b=web.json()['data']['cards'][0]['content']
# a=web.json()['data']['cards'][0]['content'][0]
# for a in b:
#     print('标题：'+a.get('word'))
#     print('内容：'+a.get('desc'))
#     print('地址：'+a.get('url'))
#     print('\n')

"""
网址二维码生成
"""
# import  pyqrcode
# code=pyqrcode.create(content='https://www.zhihu.com/people/13273183132')
# code.show()


"""
爱奇艺风云榜
"""
# from lxpy import copy_headers_dict
# import requests
# import pandas
#
# urls = ['https://pcw-api.iqiyi.com/strategy/pcw/data/topRanksData?page_st=0&tag=0&category_id=2&date=&pg_num={}'.format(str(n)) for n in range(1, 5)]
# headers = {
#     'cookie': 'T00404=425bdf17f50784457876671f72fcb19c; QC005=fe42024ae15adc66a628d7976523f892; QC008=1658308391.1658308391.1658308391.1; QC175=%7B%22upd%22%3Atrue%2C%22ct%22%3A%22%22%7D; QC006=k424dy5eq5wyma7uaep668tu; QP0013=; QP0030=1; TQC030=1; nu=0; QC173=0; QC007=DIRECT; P00004=.1658309144.f43a063b7e; IMS=IggQABj_zOCWBiouCiBkM2JkZTk3Nzc5YTlmNmE5MzAyZGEwNDRjMWM2ZThkNRAAIggI0AUQAhiwCXIkCiBkM2JkZTk3Nzc5YTlmNmE5MzAyZGEwNDRjMWM2ZThkNRAAggEAigEkCiIKIGQzYmRlOTc3NzlhOWY2YTkzMDJkYTA0NGMxYzZlOGQ1; QC010=63996715; __dfp=a1669ba939e54a4a0290d77a96ca2abf4e116ce04b0b08b12e4ba02f70ba594eb5@1659604393577@1658308394577',
#     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
# }
# for url in urls:
#     web = requests.get(url, headers=headers)
#     web.encoding = 'utf-8'
#     content_list = web.json()['data']['formatData']['data']['content']
#     # print(titles)
#     title_list=[]
#     desc_list=[]
#
#     for content in content_list:
#         # print(content)
#         try:
#             title_list.append(content['title'])
#             desc_list.append(content['desc'])
#
#             # print("电影名：" + name)
#             # print('简介：' + desc)
#         except KeyError:
#             # print('\n')
#             continue
#         print(title_list)
#         # time.sleep(1)
#         # print('\n')
#
#     # print(desc_list)
#     # df=pandas.DataFrame({
#     #     '电影名称':title_list,
#     #     '简介':desc_list
#     # })
#     # df.to_excel('C:\\Users\Administrator\Desktop\风云榜.xlsx')

# import requests  # 发送请求
# import pandas as pd  # 存入excel文件
# from time import sleep  # 随机等待，防止反爬
# import random  # 设置随机
#
# headers = {
#     'accept': 'application/json, text/plain, */*',
#     'accept-encoding': 'gzip, deflate, br',
#     'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
#     'origin': 'https://www.iqiyi.com',
#     'referer': 'https://www.iqiyi.com/',
#     'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
#     'sec-ch-ua-mobile': '?1',
#     'sec-ch-ua-platform': '"Android"',
#     'sec-fetch-dest': 'empty',
#     'sec-fetch-mode': 'cors',
#     'sec-fetch-site': 'same-site',
#     'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Mobile Safari/537.36'
# }
# urls = ['https://pcw-api.iqiyi.com/strategy/pcw/data/topRanksData?page_st=0&tag=0&category_id=2&date=&pg_num={}'.format(str(n)) for n in range(0,5)]
# for url in urls:
#     r = requests.get(url, headers=headers)
#     json_data = r.json()
#     content_list = json_data['data']['formatData']['data']['content']
#     title_list=[]
# #     desc_list=[]
# #     order_list=[]
# #     order=0
#     for content in content_list:
# #         # 排名
# #         order_list.append(order)
# #         # 标题
#         title_list.append(content['title'])
# #         print(order, ' ', content['title'])
# #         # 描述
# #         try:
# #             desc_list.append(content['desc'])
# #         except:
# #             desc_list.append('')
# #
#         df = pd.DataFrame({
#             # '排名': order_list,
#             '标题': title_list,
#             # '描述': desc_list,
#         })
# #         order += 1
#         print(df)
# # # 最后，依然采用我最顺手的方法，拼装成DataFrame的格式，保存到excel文件：
# #         df.to_excel('C:\\Users\Administrator\Desktop\风云榜.xlsx',index=False)

# -*- coding: utf-8 -*-
# from bs4 import BeautifulSoup
# # while True:
# url='http://finance.sina.com.cn/stock/sl/'
# headers={
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
#     'cookie': 'U_TRS1=00000094.d3026df5.6298770f.b75f6950; UOR=link.csdn.net,blog.sina.com.cn,; SINAGLOBAL=183.30.204.148_1654159121.137919; Qs_lvt_335601=1659012088%2C1659697996; Qs_pv_335601=4206382070995344400%2C2937551251622556000; Apache=183.30.204.138_1660209498.435153; U_TRS2=0000008a.9e962c474.62f4c95b.fba2c125; rotatecount=1; ULV=1660216306880:2:1:1:183.30.204.138_1660209498.435153:1654159121564'
# }
# data=requests.get(url=url,headers=headers)
# data.encoding='gbk'
# soup =BeautifulSoup(data.text,'lxml')
# print(soup)

# importing required module
from playsound import playsound
from tkinter import*

# playsound(r'.\空投KT - 给妈妈.mp3')


import tkinter as tk
import pygame
import threading
def play_audio(filename):
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    # while True:
    pygame.mixer.music.play(3)
    if not pygame.mixer.music.get_busy():  # 检查音频是否仍在播放
        print('停止')
def thread_it(self, func, *args):
    """ 将函数打包进线程 """
    self.myThread = threading.Thread(target=func, args=args)
    self.myThread.setDaemon(True)  # 主线程退出就直接让子线程跟随退出,不论是否运行完成。
    self.myThread.start()

def main():
    pygame.init()
    pygame.mixer.init()
    root = tk.Tk()
    root.title("MP3 Player")
    play_audio(r'空投KT - 给妈妈.mp3')
    root.geometry("400x100")
    root.mainloop()

if __name__ == "__main__":
        main()







