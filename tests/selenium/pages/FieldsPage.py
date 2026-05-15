from selenium.webdriver.common.by import By
from tests.selenium.pages.BasePage import BasePage

class FieldsPage(BasePage):
    PATH = "/fields"

    def open_page(self):
        self.open(self.PATH)

class ListComponent(FieldsPage):
    LINK_BUTTON = (By.CSS_SELECTOR,'.card-body a')

    def get_link(self, index):
        fields = self.finds(*self.LINK_BUTTON)
        p = fields[int(index)]
        href = p.get_attribute('href')
        return href