# -*- coding: utf-8 -*-
# @Time    : 2022-10-03 12:41
# @Author  : KKings
# @File    : lv3.py
# @Software: PyCharm

import logging
import posixpath
import sys
from androidemu.emulator import Emulator
from androidemu.java.helpers.native_method import native_method
from androidemu.utils import memory_helpers
from unicorn import UcError
from androidemu.java.java_class_def import JavaClassDef
from androidemu.java.java_method_def import JavaMethodDef, java_method_def
from tools import udbg

logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)7s %(name)34s |%(message)s")
logger = logging.getLogger(__name__)


@native_method
def __aeabi_memclr(mu, address, size):
    print('__aeabi_memclr(%x,%d)' % (address, size))


@native_method
def __aeabi_memcpy(mu, copy_str, soure_str, size):
    print('__aeabi_memcpy(%x,%x,%d)' % (copy_str, soure_str, size))


# Java类
class com_sec_udemo_MainActivity(metaclass=JavaClassDef, jvm_name="com/sec/udemo/MainActivity"):
    def __init__(self):
        pass

    @java_method_def(name='getSaltFromJava', signature='(Ljava/lang/String;)Ljava/lang/String;', native=False, args_list=['jstring'])
    def getSaltFromJava(self, mu, jstr):
        print('getSaltFromJava')
        return jstr.value.value + 'salt..'


@native_method
def sprintf(mu, buffer, format1, data1, data2):
    f = memory_helpers.read_utf8(mu, format1)
    data1 = memory_helpers.read_utf8(mu, data1)
    result = f % (data1, data2)
    # print('sprintf: %s' % result)
    mu.mem_write(buffer, bytes((result + '\x00').encode('utf-8')))


# Initialize emulator
emulator = Emulator(
    vfp_inst_set=True,
    vfs_root=r"C:\Users\Administrator\Desktop\unicorn-example\venv\Lib\site-packages\androidemu\vfs"
)
print(posixpath.join(posixpath.dirname(__file__), "vfs"))
# got hook
emulator.modules.add_symbol_hook('__aeabi_memclr', emulator.hooker.write_function(__aeabi_memclr) + 1)
emulator.modules.add_symbol_hook('__aeabi_memcpy', emulator.hooker.write_function(__aeabi_memcpy) + 1)
emulator.modules.add_symbol_hook('sprintf', emulator.hooker.write_function(sprintf) + 1)

# java hook
emulator.java_classloader.add_class(com_sec_udemo_MainActivity)

emulator.load_library("lib/libc.so", do_init=False)
libmod = emulator.load_library("lib/libnative-lib.so", do_init=False)

try:
    dbg = udbg.UnicornDebugger(emulator.mu)

    thiz = com_sec_udemo_MainActivity()
    s = emulator.call_symbol(libmod, "Java_com_sec_udemo_MainActivity_sign_1lv3", emulator.java_vm.jni_env.address_ptr, thiz, "123")
    print(s)

except UcError as e:
    list_tracks = dbg.get_tracks()
    ad = []
    for addr in list_tracks[-100:-1]:
        offset = hex(addr - 0xcbc66000)
        if offset.find('-') != 0:
            ad.append(offset)
    print(ad)
    print(e)
