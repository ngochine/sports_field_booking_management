import time

from selenium.webdriver.common.by import By
from tests.selenium.pages.BasePage import BasePage
from tests.selenium.locators.LoginLocators import LoginLocator

class LoginPage(BasePage):
    PATH = "/login"

    def open_page(self):
        self.open(self.PATH)

    def login(self, username, password):
        self.typing(*LoginLocator.USERNAME_INPUT,username)
        self.typing(*LoginLocator.PASSWORD_INPUT,password)
        time.sleep(1)
        self.click(*LoginLocator.BUTTON)

    def result(self):
        elements = self.finds(*LoginLocator.NOTIFICATION)
        return [e.text for e in elements]

    def screen_booking(self, name):
        self.screen("login",name)