# -*- coding: utf-8 -*-
# @Time    : 2022-09-30 19:21
# @Author  : KKings
# @File    : capstone-hello.py
# @Software: PyCharm

from capstone import *

CODE = b"\xf1\x02\x03\x0e\x00\x00\xa0\xe3\x02\x30\xc1\xe7\x00\x00\x53\xe3"

md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
for i in md.disasm(CODE, 0x1000):
    print("%x:\t%s\t%s" % (i.address, i.mnemonic, i.op_str))
