from selenium.webdriver.common.by import By


class LoginLocator(object):
    USERNAME_INPUT = (By.ID,'username')
    PASSWORD_INPUT = (By.ID,'password')
    BUTTON = (By.CSS_SELECTOR,'#loginForm > button')
    NOTIFICATION = (By.CSS_SELECTOR,'#flash-container > div')