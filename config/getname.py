"""
-*- coding:utf-8 -*-
@Time   :2020/12/15 14:09
@Author :
@File   :jar_jiexi_html.py
@Version：1.0
"""
import json

import requests

if __name__ == '__main__':
    # 仅修改xing、gender即可（此例子表示：姓王的女孩姓名）
    xing = ['yao', '姚']  # 元素1：对应姓的拼音  元素2：姓
    gender = '男'


    # 以下不用修改
    index = 1
    names=[]
    print('【', xing[1], gender, '】')
    for i in range(1):
        if gender == '男':
            result = requests.get(
                'http://{}.resgain.net/name/{}_{}.html'.format(xing[0], 'boys', index))
            result = result.content.decode('utf-8')
            slp = '<meta name="description" content="{}姓{}孩名字大全,{}姓{}孩名,{}姓{}孩取名:'.format(xing[1], gender, xing[1],
                                                                                          gender, xing[1], gender)
            result = result.split(slp)[1]
            result = result.split('">')[0]
            result=json.load(result)
            print(type(result))
            # for i in result:
            #      print(i)
            # names.append(result)

    print(names)

