
from lxml import etree
from PIL import Image
from selenium.webdriver.common.by import By

class SogouWeixinVerify(object):

    __crawl = None

    __screenSavePath = ""
    __verifyCodeSavePath = ""
    __keepVerify = True

    __sogouVerifyFunc = None
    __weixinVerifyFunc = None

    def __init__(self, crawl=None, 
        sogouVerifyFunc=None, 
        weixinVerifyFunc=None, 
        screenSavePath=None, 
        verifyCodeSavePath=None, 
        keepVerify=True):

        self.__crawl = crawl
        self.__sogouVerifyFunc = sogouVerifyFunc
        self.__weixinVerifyFunc = weixinVerifyFunc
        self.__screenSavePath = screenSavePath
        self.__verifyCodeSavePath = verifyCodeSavePath
        self.__keepVerify = keepVerify

    def checkSogouVerify(self):
        if self.__crawl is None:
            assert self.__crawl is not None
        
        # pageHtml = etree.HTML(crawl.getBrowser().page_source, etree.HTMLParser())
        sogouVerifyElement = self.__crawl.findElement(By.XPATH, '//*[@id="seccodeImage"]')
        
        if sogouVerifyElement:
            
            if callable(self.__sogouVerifyFunc):
                code = self.__sogouVerifyFunc(self.__crawl, self.getVerifyImg(sogouVerifyElement))
                if code:
                    return self.inputSogouVerifyCode(code)
                    
        return False

    def checkWeixinVerify(self):
        if self.__crawl is None:
            assert self.__crawl is not None

        weixinVerifyElement = self.__crawl.findElement(By.XPATH,'//*[@class="weui_input"]')
            
        if weixinVerifyElement:
            
            if callable(self.__weixinVerifyFunc):
                code = self.__weixinVerifyFunc(self.__crawl, self.getVerifyImg(weixinVerifyElement))
                if code:
                    pass
        return False

    def getVerifyImg(self, element):
        location = element.location
        size = element.size

        if self.__screenSavePath:
            self.__crawl.getBrowser().save_screenshot(self.__screenSavePath)

        x = location['x']
        y = location['y']
        width = location['x'] + size['width']
        height = location['y'] + size['height']

        im = Image.open(self.__screenSavePath)
        im = im.crop((int(x), int(y), int(width), int(height)))
        if self.__verifyCodeSavePath:
            im.save(self.__verifyCodeSavePath)
        return im

    def inputSogouVerifyCode(self, code):
        verifyInput = self.__crawl.findElement(By.ID, "seccodeInput")
        verifyInput.send_keys(code)
        self.__crawl.findElement(By.ID, "submit").click()
        sogouVerifyElement = self.__crawl.findElement(By.XPATH, '//*[@id="seccodeImage"]')

        if sogouVerifyElement and not self.__keepVerify:
            return False
        else:
            self.checkSogouVerify()

    def inputWeixinVerifyCode(self, code):
        pass