from selenium.webdriver.common.by import By
from tests.selenium.pages.BasePage import BasePage

class RegisterPage(BasePage):
    PATH = "/register"


    USERNAME_INPUT = (By.ID,'username')
    PASSWORD_INPUT = (By.ID,'password')
    COMFIRM_INPUT = (By.ID,'confirm')
    BUTTON = (By.CSS_SELECTOR,'#registerForm > button')
    NOTIFICATION = (By.CSS_SELECTOR,'#flash-container > div')

    def open_page(self):
        self.open(self.PATH)

    def register(self, username, password, confirm):
        self.typing(*self.USERNAME_INPUT,username)
        self.typing(*self.PASSWORD_INPUT,password)
        self.typing(*self.COMFIRM_INPUT,confirm)
        self.click(*self.BUTTON)

    def result(self):
        elements = self.finds(*self.NOTIFICATION)
        return [e.text for e in elements]