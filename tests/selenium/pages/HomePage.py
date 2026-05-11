from selenium.webdriver.common.by import By
from tests.selenium.pages.BasePage import BasePage

class HomePage(BasePage):
    URL= 'http://127.0.0.1:5000'


    SEARCH_INPUT = (By.CSS_SELECTOR,'#collapsibleNavbar > form > input')
    SEARCH_BUTTON = (By.CSS_SELECTOR,'#collapsibleNavbar > form > button')

    def get_order_btn_locator(self, index):
        return (By.CSS_SELECTOR, f'.container .row > div:nth-child({index}) div > div > button')

    def open_page(self):
        self.open(self.URL)

    def search(self,kw):
        self.typing(*self.SEARCH_INPUT,kw)
        self.click(*self.SEARCH_BUTTON)


    def order(self):
        self.order(*self.get_order_btn_locator(1))
        self.driver.implicitly_wait(1)
        self.click(*self.get_order_btn_locator(1))
        self.driver.implicitly_wait(1)
        self.click(*self.get_order_btn_locator(2))
        self.driver.implicitly_wait(1)