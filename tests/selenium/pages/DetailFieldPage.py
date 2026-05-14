import time
from datetime import datetime
from selenium.webdriver.common.by import By

from tests.selenium.data.booking_data import BOOKING_CASES
from tests.selenium.pages.BasePage import BasePage


class DetailFieldPage(BasePage):
    FIELD_NAME = (By.CSS_SELECTOR, "body > div:nth-child(3) > div.position-relative.mb-5  h1")
    ADDRESS = (By.CSS_SELECTOR, "body > div:nth-child(3) > div.position-relative.mb-5  span.me-3")

    def open_page(self, link):
        self.open_not_base(link)

    def get_field_name(self):
        return self.find(*self.FIELD_NAME).text

    def get_address(self):
        return self.find(*self.ADDRESS).text


class BookingInfoComponent(DetailFieldPage):
    DATE_INPUT = (By.ID, 'dateSelectedValue')
    START_TIME = (By.ID, 'startTime')
    END_TIME = (By.ID, 'endTime')
    TOTAL_TIME = (By.ID, 'totalTime')
    TOTAL_PRICE = (By.ID, 'totalPrice')
    BOOK_BUTTON = (By.CSS_SELECTOR, '.col-lg-4 .card-body > div:nth-child(5) > button')
    TABLE_PRICE = (By.CSS_SELECTOR, '#fieldPriceContainer tbody tr')
    END_INPUT = ('body > div:nth-child(6) input.flatpickr-hour','body > div:nth-child(6) input.flatpickr-minute')
    START_INPUT = ('body > div:nth-child(7) input.flatpickr-hour','body > div:nth-child(7) input.flatpickr-minute')

    def parse_time(self, time_str: str):
        return datetime.strptime(time_str.strip(), "%H:%M")

    def time_to_minutes(self, t: str):
        h, m = t.split(":")
        return int(h) * 60 + int(m)

    def minutes_to_time_str(self, minutes):
        h = minutes // 60
        m = minutes % 60
        return f"{h:02d}:{m:02d}"

    def set_value(self, element_id, value):
        self.driver.execute_script("""
            let el = document.getElementById(arguments[0]); 
            el.value = arguments[1]; 
            el.dispatchEvent(new Event('change', { bubbles: true }))
        """, element_id, value)

    def set_value_flat(self, element_css, value):
        self.driver.execute_script("""
            let el = document.querySelector(arguments[0]);
            el.value = arguments[1];
            el.dispatchEvent(new Event('input', { bubbles: true }));
            el.dispatchEvent(new Event('change', { bubbles: true }));
            el.dispatchEvent(new Event('blur', { bubbles: true }));
        """, element_css, value)

    def set_flatpickr_time(self, input_locator, hour, minute, sel_hour_css, sel_minute_css):
        self.driver.execute_script(
            """document.querySelector('#' + arguments[0]).click();""",
            input_locator[1]
        )
        time.sleep(1)
        self.set_value_flat(sel_hour_css, str(hour).zfill(2))
        self.set_value_flat(sel_minute_css, str(minute).zfill(2))
        self.driver.execute_script("""document.activeElement.blur();""")

    def select_booking_info(self, date=BOOKING_CASES["default_day"], start_time="", end_time=""):
        self.scroll(800)
        self.set_value(self.DATE_INPUT[1], date)
        if start_time:
            start_h, start_m = start_time.split(":")
            self.set_flatpickr_time(self.START_TIME, start_h, start_m, self.START_INPUT[0], self.START_INPUT[1])
        if end_time:
            end_h, end_m = end_time.split(":")
            self.set_flatpickr_time(self.END_TIME, end_h, end_m, self.END_INPUT[0], self.END_INPUT[1])
        time.sleep(2)

    def open_popup(self):
        time.sleep(1)
        self.scroll()
        self.driver.implicitly_wait(1)
        self.click(*self.BOOK_BUTTON)

    def get_date_value(self):
        return self.find(*self.DATE_INPUT).get_attribute("value")

    def get_start_time_value(self):
        return self.find(*self.START_TIME).get_attribute("value")

    def get_end_time_value(self):
        return self.find(*self.END_TIME).get_attribute("value")

    def get_total_time(self):
        return self.find(*self.TOTAL_TIME).text

    def get_total_price(self):
        return self.find(*self.TOTAL_PRICE).text.replace(".", "")

    def get_price_table(self):
        rows = self.finds(*self.TABLE_PRICE)
        result = []
        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            result.append({
                "start_time": cols[0].text.strip()[:5] ,
                "end_time": cols[1].text.strip()[:5] ,
                "price": int(cols[2].text.replace(" VNĐ", "").replace(".", "").replace(",",""))
            })
        return result

    def get_valid_slots(self):
        return [(row["start_time"], row["end_time"]) for row in self.get_price_table()]

    def get_outside_time(self):
        slots = self.get_valid_slots()
        if slots:
            slots_sorted = sorted(slots, key=lambda x: self.time_to_minutes(x[0]))
            first_start = slots_sorted[0][0]
            last_end = slots_sorted[-1][1]
            first_start_min = self.time_to_minutes(first_start)
            last_end_min = self.time_to_minutes(last_end)
            if first_start_min >= 60:
                return "00:00", self.minutes_to_time_str(first_start_min - 60)
            if last_end_min <= (24 * 60 - 60):
                return self.minutes_to_time_str(last_end_min), self.minutes_to_time_str(last_end_min + 60)
            for i in range(len(slots_sorted) - 1):
                end_current = self.time_to_minutes(slots_sorted[i][1])
                start_next = self.time_to_minutes(slots_sorted[i + 1][0])
                if start_next - end_current >= 60:
                    return self.minutes_to_time_str(end_current), self.minutes_to_time_str(end_current + 60)
        return "00:00", "01:00"

    def get_price_by_time(self, start_time, end_time):
        table = self.get_price_table()
        start_min = self.time_to_minutes(start_time)
        end_min = self.time_to_minutes(end_time)
        if end_min <= start_min:
            return None
        hours = (end_min - start_min) / 60
        for row in table:
            row_start = self.time_to_minutes(row["start_time"])
            row_end = self.time_to_minutes(row["end_time"])
            if row_start <= start_min < row_end:
                return str(int(row["price"] * hours))
        return None

    def calculate_price_multi_slot(self, start_time, end_time):
        start_min = self.time_to_minutes(start_time)
        end_min = self.time_to_minutes(end_time)
        if end_min <= start_min:
            return "0"
        total = 0
        for row in self.get_price_table():
            slot_start = self.time_to_minutes(row["start_time"])
            slot_end = self.time_to_minutes(row["end_time"])
            price_per_hour = row["price"]
            overlap_start = max(start_min, slot_start)
            overlap_end = min(end_min, slot_end)
            if overlap_start < overlap_end:
                hours = (overlap_end - overlap_start) / 60
                total += hours * price_per_hour
        return str(int(total))

    def get_adjacent_slots_time(self):
        self.scroll(500)
        slots = self.get_valid_slots()
        for i in range(len(slots) - 1):
            s1, e1 = slots[i]
            s2, e2 = slots[i + 1]
            if e1 == s2:
                return s1, e2
        return None, None

    def fill_booking(self, date=BOOKING_CASES["default_day"], slot_index= BOOKING_CASES["valid_slot_index"]):
        slots = self.get_valid_slots()
        start, end = slots[slot_index]
        self.select_booking_info(date=date, start_time=start, end_time=end)
        time.sleep(1)
        return start, end


