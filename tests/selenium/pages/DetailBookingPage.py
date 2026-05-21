from tests.selenium.pages.BasePage import BasePage
from tests.selenium.locators.DetailBookingLocators import DetailBookingLocators


class DetailBookingPage(BasePage):

    def open_page(self, link):
        self.open_not_base(link)

    def click_cancel(self):
        self.click(*DetailBookingLocators.CANCEL_BUTTON)

    def screen_cancel(self, name):
        self.screen("cancel", name)