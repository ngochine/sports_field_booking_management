import time, os, pytest
from datetime import datetime, timedelta
from tests.selenium.data.booking_data import BOOKING_CASES
from tests.test_base import driver, test_app, driver2
from tests.selenium.fixture import detail_page, guest_detail_page,detail_page_2
from tests.selenium.locators.DetailFieldLocators import BookingInfoLocators



def test_tc1_booking_without_login(guest_detail_page):
    guest_detail_page.scroll()
    guest_detail_page.fill_booking(slot_index=1)
    guest_detail_page.open_popup()
    guest_detail_page.confirm_booking()
    alert = guest_detail_page.get_text_alert()
    guest_detail_page.screen_booking("TC1_booking_without_login.png")
    assert "Vui lòng đăng nhập để thực hiện chức năng này" in alert


def test_tc2_total_price_same_slot(detail_page):
    start, end = detail_page.fill_booking()
    total_price = int(detail_page.get_total_price())
    expected_price = detail_page.get_price_by_time(start, end)
    detail_page.screen_booking("TC2_total_price_same_slot.png")
    assert total_price == int(expected_price)


def test_tc3_total_price_multi_slot(detail_page):
    start, end = detail_page.get_adjacent_slots_time()
    detail_page.select_booking_info(start_time=start,end_time=end)
    total_price = int(detail_page.get_total_price())
    expected_price = detail_page.calculate_price_multi_slot(start,end)
    detail_page.screen_booking("TC3_total_price_multi_slot.png")
    assert total_price == int(expected_price)


def test_tc4_update_total_price_when_change_time(detail_page):
    start, end = detail_page.fill_booking()
    old_price = detail_page.get_total_price()
    new_end = (
        datetime.strptime(end, "%H:%M") - timedelta(hours=1)
    ).strftime("%H:%M")
    detail_page.select_booking_info(start_time=start,end_time=new_end)
    time.sleep(1)
    new_price = detail_page.get_total_price()
    detail_page.screen_booking("TC4_update_total_price.png")
    assert old_price != new_price


def test_tc5_verify_popup_info(detail_page):
    field_name = detail_page.get_field_name()
    address = detail_page.get_address()
    detail_page.scroll()
    detail_page.fill_booking()
    detail_page.open_popup()
    assert detail_page.is_visible()
    errors = detail_page.verify_confirm_info(
        field_name=field_name,
        address=address,
        date=BOOKING_CASES["default_day"],
        start_time=detail_page.get_start_time_value(),
        end_time=detail_page.get_end_time_value(),
        total_duration=detail_page.get_total_time(),
        total_price=int(detail_page.get_total_price()),
    )
    detail_page.screen_booking("TC5_verify_popup_info.png")
    assert errors == []


def test_tc6_valid_booking(detail_page):
    current_url = detail_page.get_url()
    detail_page.fill_booking(slot_index=BOOKING_CASES["booking_slot_index"])
    detail_page.open_popup()
    detail_page.confirm_booking()
    alert = detail_page.get_text_alert()
    time.sleep(1)
    detail_page.screen_booking("TC6_valid_booking.png")
    assert "Đặt sân thành công! Vui lòng vào 'Lịch sử đặt sân' để thanh toán trong 15 phút" in alert
    assert current_url != detail_page.get_url()


def test_tc7_cancel_popup(detail_page):
    current_url = detail_page.get_url()
    detail_page.fill_booking()
    detail_page.open_popup()
    detail_page.cancel_popup()
    time.sleep(0.5)
    detail_page.screen_booking("TC7_cancel_popup.png")
    assert current_url == detail_page.get_url()
    # assert detail_page.is_visible()


def test_tc8_close_popup_x(detail_page):
    current_url = detail_page.get_url()
    detail_page.fill_booking()
    detail_page.open_popup()
    detail_page.close_popup()
    time.sleep(0.5)
    detail_page.screen_booking("TC8_close_popup_x.png")
    assert current_url == detail_page.get_url()


def test_tc9_empty_date(detail_page):
    detail_page.fill_booking(date="")
    detail_page.screen_booking("TC9_empty_date.png")
    assert not detail_page.is_enabled(*BookingInfoLocators.BOOK_BUTTON)


