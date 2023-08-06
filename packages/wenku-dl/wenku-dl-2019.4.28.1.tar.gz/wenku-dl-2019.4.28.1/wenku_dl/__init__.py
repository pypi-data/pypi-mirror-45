
import os
from aigpy.cmdHelper import myinput, myinputInt
import aigpy.pathHelper as pathHelper

from wenku_dl.download import Downloader
from wenku_dl.wenku import WenkuConfig

WENKU_DL_VERSION = '2019.4.28.1'

def setting(cf):
    print('--------------设置--------------')
    while True:
        out = myinput('输出目录:')
        if not os.path.exists(out):
            if pathHelper.mkdirs(out) is False:
                print('[错误] 输入地址不正确!')
                continue
        break
    while True:
        num = myinputInt('线程数:', 0)
        if num == 0:
            print('[错误] 输入数量不正确!')
            continue
        break
    cf.set(out, str(num))

def printMenu(cf):
    print("====================Wenku-dl========================")
    print("[输出目录]: " + cf.outputdir)
    print("[线程数量]: " + cf.threadnum)
    print("[输入0]  : 退出")
    print("[输入1]  : 设置")
    print("[输入url]: 下载链接文档")
    print("===================================================")

def main(argv=None):
    cf = WenkuConfig()
    dl = Downloader()
    while True:
        printMenu(cf)
        url = myinput('输入:')
        if url == '0':
            return
        if url == '1':
            setting(cf)
            continue
        dl.start(url)
        
__all__ = ['main']
