import os
import requests

from wenku_dl.wenku import WenkuAPI
from wenku_dl.wenku import WenkuConfig

from aigpy import pathHelper
from aigpy import pdfHelper
from aigpy import threadHelper

class Downloader(object):
    def __init__(self, threadnum = 3):
        self.api = WenkuAPI()
        self.thread = threadHelper.ThreadTool(threadnum)

    def __threadfuc__(self, data):
        img = requests.get(data['url']).content
        file = data['path']
        with open(file, 'wb') as fp:
                fp.write(img)

    def start(self, url):
        conf = WenkuConfig()
        info = self.api.parse(url)
        path = pathHelper.getDiffTmpPathName(conf.outputdir)
        name = conf.outputdir + '/' + pathHelper.replaceLimitChar(info['title'], '-')
        # 下载图片
        pathHelper.mkdirs(path)
        array = []
        for index, item in enumerate(info['pngurls']):
            file = path + '/' + str(index) + '.png'
            para = {'url': item, 'path': file}
            self.thread.start(self.__threadfuc__, para)
            array.append(file)
        self.thread.waitAll()
        # 图片转pdf
        pdfHelper.imag2pdf(array, name+'.pdf')
        pathHelper.remove(path)
        print('[下载完成] '+ name)
        
