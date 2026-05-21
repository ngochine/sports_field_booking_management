import time
from datetime import datetime, timedelta
from tests.selenium.data.booking_data import CANCEL_CASE
from tests.selenium.pages.DetailBookingPage import DetailBookingPage
from tests.selenium.pages.HistoryPage import HistoryPage
from tests.selenium.fixture import cancel_history_page, open_detail_page, login, register_login
from tests.selenium.locators.HistoryLocators import HistoryLocators
from tests.test_base import driver,test_app,driver2


def create_booking(driver, hours_before, minutes_before=0):
    detail_page = open_detail_page(driver=driver)
    booking_time = (datetime.now().replace(second=0, microsecond=0)+ timedelta(hours=hours_before, minutes=minutes_before))
    detail_page.select_booking_info(
        date=booking_time.strftime("%Y-%m-%d"),
        start_time=booking_time.strftime("%H:%M"),
        end_time=(booking_time + timedelta(hours=1)).strftime("%H:%M")
    )
    time.sleep(1)
    detail_page.open_popup()
    booking_info = detail_page.get_booking_popup_info()
    detail_page.confirm_booking()
    alert = detail_page.get_text_alert()
    assert "Đặt sân thành công!" in alert
    return booking_info



def test_tc1_cancel_booking_success(driver):
    driver = login(driver=driver,username=CANCEL_CASE["valid_user"][0],password=CANCEL_CASE["valid_user"][1])
    booking_info = create_booking(driver, 2, 20)
    history_page = HistoryPage(driver)
    history_page.open_page()
    time.sleep(1)
    el = history_page.find_booking_by_info(booking_info)
    old_status = history_page.get_status_booking(el)
    history_page.click_cancel(el)
    time.sleep(1)
    history_page.confirm_cancel_booking()
    success_msg = history_page.get_text_alert()
    assert "Huỷ sân thành công!" in success_msg
    updated = history_page.find_booking_by_info(booking_info)
    assert history_page.get_status_booking(updated) == "Đã huỷ"
    assert history_page.get_status_booking(updated) != old_status
    history_page.screen_cancel("TC1_cancel_booking_success.png")



def test_tc2_cancel_booking_exactly_2_hours_before(driver):
    driver = login(driver=driver,username=CANCEL_CASE["valid_user"][0],password=CANCEL_CASE["valid_user"][1])
    while datetime.now().second != 0:
        time.sleep(0.2)
    booking_info = create_booking(driver, 2, 1)
    booking_datetime = datetime.strptime(
        f'{booking_info["booking_date"]} {booking_info["time_range"].split("-")[0].strip()}',
        "%d/%m/%Y %H:%M:%S"
    )
    history_page = HistoryPage(driver)
    history_page.open_page()
    el = history_page.find_booking_by_info(booking_info)
    old_status = history_page.get_status_booking(el)
    assert old_status != "Đã hủy"
    history_page.click_cancel(el)
    target_time = booking_datetime - timedelta(hours=2)
    wait_seconds = (target_time - datetime.now()).total_seconds() - 1
    if wait_seconds > 0:
        time.sleep(wait_seconds)
    history_page.confirm_cancel_booking()
    success_msg = history_page.get_text_alert()
    assert "Huỷ sân thành công!" in success_msg
    updated = history_page.find_booking_by_info(booking_info)
    assert history_page.get_status_booking(updated) == "Đã huỷ"
    history_page.screen_cancel("TC2_cancel_booking_exactly_2_hours_before.png")


def test_tc3_cannot_cancel_booking_under_2_hours(driver):
    driver = login(driver=driver,username=CANCEL_CASE["valid_user"][0],password=CANCEL_CASE["valid_user"][1])
    booking_info = create_booking(driver, 1, 30)
    history_page = HistoryPage(driver)
    history_page.open_page()
    el = history_page.find_booking_by_info(booking_info)
    old_status = history_page.get_status_booking(el)
    history_page.click_cancel(el)
    history_page.confirm_cancel_booking()
    error_msg = history_page.get_text_alert()
    assert "Không được huỷ khi còn dưới 2 giờ trước giờ chơi" in error_msg
    updated = history_page.find_booking_by_info(booking_info)
    assert history_page.get_status_booking(updated) == old_status
    history_page.screen_cancel("TC3_cannot_cancel_booking_under_2_hours.png")


def test_tc4_cancel_popup_info_all_bookings(cancel_history_page):
    bookings = cancel_history_page.get_cancelable_bookings()
    assert len(bookings) > 0
    current_page = bookings[0]["page"]
    cancel_history_page.go_to_page(current_page)
    for item in bookings:
        if current_page != item["page"]:
            current_page = item["page"]
            cancel_history_page.go_to_page(current_page)
        time.sleep(1)
        booking_elements = cancel_history_page.finds(*HistoryLocators.BOOKING_CARD)
        el = booking_elements[item["index"]]
        time.sleep(0.5)
        cancel_history_page.click_cancel(el)
        time.sleep(1)
        cancel_history_page.assert_popup_matches(el)
        cancel_history_page.close_cancel_popup()
        assert cancel_history_page.get_status_booking(el) in ["Chờ thanh toán", "Đã thanh toán"]
    cancel_history_page.screen_cancel("TC4_cancel_popup_info_all_bookings.png")