class PopupComponent(DetailFieldPage):
    CONFIRM_MODAL = (By.CSS_SELECTOR, "#confirmBookingModal .modal-content")
    CONFIRM_FIELD_NAME = (By.CSS_SELECTOR,"#confirmBookingModal .modal-content > .modal-body > div:nth-child(2) > div:nth-child(1) > span:nth-child(2)")
    CONFIRM_ADDRESS = (By.ID, "confirmFieldAddress")
    DATE = (By.ID, "confirmDate")
    START_TIME = (By.ID, "confirmStartTime")
    END_TIME = (By.ID, "confirmEndTime")
    DURATION = (By.ID, "confirmDuration")
    TOTAL_PRICE = (By.ID, "confirmTotalPrice")
    CLOSE_BTN = (By.CSS_SELECTOR, "#confirmBookingModal .btn-close")
    CANCEL_BTN = (By.CSS_SELECTOR, "#confirmBookingModal .modal-footer > button:nth-child(1)")
    CONFIRM_BTN = (By.CSS_SELECTOR, "#confirmBookingModal .modal-footer > button:nth-child(2)")

    def is_visible(self):
        time.sleep(1)
        return self.find(*self.CONFIRM_MODAL).is_displayed()

    def close_popup(self):
        self.click(*self.CLOSE_BTN)

    def cancel_popup(self):
        self.click(*self.CANCEL_BTN)

    def confirm_booking(self):
        self.click(*self.CONFIRM_BTN)

    def get_confirm_field_name(self):
        return self.find(*self.CONFIRM_FIELD_NAME).text

    def get_confirm_address(self):
        return self.find(*self.CONFIRM_ADDRESS).text

    def get_date(self):
        return self.find(*self.DATE).text

    def get_start_time(self):
        return self.find(*self.START_TIME).text.strip()

    def get_end_time(self):
        return self.find(*self.END_TIME).text.strip()

    def get_duration(self):
        return self.find(*self.DURATION).text.replace("Giờ", "").replace(" ", "").strip()

    def get_total_price(self):
        return self.find(*self.TOTAL_PRICE).text.replace(".", "").replace(" VND", "").strip()

    def verify_confirm_info(self, field_name, address, date, start_time, end_time, total_duration, total_price):
        errors = []
        if self.get_confirm_field_name() != field_name:
            errors.append(f"Field name sai: {self.get_confirm_field_name()} != {field_name}")
        if self.get_confirm_address() != address:
            errors.append(f"Address sai: {self.get_confirm_address()} != {address}")
        if self.get_date() != date:
            errors.append(f"Date sai: {self.get_date()} != {date}")
        if self.get_start_time() != start_time:
            errors.append(f"Start time sai: {self.get_start_time()} != {start_time}")
        if self.get_end_time() != end_time:
            errors.append(f"End time sai: {self.get_end_time()} != {end_time}")
        if int(self.get_duration()) != int(total_duration):
            errors.append(f"Total duration sai: {self.get_duration()} != {total_duration}")
        if int(self.get_total_price()) != int(total_price):
            errors.append(f"Total price sai: {self.get_total_price()} != {total_price}")
        return errors