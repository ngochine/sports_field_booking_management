from selenium.webdriver.common.by import By
from tests.selenium.pages.BasePage import BasePage
from tests.selenium.locators.FieldsLocators import ListFieldsLocators


class FieldsPage(BasePage):
    PATH = "/fields"

    def open_page(self):
        self.open(self.PATH)

    def get_link(self, index):
        fields = self.finds(*ListFieldsLocators.LINK_BUTTON)
        p = fields[int(index)]
        href = p.get_attribute('href')
        return href