def test_tc6_cancel_booking_server_disconnect(driver):
    driver = login(driver, CANCEL_CASE["valid_user"][0], CANCEL_CASE["valid_user"][1])
    booking_info = create_booking(driver, 3)
    history_page = HistoryPage(driver)
    history_page.open_page()
    el = history_page.find_booking_by_info(booking_info)
    old_status = history_page.get_status_booking(el)
    history_page.click_cancel(el)
    time.sleep(1)
    driver.execute_cdp_cmd("Network.enable", {})
    driver.execute_cdp_cmd("Network.emulateNetworkConditions", {
        "offline": True,
        "latency": 0,
        "downloadThroughput": 0,
        "uploadThroughput": 0
    })
    history_page.confirm_cancel_booking()
    time.sleep(2)
    error_msg = history_page.get_text_alert()
    assert "lỗi kết nối" in error_msg.lower() or "failed" in error_msg.lower()
    updated = history_page.find_booking_by_info(booking_info)
    assert history_page.get_status_booking(updated) == old_status
    driver.execute_cdp_cmd("Network.emulateNetworkConditions", {
        "offline": False,
        "latency": 0,
        "downloadThroughput": -1,
        "uploadThroughput": -1
    })
    history_page.open_page()
    history_page.screen_cancel("TC6_cancel_booking_network_offline.png")


def test_tc7_double_click_cancel_booking(driver):
    driver = login(driver, CANCEL_CASE["valid_user"][0], CANCEL_CASE["valid_user"][1])
    booking_info = create_booking(driver, 9)
    history_page = HistoryPage(driver)
    history_page.open_page()
    el = history_page.find_booking_by_info(booking_info)
    old_status = history_page.get_status_booking(el)
    history_page.click_cancel(el)
    time.sleep(1)
    history_page.double_click_cancel()
    msg = history_page.get_text_alert()
    msg2 = history_page.get_text_alert()
    if "Huỷ sân thành công!" in msg2:
        history_page.screen_cancel("TC8_double_click_cancel.png")
        assert False
    assert "Huỷ sân thành công!" in msg
    updated = history_page.find_booking_by_info(booking_info)
    new_status = history_page.get_status_booking(updated)
    assert new_status == "Đã hủy"
    assert new_status != old_status
    history_page.screen_cancel("TC8_double_click_cancel.png")

def test_tc8_cannot_cancel_other_user_booking(driver,driver2):
    driver = register_login(driver=driver)
    booking_info = create_booking(driver, 3)
    history_page = HistoryPage(driver)
    history_page.open_page()
    el=history_page.find_booking_by_info(booking_info)
    old_status = history_page.get_status_booking(el)
    link=history_page.get_link(el)
    driver2 = register_login(driver=driver2)
    detail_page= DetailBookingPage(driver2)
    detail_page.open_not_base(link)
    time.sleep(1)
    detail_page.scroll(8000)
    time.sleep(1)
    detail_page.click_cancel()
    alert = detail_page.get_text_alert()
    assert "không có quyền" in alert
    history_page.open_page()
    updated = history_page.find_booking_by_info(booking_info)
    new_status = history_page.get_status_booking(updated)
    assert new_status == old_status
    history_page.screen_cancel("TC8_no_permission_cancel.png")

from tests.selenium.pages.HistoryPage import HistoryPage
from tests.selenium.fixture import login
from tests.selenium.data.booking_data import CANCEL_CASE


def test_tc9_cancel_booking_not_exist(driver):
    driver = login(driver, CANCEL_CASE["valid_user"][0], CANCEL_CASE["valid_user"][1])
    detail_page = DetailBookingPage(driver)
    detail_page.open('/booking/999999')
    detail_page.screen_cancel("TC9_cancel_nonexistent_booking.png")
    assert "404" in detail_page.driver.page_source


def test_tc10_cancel_booking_multi_tab(driver,driver2):
    driver,account= register_login(driver=driver,get_account=True)
    booking_info = create_booking(driver, 18)
    history_page = HistoryPage(driver)
    history_page.open_page()
    el=history_page.find_booking_by_info(booking_info)
    old_status = history_page.get_status_booking(el)
    link=history_page.get_link(el)
    detail_tab1 = DetailBookingPage(driver=driver)
    detail_tab1.open_not_base(link)
    driver2 = login(driver=driver2,username=account["username"],password=account["password"])
    detail_tab2 = DetailBookingPage(driver=driver2)
    detail_tab2.open_not_base(link)
    time.sleep(1)
    detail_tab1.scroll(8000)
    time.sleep(1)
    detail_tab1.click_cancel()
    alert1 = detail_tab1.get_text_alert()
    assert "Huỷ sân thành công!" in alert1
    time.sleep(1)
    detail_tab2.scroll(8000)
    time.sleep(1)
    detail_tab2.click_cancel()
    alert2 = detail_tab2.get_text_alert()
    print(alert2)
    assert "Chỉ được huỷ khi booking có trạng thái PENDING hoặc PAID" in alert2
    driver.switch_to.window(driver.window_handles[0])
    history_page.open_page()
    updated = history_page.find_booking_by_info(booking_info)
    new_status = history_page.get_status_booking(updated)
    assert new_status != old_status
    assert "Đã hủy" in new_status
    history_page.screen_cancel("TC10_multi_tab_cancel.png")

