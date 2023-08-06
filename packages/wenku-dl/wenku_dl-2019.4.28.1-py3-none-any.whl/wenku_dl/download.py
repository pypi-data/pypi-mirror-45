import os
import requests

from wenku_dl.wenku import WenkuAPI
from wenku_dl.wenku import WenkuConfig

from aigpy import pathHelper
from aigpy import pdfHelper

class Downloader(object):
    def __init__(self):
        self.api = WenkuAPI()
    
    def start(self, url):
        conf = WenkuConfig()
        info = self.api.parse(url)
        path = pathHelper.getDiffTmpPathName(conf.outputdir)
        name = conf.outputdir + '/' + pathHelper.replaceLimitChar(info['title'], '-')
        # 下载图片
        pathHelper.mkdirs(path)
        array = []
        for index, item in enumerate(info['pngurls']):
            img = requests.get(item).content
            file = path + '/' + str(index) + '.png'
            with open(file, 'wb') as fp:
                fp.write(img)
                array.append(file)
        # 图片转pdf
        pdfHelper.imag2pdf(array, name+'.pdf')
        pathHelper.remove(path)
        print(f'[下载完成]{name}')
