import time, os
from datetime import datetime, timedelta

from tests.selenium.data.booking_data import BOOKING_CASES
from tests.test_base import driver, test_app
from tests.selenium.fixture import booking_page, popup, detail_page,fields_page,auth_driver
from tests.selenium.guest_fixture import guest_booking_page,guest_popup,guest_detail_page,guest_fields_page

SCREENSHOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),  "booking")


def test_tc1_valid_booking_not_logged_in(guest_booking_page, guest_popup):
    guest_booking_page.scroll()
    guest_booking_page.fill_booking()
    time.sleep(1)
    guest_booking_page.open_popup()
    time.sleep(2)
    guest_popup.confirm_booking()
    alert = guest_popup.get_text_alert()
    guest_booking_page.screen(SCREENSHOT_DIR, "TC1_guest_booking.png")
    assert "Vui lòng đăng nhập để thực hiện chức năng này" in alert


def test_tc2_total_time_price_one_slot(booking_page, popup):
    start, end = booking_page.fill_booking()
    total_price = booking_page.get_total_price()
    expected_price = booking_page.get_price_by_time(start, end)
    booking_page.screen(SCREENSHOT_DIR, "TC2_total_time_price_one_slot.png")
    assert expected_price == total_price


def test_tc3_total_time_price_multi_slot(booking_page):
    start, end = booking_page.get_adjacent_slots_time()
    booking_page.select_booking_info(start_time=start, end_time=end)
    total_price = int(booking_page.get_total_price())
    expected_price = booking_page.calculate_price_multi_slot(start, end)
    booking_page.screen(SCREENSHOT_DIR, "TC3_total_time_price_multi_slot.png")
    assert total_price == int(expected_price)


def test_tc4_update_total_price_when_change_time(booking_page, popup):
    start, end = booking_page.fill_booking()
    price_before = booking_page.get_total_price()
    booking_page.screen(SCREENSHOT_DIR, "TC4_before_total_price.png")
    time.sleep(1)
    new_end = (datetime.strptime(end, "%H:%M") - timedelta(hours=1)).strftime("%H:%M")
    booking_page.select_booking_info(start_time=start,end_time= new_end)
    time.sleep(1)
    price_after = booking_page.get_total_price()
    booking_page.screen(SCREENSHOT_DIR, "TC4_update_total_price.png")
    assert price_before != price_after


def test_tc5_valid_booking(booking_page, popup, detail_page):
    url = booking_page.get_url()
    field_name = detail_page.get_field_name()
    address = detail_page.get_address()
    time.sleep(1)
    booking_page.scroll()
    booking_page.fill_booking()
    booking_page.open_popup()
    assert popup.is_visible()
    errors = popup.verify_confirm_info(
        field_name=field_name,
        address=address,
        date=BOOKING_CASES["default_day"],
        start_time=booking_page.get_start_time_value(),
        end_time=booking_page.get_end_time_value(),
        total_duration=booking_page.get_total_time(),
        total_price=int(booking_page.get_total_price()),
    )
    assert errors == []
    popup.confirm_booking()
    time.sleep(2)
    booking_page.screen(SCREENSHOT_DIR, "TC5_valid_booking.png")
    assert url != booking_page.get_url()


def test_tc6_cancel_popup(booking_page, popup):
    url_before = booking_page.get_url()
    booking_page.fill_booking()
    booking_page.open_popup()
    assert popup.is_visible()
    popup.cancel_popup()
    time.sleep(1)
    booking_page.screen(SCREENSHOT_DIR, "TC6_cancel_popup.png")
    assert popup.is_visible() == False
    assert url_before == booking_page.get_url()


def test_tc7_close_popup_x(booking_page, popup):
    url_before = booking_page.get_url()
    booking_page.fill_booking()
    booking_page.open_popup()
    time.sleep(1)
    assert popup.is_visible()
    popup.close_popup()
    time.sleep(1)
    booking_page.screen(SCREENSHOT_DIR, "TC7_close_popup_x.png")
    assert popup.is_visible() == False
    assert url_before == booking_page.get_url()


