# -*- coding: utf-8 -*-
# @Time    : 2022-10-01 19:58
# @Author  : KKings
# @File    : sign_lv1.py
# @Software: PyCharm
import binascii

from unicorn import *
from unicorn.arm_const import *


def hook_code(uc, address, size, user_data):
    """ 监听指令执行操作
    uc:
    address     : 当前指令地址
    size        : 指令长度,若长度未知则为0
    user_data   : hook_add 设置时的 user_data 参数
    """
    print(">>> Tracing instruction at 0x%x, instruction size = 0x%x" % (address, size))


def hook_memory(uc, type, address, size, value, user_data):
    """ 监听内存异常操作
    uc:
    type        : 内存操作类型 READ|WRITE
    address     : 当前指令地址
    size        : 操作长度
    value       : 写入值
    user_data   : hook_add 设置时的 user_data 参数
    """
    pc = uc.reg_read(UC_ARM_REG_PC)
    print(">>> memory error: pc%x address:%x size:%x" % (pc, address, size))


a1 = b'123'
mu = Uc(UC_ARCH_ARM, UC_MODE_THUMB)

# image
image_base = 0x0
image_size = 0x10000 * 8
mu.mem_map(image_base, image_size)
so = open('lib/libnative-lib.so', "rb").read()
mu.mem_write(image_base, so)  # 简陋的加载方式

# stack
stack_base = 0xa0000
stack_size = 0x10000 * 3
stack_top = stack_base + stack_size - 4  # Sp
mu.mem_map(stack_base, stack_size)
mu.reg_write(UC_ARM_REG_SP, stack_top)

# data segment
data_base = 0xf0000
data_size = 0x10000 * 3
mu.mem_map(data_base, data_size)
# mu.reg_write(data_base, a1)
mu.reg_write(UC_ARM_REG_R0, data_base)

# set hook
# mu.hook_add(UC_HOOK_CODE, hook_code, 0)
# mu.hook_add(UC_HOOK_MEM_UNMAPPED, hook_code, 0)

# fix got
mu.mem_write(0x1EDB0, b'\xd9\x98\x00\x00')

target = image_base + 0x9b68
target_end = image_base + 0x9C2C  # while 不执行 sprintf

# start
try:
    mu.emu_start(target + 1, target_end)  # 不加1会出异常 Unhandled CPU exception (UC_ERR_EXCEPTION)
    r2 = mu.reg_read(UC_ARM_REG_R2)
    result = mu.mem_read(r2, 16)
    print(binascii.b2a_hex(result)) # b'25e5fa71b765a7302ec27b1745725c38'

except UcError as e:
    print(e)