def test_tc10_disable_past_date(detail_page):
    date_input = detail_page.find(*BookingInfoLocators.DATE_INPUT)
    min_date = date_input.get_attribute("min")
    detail_page.screen_booking("TC10_disable_past_date.png")
    assert min_date == datetime.today().strftime("%Y-%m-%d")


def test_tc11_input_past_date(detail_page):
    past_date = BOOKING_CASES["past_date"]
    detail_page.set_value(BookingInfoLocators.DATE_INPUT[1],past_date)
    time.sleep(1)
    alert = detail_page.get_text_alert()
    detail_page.scroll(400)
    time.sleep(1)
    current_value = detail_page.get_date_value()
    detail_page.screen_booking("TC11_input_past_date.png")
    assert "Không được chọn ngày ở quá khứ" in alert
    assert current_value != past_date
    assert current_value == detail_page.get_date_min()


def test_tc12_invalid_date(detail_page):
    detail_page.set_value(BookingInfoLocators.DATE_INPUT[1],"2025-99-99")
    time.sleep(1)
    current_value = detail_page.get_date_value()
    detail_page.screen_booking("TC12_invalid_date.png")
    assert current_value != "2025-99-99"
    assert current_value == detail_page.get_date_min()


def test_tc13_empty_start_time(detail_page):
    start, end = BOOKING_CASES["empty_start_time"]
    detail_page.select_booking_info(start_time=start,end_time=end)
    detail_page.screen_booking("TC13_empty_start_time.png")
    assert not detail_page.is_enabled(*BookingInfoLocators.BOOK_BUTTON)


def test_tc14_auto_fill_end_time(detail_page):
    detail_page.select_booking_info(start_time="13:00",end_time="")
    end_time = detail_page.get_end_time_value()
    detail_page.screen_booking("TC14_auto_fill_end_time.png")
    assert end_time != ""
    assert detail_page.space_time() >=1


def test_tc15_end_time_smaller_than_start(detail_page):
    start, end = BOOKING_CASES["end_smaller_than_start"]
    detail_page.select_booking_info(start_time=start,end_time=end)
    detail_page.screen_booking("TC15_end_time_smaller_than_start.png")
    assert detail_page.space_time() >= 1


def test_tc16_start_time_smaller_current(detail_page):
    detail_page.select_booking_info(*BOOKING_CASES["start_smaller_than_current"])
    detail_page.screen_booking("TC16_start_time_smaller_current.png")
    if detail_page.is_enabled(*BookingInfoLocators.BOOK_BUTTON):
        detail_page.open_popup()
        detail_page.confirm_booking()
        alert = detail_page.get_text_alert()
        assert "Phải đặt sân trước ít nhất 1 tiếng" in alert
    else:
        assert "Sân hiện không phục vụ trong khung giờ bạn chọn." in detail_page.get_err()


def test_tc17_invalid_time_input(detail_page):
    start, end = BOOKING_CASES["invalid_time"]
    detail_page.select_booking_info(start_time=start,end_time=end)
    detail_page.screen_booking("TC17_invalid_time_input.png")
    assert detail_page.get_start_time_value() != "aa:00"
    assert detail_page.get_end_time_value() != "-1:00"


def test_tc18_booking_under_one_hour(detail_page):
    detail_page.fill_part_booking()
    detail_page.screen_booking("TC18_booking_under_one_hour.png")
    assert detail_page.space_time() >= 1


def test_tc19_outside_business_hours(detail_page):
    start,end=detail_page.get_outside_time()
    detail_page.select_booking_info(start_time=start,end_time=end)
    detail_page.screen_booking("TC19_outside_business_hours.png")
    assert "Sân hiện không phục vụ trong khung giờ bạn chọn." in detail_page.get_err()
    assert not detail_page.is_enabled(*BookingInfoLocators.BOOK_BUTTON)


def test_tc20_duplicate_booking(detail_page):
    current_url = detail_page.get_url()
    start, end = detail_page.fill_booking()
    detail_page.open_popup()
    detail_page.confirm_booking()
    detail_page.get_text_alert()
    time.sleep(2)
    detail_page.driver.get(current_url)
    detail_page.select_booking_info(start_time=start,end_time=end)
    detail_page.open_popup()
    detail_page.confirm_booking()
    alert = detail_page.get_text_alert()
    detail_page.screen_booking("TC20_duplicate_booking.png")
    assert "Khung giờ đặt bị trùng" in alert


