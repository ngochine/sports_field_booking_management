from tests.selenium.pages.BasePage import BasePage


class HomePage(BasePage):
    PATH = "/"

    def open_page(self):
        self.open(self.PATH)