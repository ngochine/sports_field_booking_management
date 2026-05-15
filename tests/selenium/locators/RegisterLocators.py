from selenium.webdriver.common.by import By


class RegisterLocators(object):
    USERNAME_INPUT = (By.ID,'username')
    PASSWORD_INPUT = (By.ID,'password')
    COMFIRM_INPUT = (By.ID,'confirm')
    BUTTON = (By.CSS_SELECTOR,'#registerForm > button')
    NOTIFICATION = (By.CSS_SELECTOR,'#flash-container > div')