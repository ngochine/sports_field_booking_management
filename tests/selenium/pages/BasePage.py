from pathlib import Path

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from instances.config import Config
import os

class BasePage:
    def __init__(self,driver):
        self.driver=driver

    def open(self, path=""):
        self.driver.get(Config.BASE_URL + path)

    def close(self):
        self.driver.quit()

    def open_not_base(self,path=""):
        self.driver.get(path)

    def wait(self, by, value):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((by, value)))

    def find(self,by,value):
        self.wait(by,value)
        return self.driver.find_element(by,value)

    def finds(self,by,value):
        self.wait(by,value)
        return self.driver.find_elements(by,value)

    def typing(self,by,value,text):
        e=self.find(by,value)
        e.send_keys(text)

    def click(self,by,value):
        e = self.find(by, value)
        e.click()

    def get_text(self,by,value):
        e=self.find(by, value)
        return e.text

    def is_enabled(self,by,value):
        e=self.find(by, value)
        return e.is_enabled()

    def screen(self, folder, name):
        BASE_DIR = Path(__file__).resolve().parents[3]
        path = BASE_DIR / "docs" / "screenshots" / "selenium" / folder
        path.mkdir(parents=True, exist_ok=True)
        self.driver.save_screenshot(str(path / name))


    def get_url(self):
        return self.driver.current_url

    def scroll(self, f=700):
        self.driver.execute_script(f"window.scrollTo(0, {f});")

    def get_text_alert(self, timeout=5):
        try:
            alert = WebDriverWait(self.driver, timeout).until(
                EC.alert_is_present(),
            )
            text = alert.text
            alert.accept()
            return text
        except:
            return None