def test_tc21_partial_overlap_booking(detail_page):
    current_url = detail_page.get_url()
    date = detail_page.plus_date(18)
    start, end = detail_page.part_time(date=date)
    detail_page.open_popup()
    detail_page.confirm_booking()
    detail_page.get_text_alert()
    time.sleep(2)
    detail_page.driver.get(current_url)
    detail_page.select_booking_info(
        date=date,
        start_time=start,
        end_time=detail_page.add_hours(end,1)
    )
    detail_page.open_popup()
    detail_page.confirm_booking()
    alert = detail_page.get_text_alert()
    detail_page.screen_booking("TC21_partial_overlap_booking.png")
    assert "Khung giờ đặt bị trùng" in alert


def test_tc22_concurrent_booking(detail_page,detail_page_2):
    page1 = detail_page
    page2 = detail_page_2
    current_url = page1.get_url()
    page2.driver.get(current_url)
    start, end = page1.fill_booking(date=page1.plus_date(57))
    page1.open_popup()
    page2.select_booking_info(date=page2.plus_date(57), start_time=start,end_time=end)
    page2.open_popup()
    page1.confirm_booking()
    alert1 = page1.get_text_alert()
    page1.screen_booking("TC22_concurrent_booking_1.png")
    page2.confirm_booking()
    alert2 = page2.get_text_alert()
    page2.screen_booking("TC22_concurrent_booking_2.png")
    assert "Đặt sân thành công" in alert1
    assert "Khung giờ đặt bị trùng" in alert2



def test_tc23_cross_day_booking(detail_page):
    detail_page.select_booking_info(start_time="23:30",end_time="00:30")
    detail_page.screen_booking("TC23_cross_day_booking.png")
    assert "Không được đặt qua ngày" in detail_page.get_err()
    assert not detail_page.is_enabled(*BookingInfoLocators.BOOK_BUTTON)


def test_tc24_booking_three_times(detail_page):
    page= detail_page
    current_url = page.get_url()
    for i in range(3):
        page.fill_booking(date=page.plus_date(i+21))
        page.open_popup()
        page.confirm_booking()
        page.get_text_alert()
        time.sleep(1)
        if i==2:
            page.screen_booking("TC24_booking_three_times.png")
        page.driver.get(current_url)
    assert True


def test_tc25_booking_fourth_time(detail_page):
    page= detail_page
    current_url = page.get_url()
    alert =""
    for i in range(4):
        page.fill_booking(date=page.plus_date(i+10))
        page.open_popup()
        page.confirm_booking()
        time.sleep(1)
        alert=page.get_text_alert()
        time.sleep(1)
        if i==3:
            page.screen_booking("TC25_booking_fourth_time.png")
        page.driver.get(current_url)
    assert "Tài khoản đã đạt giới hạn đặt trong ngày (3 lần/ngày)" in alert


def test_tc26_booking_field_not_found(detail_page):
    detail_page.open('/field/999999')
    detail_page.screen_booking("TC26_booking_field_not_found.png")
    assert "404" in detail_page.driver.page_source


def test_tc27_double_click_booking(detail_page):
    detail_page.fill_booking(date=detail_page.plus_date(184))
    detail_page.double_click_booking()
    assert detail_page.count_popup() == 1
    detail_page.double_confirm_booking()
    alert = detail_page.get_text_alert()
    if detail_page.count_alert() ==1:
        time.sleep(1)
        assert "Đặt sân thành công" in detail_page.get_text_alert()
        detail_page.screen_booking("TC27_double_click_booking.png")
        assert detail_page.count_alert() == 0
    else :
        assert "Khung giờ đặt bị trùng" in alert
        detail_page.screen_booking("TC27_double_click_booking.png")

def test_tc29_role_denied(detail_page):
    detail_page.fill_booking(slot_index=BOOKING_CASES["booking_slot_index"])
    detail_page.open_popup()
    detail_page.confirm_booking()
    alert = detail_page.get_text_alert()
    time.sleep(1)
    detail_page.screen_booking("TC29_role_denied.png")
    assert "Tài khoản của bạn không đủ quyền để thực hiện hành động này" in alert

