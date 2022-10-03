# -*- coding: utf-8 -*-
# @Time    : 2022-10-04 1:31
# @Author  : KKings
# @File    : GenPyByTemplate.py
# @Software: PyCharm
import datetime
import sys
import time
from os.path import dirname, abspath
from string import Template

BASE_PATH = f'{dirname(abspath(__file__))}\\base.txt'
ROOT_PATH = dirname(dirname(abspath(__file__))) + '\\'
print()
if __name__ == '__main__':
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    fileNames = []
    if len(sys.argv) == 1:
        fileNames = [str(time.time_ns())]
    elif len(sys.argv) >= 2:
        fileNames = sys.argv
    else:
        raise f"参数错误 {sys.argv}"

    for fileName in fileNames:
        if fileName == __file__:
            continue
        fileName = fileName + '.py'
        with open(BASE_PATH, 'r', encoding='utf-8') as f:
            tp = Template(f.read())

        with open(ROOT_PATH + fileName, 'w', encoding='utf-8') as f:
            f.write(tp.substitute(
                now=now,
                fileName=fileName,
            ))

        print('%s 文件创建完成' % fileName)