def test_tc8_empty_date(booking_page, popup):
    booking_page.fill_booking(date="")
    booking_page.open_popup()
    booking_page.screen(SCREENSHOT_DIR, "TC8_empty_date.png")
    assert popup.is_visible()== False

def test_tc9_past_date_disabled(booking_page):
    date_input = booking_page.find(*booking_page.DATE_INPUT)
    min_date = date_input.get_attribute("min")
    booking_page.screen(SCREENSHOT_DIR, "TC9_min_date_disabled.png")
    assert min_date == datetime.today().strftime("%Y-%m-%d")


def test_tc10_input_past_date(booking_page):
    past_date = (datetime.today() + timedelta(days=-1)).strftime("%Y-%m-%d")
    booking_page.set_value("dateSelectedValue", past_date)
    time.sleep(1)
    current_value = booking_page.get_date_value()
    booking_page.screen(SCREENSHOT_DIR, "TC10_input_past_date.png")
    assert current_value != past_date


def test_tc11_empty_start_time(booking_page, popup):
    start, end = BOOKING_CASES["empty_start_time"]
    booking_page.select_booking_info(start_time=start, end_time=end)
    booking_page.open_popup()
    booking_page.screen(SCREENSHOT_DIR, "TC11_empty_start_time.png")
    assert popup.is_visible() == False


def test_tc12_empty_end_time(booking_page, popup):
    start , end = BOOKING_CASES["empty_end_time"]
    booking_page.select_booking_info(start_time=start,end_time= end)
    booking_page.screen(SCREENSHOT_DIR, "TC12_empty_end_time.png")
    # end_current_value = booking_page.get_end_time_value()
    assert booking_page.get_end_time_value()


def test_tc13_end_time_smaller_than_start(booking_page):
    start, end = BOOKING_CASES["end_smaller_than_start"]
    booking_page.select_booking_info(start_time= start, end_time= end)
    time.sleep(1)
    actual_start = datetime.strptime(booking_page.get_start_time_value(), "%H:%M")
    actual_end = datetime.strptime(booking_page.get_end_time_value(), "%H:%M")
    diff_hours = (actual_end - actual_start).total_seconds() / 3600
    booking_page.screen(SCREENSHOT_DIR, "TC13_end_smaller_than_start.png")
    assert actual_end >= actual_start
    assert diff_hours >= 1


def test_tc14_start_time_smaller_than_current(booking_page, popup):
    date, start, end = BOOKING_CASES["start_smaller_than_current"]
    booking_page.select_booking_info(date=date, start_time= start, end_time=end)
    booking_page.open_popup()
    time.sleep(1)
    popup.confirm_booking()
    time.sleep(1)
    alert = popup.get_text_alert()
    booking_page.screen(SCREENSHOT_DIR, "TC14_start_time_smaller_than_current.png")
    assert "Giờ bắt đầu phải lớn hơn thời gian hiện tại" in alert


def test_tc15_outside_business_hours(booking_page, popup):
    start, end = booking_page.get_outside_time()
    booking_page.select_booking_info(start_time=start,end_time=end)
    booking_page.open_popup()
    popup.confirm_booking()
    alert = popup.get_text_alert()
    booking_page.screen(SCREENSHOT_DIR, "TC15_outside_business_hours.png")
    assert "Khung giờ không hoạt động" in alert


def test_tc16_duplicate_booking(booking_page, popup):
    url = booking_page.get_url()
    booking_page.scroll()
    start, end = booking_page.fill_booking(slot_index=BOOKING_CASES["duplicate_slot_index"])
    booking_page.open_popup()
    popup.confirm_booking()
    popup.get_text_alert()
    time.sleep(2)
    booking_page.driver.get(url)
    time.sleep(1)
    booking_page.select_booking_info(start_time=start, end_time=end)
    booking_page.open_popup()
    popup.confirm_booking()
    alert = popup.get_text_alert()
    booking_page.screen(SCREENSHOT_DIR, "TC16_duplicate_booking.png")
    assert "Khung giờ này đã có người đặt" in alert