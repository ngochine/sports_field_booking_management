import time
import pytest

from tests.selenium.data.booking_data import CANCEL_CASE
from tests.selenium.pages.HistoryPage import HistoryPage
from tests.selenium.locators.HistoryLocators import HistoryLocators,BookingCardLocators
from tests.test_base import driver,test_app,driver2
from tests.selenium.fixture import history_page, login, cancel_history_page


def filter(cancel_history_page,name="",count_cancel=0,count_detail=0,count_pay=0):
    select = cancel_history_page.find(*HistoryLocators.FILTER_SELECT)
    select.send_keys(name)
    time.sleep(1)
    cards = cancel_history_page.get_all_bookings()
    assert len(cards) > 0
    for el in cards:
        assert el["field_name"] != ""
        assert el["status"] == name
        assert el["cancel_buttons"] == count_cancel
        assert el["detail_buttons"] == count_detail
        assert el["pay_buttons"] == count_pay

def test_tc1_history_without_login(driver):
    page = HistoryPage(driver)
    page.open_page()
    time.sleep(1)
    cards = page.get_cards()
    assert len(cards) == 0
    assert "bookings" not in page.get_url()
    page.screen_history("TC1_history_without_login.png")


def test_tc2_user_no_booking(history_page):
    cards = history_page.get_cards()
    assert len(cards) == 0
    assert "Bạn chưa đặt sân nào!" in history_page.get_text("tag name","body")
    history_page.screen_history("TC2_user_no_booking.png")


def test_tc3_pagination(cancel_history_page):
    current_url = cancel_history_page.get_url()
    assert cancel_history_page.has_next_page()
    cancel_history_page.go_to_next_page()
    time.sleep(1)
    assert current_url != cancel_history_page.get_url()
    assert "2" in cancel_history_page.get_url()
    cancel_history_page.screen_history("TC3_pagination.png")


def test_tc4_booking_information(cancel_history_page):
    bookings = cancel_history_page.get_all_bookings()
    assert len(bookings) > 0
    for booking in bookings:
        assert booking["field_name"] != ""
        assert booking["booking_date"] != ""
        assert booking["time_range"] != ""
        assert booking["price"] != ""
        assert booking["status"] != ""
    cancel_history_page.screen_history("TC4_booking_information.png")


def test_tc5_filter_all_status(cancel_history_page):
    page = cancel_history_page
    filter_select = page.find(*HistoryLocators.FILTER_SELECT)
    assert filter_select.get_attribute("value") != ""
    bookings = page.get_all_bookings()
    assert len(bookings) > 0
    for booking in bookings:
        assert booking["field_name"] != ""
        assert booking["status"] != ""
    page.screen_history("TC5_filter_all_status.png")


def test_tc6_filter_paid(cancel_history_page):
    filter(cancel_history_page,name="Đã thanh toán",count_cancel=1,count_detail=1,count_pay=0)
    cancel_history_page.screen_history("TC6_filter_paid.png")


def test_tc7_filter_pending(cancel_history_page):
    filter(cancel_history_page, name="Chờ thanh toán", count_cancel=1, count_detail=1, count_pay=1)
    cancel_history_page.screen_history("TC7_filter_pending.png")


def test_tc8_filter_cancelled(cancel_history_page):
    filter(cancel_history_page, name="Đã hủy", count_cancel=0, count_detail=1, count_pay=0)
    cancel_history_page.screen_history("TC8_filter_cancelled.png")