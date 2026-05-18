from selenium.webdriver.common.by import By
from tests.selenium.pages.BasePage import BasePage
from tests.selenium.locators.RegisterLocators import RegisterLocators

class RegisterPage(BasePage):
    PATH = "/register"

    def open_page(self):
        self.open(self.PATH)

    def register(self, username, password, confirm):
        self.typing(*RegisterLocators.USERNAME_INPUT,username)
        self.typing(*RegisterLocators.PASSWORD_INPUT,password)
        self.typing(*RegisterLocators.COMFIRM_INPUT,confirm)
        self.click(*RegisterLocators.BUTTON)

    def result(self):
        elements = self.finds(*RegisterLocators.NOTIFICATION)
        return [e.text for e in elements]

    def screen_register(self, name):
        self.screen("register",name)