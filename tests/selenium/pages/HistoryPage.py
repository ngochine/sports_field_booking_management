import time
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains

from tests.selenium.pages.BasePage import BasePage
from tests.selenium.locators.HistoryLocators import (
    HistoryLocators,
    BookingCardLocators,
    CancelPopupLocators
)


class HistoryPage(BasePage):
    PATH = "/bookings"

    def open_page(self):
        self.open(self.PATH)

    def go_to_page(self, page_number):
        self.open(f"/bookings?page={page_number}")

    def get_cards(self):
        return self.finds(*HistoryLocators.BOOKING_CARD)

    def get_status(self, el):
        return el.find_element(*BookingCardLocators.TAG_STATUS).text.strip()

    def has_cancel(self, el):
        return len(el.find_elements(*BookingCardLocators.CANCEL_BUTTON)) > 0

    def get_name(self, el):
        return el.find_element(*BookingCardLocators.NAME_FIELD).text

    def get_date(self, el):
        return el.find_element(*BookingCardLocators.BOOKING_DATE).text

    def get_time(self, el):
        return el.find_element(*BookingCardLocators.BOOKING_TIME).text

    def get_price(self, el):
        return el.find_element(*BookingCardLocators.TOTAL_PRICE).text

    def get_detail(self,el):
        return el.find_element(*BookingCardLocators.DETAIL_BUTTON)

    def click_detail(self,el):
        e=self.get_detail(el)
        e.click()

    def click_cancel(self, el):
        btn = el.find_element(*BookingCardLocators.CANCEL_BUTTON)
        self.driver.execute_script( "arguments[0].scrollIntoView({block: 'center'});", btn)
        time.sleep(0.5)
        btn.click()


    def parse_booking_datetime(self, date_str, time_range):
        start_time_str = time_range.split("-")[0].strip()
        return datetime.strptime(
            f"{date_str} {start_time_str}",
            "%d/%m/%Y %H:%M:%S"
        )


    def has_next_page(self):
        time.sleep(1)
        self.scroll(8000)
        time.sleep(1)
        next_button = self.find(*HistoryLocators.NEXT_PAGE)
        if not next_button: return False
        parent = next_button.find_element(By.XPATH, "..")
        return "disabled" not in parent.get_attribute("class")


    def go_to_next_page(self):
        time.sleep(1)
        self.scroll(8000)
        self.driver.implicitly_wait(2)
        next_btn = self.find(*HistoryLocators.NEXT_PAGE)
        next_btn.click()


    def is_cancelable(self, el):
        if not self.has_cancel(el):
            return False
        booking_time = self.parse_booking_datetime(self.get_date(el),self.get_time(el))
        return datetime.now() < booking_time - timedelta(hours=2)


    def find_booking_by_info(self, booking_info):
        for el in self.get_cards():
            if (
                self.get_name(el) == booking_info["field_name"]
                and self.get_date(el) == booking_info["booking_date"]
                and self.get_time(el) == booking_info["time_range"]
            ):
                return el
        raise Exception("Không tìm thấy booking")


    def select_cancelable_booking(self):
        while True:
            for el in self.get_cards():
                if self.is_cancelable(el):
                    return el
            if not self.has_next_page():
                break
            self.go_to_next_page()
        raise Exception("Không tìm thấy booking đủ điều kiện huỷ (>2h trước giờ bắt đầu)")


    def get_cancelable_bookings(self):
        result = []
        page = 1
        while True:
            for i, el in enumerate(self.get_cards()):
                if self.is_cancelable(el):
                    result.append({
                        "page": page,
                        "index": i
                    })
            if not self.has_next_page():
                break
            self.go_to_next_page()
            page += 1
        return result


    def get_booking_info(self,el):
        return {
            "field_name": self.get_name(el),
            "booking_date": self.get_date(el),
            "time_range": self.get_time(el),
            "total_price": self.get_price(el),
        }


    def get_cancel_popup_info(self):
        self.wait(*CancelPopupLocators.POPUP_BOOKING_DATE)
        return {
            "field_name": self.get_text(*CancelPopupLocators.POPUP_NAME_FIELD),
            "booking_date": self.get_text(*CancelPopupLocators.POPUP_BOOKING_DATE),
            "time_range": self.get_text(*CancelPopupLocators.POPUP_BOOKING_TIME),
            "total_price": self.get_text(*CancelPopupLocators.POPUP_TOTAL_PRICE),
        }

    def confirm_cancel_booking(self):
        self.click(*CancelPopupLocators.POPUP_CANCEL_BUTTON)

    def close_cancel_popup(self):
        try:
            self.click(*CancelPopupLocators.POPUP_BACK_BUTTON)
        except:
            self.click(*CancelPopupLocators.POPUP_CLOSE_BUTTON)

    def double_click_cancel(self):
        btn = self.find(*CancelPopupLocators.POPUP_CANCEL_BUTTON)
        ActionChains(self.driver).double_click(btn).perform()

    def get_status_booking(self, el):
        return self.get_status(el)

    def assert_popup_matches(self, el):
        booking_info = self.get_booking_info(el)
        popup = self.get_cancel_popup_info()
        assert popup["field_name"] == booking_info["field_name"], "Sai tên sân"
        assert popup["booking_date"] == booking_info["booking_date"], "Sai ngày đặt"
        assert popup["time_range"] == booking_info["time_range"], "Sai thời gian"
        assert (popup["total_price"]).replace("VNĐ", "VND").strip() == (booking_info["total_price"]).replace("VNĐ", "VND").strip(), "Sai tổng tiền"

    def screen_cancel(self, name):
        self.screen("cancel", name)

    def get_link(self,el):
        button = self.get_detail(el)
        href = button.get_attribute('href')
        return href

    def get_link_booking(self,booking_info):
        el=self.find_booking_by_info(booking_info)
        self.get_link(el)

    def open_not_base(self,path=""):
        self.driver.get(path)