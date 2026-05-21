import time
from datetime import datetime, timedelta
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from tests.selenium.data.booking_data import BOOKING_CASES
from tests.selenium.pages.BasePage import BasePage
from tests.selenium.locators.DetailFieldLocators import DetailFieldLocators,BookingInfoLocators,PopupLocator


class DetailFieldPage(BasePage):

    def open_page(self, link):
        self.open_not_base(link)

    def get_field_name(self):
        return self.get_text(*DetailFieldLocators.FIELD_NAME)

    def get_address(self):
        return self.get_text(*DetailFieldLocators.ADDRESS)

    def get_err(self):
        return self.get_text(*BookingInfoLocators.ERR_MESSAGE)

    def time_to_minutes(self, t: str):
        h, m = t.split(":")
        return int(h) * 60 + int(m)

    def minutes_to_time_str(self, minutes):
        h = minutes // 60
        m = minutes % 60
        return f"{h:02d}:{m:02d}"

    def add_hours(self, time_str, hours):
        total_minutes = self.time_to_minutes(time_str)
        total_minutes += int(hours * 60)
        total_minutes %= 24 * 60
        return self.minutes_to_time_str(total_minutes)

    def reduct_hours(self, time_str, hours=1):
        total_minutes = self.time_to_minutes(time_str) - hours * 60
        total_minutes %= 24 * 60
        return self.minutes_to_time_str(total_minutes)


    def set_value(self, element_id, value):
        self.driver.execute_script("""
            let el = document.getElementById(arguments[0]); 
            el.value = arguments[1]; 
            el.dispatchEvent(new Event('change', { bubbles: true }))
            el.dispatchEvent(new Event('blur', { bubbles: true }));
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
        self.set_value(BookingInfoLocators.DATE_INPUT[1], date)
        if start_time:
            start_h, start_m = start_time.split(":")
            self.set_flatpickr_time(BookingInfoLocators.START_TIME, start_h, start_m, *BookingInfoLocators.START_INPUT)
        if end_time:
            end_h, end_m = end_time.split(":")
            self.set_flatpickr_time(BookingInfoLocators.END_TIME, end_h, end_m, *BookingInfoLocators.END_INPUT)
        time.sleep(1)


    def open_popup(self):
        time.sleep(0.5)
        self.scroll()
        self.click(*BookingInfoLocators.BOOK_BUTTON)

    def double_click_booking(self):
        book_btn= self.find(*BookingInfoLocators.BOOK_BUTTON)
        ActionChains(self.driver) \
            .double_click(book_btn) \
            .perform()

    def get_date_value(self):
        return self.find(*BookingInfoLocators.DATE_INPUT).get_attribute("value")

    def get_date_min(self):
        return self.find(*BookingInfoLocators.DATE_INPUT).get_attribute("min")

    def get_start_time_value(self):
        return self.find(*BookingInfoLocators.START_TIME).get_attribute("value")

    def get_end_time_value(self):
        return self.find(*BookingInfoLocators.END_TIME).get_attribute("value")

    def get_total_time(self):
        return self.find(*BookingInfoLocators.TOTAL_TIME).text

    def get_total_price(self):
        return self.find(*BookingInfoLocators.TOTAL_PRICE).text.replace(".", "")

    def get_price_table(self):
        rows = self.finds(*BookingInfoLocators.TABLE_PRICE)
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

    def space_time(self):
        end_time = self.get_end_time_value()
        start_time = self.get_start_time_value()
        return self.time_to_minutes(end_time) - self.time_to_minutes(start_time)

    def fill_booking(self, date=BOOKING_CASES["default_day"], slot_index= BOOKING_CASES["valid_slot_index"]):
        slots = self.get_valid_slots()
        start, end = slots[slot_index]
        self.select_booking_info(date=date, start_time=start, end_time=end)
        time.sleep(1)
        return start, end

    def fill_part_booking(self, date=BOOKING_CASES["default_day"], slot_index= BOOKING_CASES["valid_slot_index"]):
        slots = self.get_valid_slots()
        start, _ = slots[slot_index]
        end=self.add_hours(start,0.5)
        print(start, end)
        self.select_booking_info(date=date, start_time=start, end_time=end)
        time.sleep(1)
        return start, end

    def part_time(self,date=BOOKING_CASES["default_day"], slot_index= 0):
        slots = self.get_valid_slots()
        start, end = slots[slot_index]
        start_dt = datetime.strptime(start, "%H:%M")
        end_dt = datetime.strptime(end, "%H:%M")
        while end_dt - start_dt < timedelta(hours=2):
            slot_index += 1
            start, end = slots[slot_index]
            start_dt = datetime.strptime(start, "%H:%M")
            end_dt = datetime.strptime(end, "%H:%M")
        start_str = start_dt.strftime("%H:%M")
        end_str = (end_dt - timedelta(hours=1)).strftime("%H:%M")
        self.select_booking_info(date=date, start_time=start_str, end_time=end_str)
        time.sleep(1)
        return start_str, end_str

    def plus_date(self,num):
        return (datetime.strptime(BOOKING_CASES["default_day"], "%Y-%m-%d") + timedelta(days=num)).strftime("%Y-%m-%d")

    def is_visible(self):
        return self.find(*PopupLocator.CONFIRM_MODAL).is_displayed()

    def close_popup(self):
        self.click(*PopupLocator.CLOSE_BTN)

    def cancel_popup(self):
        self.click(*PopupLocator.CANCEL_BTN)

    def confirm_booking(self):
        self.click(*PopupLocator.CONFIRM_BTN)

    def double_confirm_booking(self):
        book_btn= self.find(*PopupLocator.CONFIRM_BTN)
        ActionChains(self.driver) \
            .double_click(book_btn) \
            .perform()

    def get_confirm_field_name(self):
        return self.find(*PopupLocator.CONFIRM_FIELD_NAME).text

    def get_confirm_address(self):
        return self.find(*PopupLocator.CONFIRM_ADDRESS).text

    def get_date(self):
        return self.find(*PopupLocator.DATE).text

    def get_start_time(self):
        return self.find(*PopupLocator.START_TIME).text.strip()

    def get_end_time(self):
        return self.find(*PopupLocator.END_TIME).text.strip()

    def get_duration(self):
        return self.find(*PopupLocator.DURATION).text.replace("Giờ", "").replace(" ", "").strip()

    def get_total_price_popup(self):
        return self.find(*PopupLocator.TOTAL_PRICE).text.replace(".", "").replace(" VND", "").strip()

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
        if int(self.get_total_price_popup()) != int(total_price):
            errors.append(f"Total price sai: {self.get_total_price_popup()} != {total_price}")
        return errors

    def screen_booking(self, name):
        self.screen("booking",name)

    def count_popup(self):
        return len(self.finds(*PopupLocator.CONFIRM_MODAL))

    def count_alert(self):
        try:
            self.driver.switch_to.alert
            return 1
        except:
            return 0

    def get_booking_popup_info(self):
        return {
            "field_name": self.get_confirm_field_name(),
            "booking_date": datetime.strptime(self.get_date(),"%Y-%m-%d").strftime("%d/%m/%Y"),
            "time_range": (f'{self.get_start_time()}:00 - {self.get_end_time()}:00'),
            "total_price": self.get_total_price_popup(),
        }

