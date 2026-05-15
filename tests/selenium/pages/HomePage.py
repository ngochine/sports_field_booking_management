from selenium.webdriver.common.by import By
from tests.selenium.pages.BasePage import BasePage

class HomePage(BasePage):
    PATH = "/"
    def open_page(self):
        self.open(self.PATH)
    LINK_BUTTON = (By.CSS_SELECTOR,'body > div:nth-child(3) > div:nth-child(2) > div > div.row > div:nth-child(2) > div > div > a')
