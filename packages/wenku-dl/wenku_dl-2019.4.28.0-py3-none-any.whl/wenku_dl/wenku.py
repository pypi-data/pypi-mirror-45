import os
import re
import json
import requests
from aigpy import configHelper

class WenkuAPI(object):
    def __init__(self):
        pass

    def getDocid(self, inurl):
        try:
            return re.findall('view/(.*).html', inurl)[0]
        except:
            return None
    
    def getDocInfo(self, inurl):
        docid = self.getDocid(inurl)
        url   = f'https://wenku.baidu.com/api/doc/getdocinfo?callback=json&doc_id={docid}'
        data  = requests.get(url).text
        data  = re.match(r'.*json\((.*)\)', data).group(1)
        data  = data.encode().decode('unicode_escape')
        data  = json.loads(data)
        return data

    def getPngUrls(self, inurl):
        html  = requests.get(inurl).text
        urls  = re.search("WkInfo.htmlUrls = '(.*)'", html).group(1)
        urls  = urls.replace(r'\/', '/')
        urls  = urls.encode().decode('unicode_escape')
        urls  = json.loads(urls)
        array = []
        for url in urls['png']:
            array.append(url['pageLoadUrl'])
        return array
    
    def parse(self, inurl):
        docid   = self.getDocid(inurl)
        pngurls = self.getPngUrls(inurl)
        info    = self.getDocInfo(inurl)
        ret = {'docid': docid, 
               'pngurls': pngurls,
               'title': info['docInfo']['docTitle'],
               'creattime': info['docInfo']['createTime']}
        return ret
  
class WenkuConfig(object):
    FILE_NAME = "wenku.ini"
    def __init__(self):
        self.outputdir   = configHelper.GetValue("base", "outputdir", "./", self.FILE_NAME)
        self.threadnum   = configHelper.GetValue("base", "threadnum", "3", self.FILE_NAME)
    
    def set(self, outputdir=None, threadnum=None):
        if outputdir is not None:
            configHelper.SetValue("base", "outputdir", outputdir, self.FILE_NAME)
            self.outputdir = outputdir
        if threadnum is not None:
            configHelper.SetValue("base", "threadnum", threadnum, self.FILE_NAME)
            self.threadnum = threadnum
