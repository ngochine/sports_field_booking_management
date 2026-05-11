from instances.config import Config
import os

class BasePage:
    def __init__(self,driver):
        self.driver=driver

    def open(self, path=""):
        self.driver.get(Config.BASE_URL + path)

    def find(self,by,value):
        return self.driver.find_element(by,value)

    def finds(self,by,value):
        return self.driver.find_elements(by,value)

    def typing(self,by,value,text):
        e=self.find(by,value)
        e.send_keys(text)

    def click(self,by,value):
        e = self.find(by, value)
        e.click()

    def screen(self, SCREENSHOT_DIR ,name):
        os.makedirs(SCREENSHOT_DIR, exist_ok=True)
        self.driver.save_screenshot(os.path.join(SCREENSHOT_DIR, name))
