from selenium.webdriver.common.by import By
from tests.selenium.pages.BasePage import BasePage

class LoginPage(BasePage):
    PATH = "/login"

    USERNAME_INPUT = (By.ID,'username')
    PASSWORD_INPUT = (By.ID,'password')
    BUTTON = (By.CSS_SELECTOR,'#loginForm > button')
    NOTIFICATION = (By.CSS_SELECTOR,'#flash-container > div')

    def open_page(self):
        self.open(self.PATH)

    def login(self, username, password):
        self.typing(*self.USERNAME_INPUT,username)
        self.typing(*self.PASSWORD_INPUT,password)
        self.click(*self.BUTTON)

    def result(self):
        elements = self.finds(*self.NOTIFICATION)
        return [e.text for e in elements]