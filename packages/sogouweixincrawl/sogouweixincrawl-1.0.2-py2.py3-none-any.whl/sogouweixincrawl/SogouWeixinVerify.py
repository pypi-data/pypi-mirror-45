
from lxml import etree
from PIL import Image
from selenium.webdriver.common.by import By

class SogouWeixinVerify(object):

    __screenSavePath = ""
    __verifyCodeSavePath = ""

    def __init__(self, screenSavePath, verifyCodeSavePath):
        self.__screenSavePath = screenSavePath
        self.__verifyCodeSavePath = verifyCodeSavePath

    def check(self, crawl=None, sogouVerifyFunc=None, weixinVerifyFunc=None):
        if crawl is None:
            return
        
        # pageHtml = etree.HTML(crawl.getBrowser().page_source, etree.HTMLParser())
        sogouVerifyElement = crawl.findElement(By.XPATH, '//*[@id="seccodeImage"]')
        
        if sogouVerifyElement:
            
            if callable(sogouVerifyFunc):
                sogouVerifyFunc(crawl, self.getVerifyImg(crawl, sogouVerifyElement))
            return
        
        weixinVerifyElement = crawl.findElement(By.XPATH,'//*[@class="weui_input"]')
        
        if weixinVerifyElement:
            
            if callable(weixinVerifyFunc):
                weixinVerifyFunc(crawl, self.getVerifyImg(crawl, weixinVerifyElement))
            return

    def getVerifyImg(self, crawl, element):
        location = element.location
        size = element.size

        if self.__screenSavePath:
            crawl.getBrowser().save_screenshot(self.__screenSavePath)

        x = location['x']
        y = location['y']
        width = location['x'] + size['width']
        height = location['y'] + size['height']

        im = Image.open(self.__screenSavePath)
        im = im.crop((int(x), int(y), int(width), int(height)))
        if self.__verifyCodeSavePath:
            im.save(self.__verifyCodeSavePath)
        return im