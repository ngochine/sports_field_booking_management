import time, os
from  tests.test_base import driver,test_app
from tests.selenium.guest_fixture import register_page
from tests.selenium.data.user_data import REGISTER_USERS
from tests.selenium.locators.RegisterLocators import RegisterLocators


def check_contains(text_list, expected):
    return any(expected in t for t in text_list)


def test_register_valid(register_page):
    username, password, confirm = REGISTER_USERS["valid"]
    register_page.register(username, password, confirm)
    time.sleep(1)
    results = register_page.result()
    register_page.screen_register("TC1_valid.png")
    assert check_contains(results, "Đăng ký thành công")


def test_register_empty_username(register_page):
    username, password, confirm = REGISTER_USERS["empty_username"]
    register_page.register(username, password, confirm)
    time.sleep(1)
    username_input = register_page.find(*RegisterLocators.USERNAME_INPUT)
    msg = register_page.driver.execute_script("return arguments[0].validationMessage;", username_input)
    register_page.screen_register("TC2_empty_username.png")
    assert msg != ""


def test_register_username_space(register_page):
    username, password, confirm = REGISTER_USERS["username_space"]
    register_page.register(username, password, confirm)
    time.sleep(1)
    results = register_page.result()
    register_page.screen_register("TC3_username_space.png")
    assert check_contains(results, "Tên người dùng không được chứa khoảng trắng")


def test_register_username_too_long(register_page):
    username, password, confirm = REGISTER_USERS["username_too_long"]
    register_page.register(username, password, confirm)
    time.sleep(1)
    results = register_page.result()
    register_page.screen_register("TC4_username_too_long.png")
    assert check_contains(results, "Tên người dùng phải từ 3-30 ký tự")


def test_register_username_too_short(register_page):
    username, password, confirm = REGISTER_USERS["username_too_short"]
    register_page.register(username, password, confirm)
    time.sleep(1)
    results = register_page.result()
    register_page.screen_register("TC5_username_too_short.png")
    assert check_contains(results, "Tên người dùng phải từ 3-30 ký tự")


def test_register_duplicate_username(register_page):
    username, password, confirm = REGISTER_USERS["duplicate_username"]
    register_page.register(username, password, confirm)
    time.sleep(1)
    results = register_page.result()
    register_page.screen_register("TC6_duplicate_username.png")
    assert check_contains(results, "Tên người dùng đã tồn tại")


def test_register_empty_password(register_page):
    username, password, confirm = REGISTER_USERS["empty_password"]
    register_page.register(username, password, confirm)
    time.sleep(1)
    password_input = register_page.find(*RegisterLocators.PASSWORD_INPUT)
    msg = register_page.driver.execute_script("return arguments[0].validationMessage;", password_input)
    register_page.screen_register("TC7_empty_password.png")
    assert msg != ""


def test_register_password_missing_uppercase(register_page):
    username, password, confirm = REGISTER_USERS["missing_uppercase"]
    register_page.register(username, password, confirm)
    time.sleep(1)
    results = register_page.result()
    register_page.screen_register("TC8_missing_uppercase.png")
    assert check_contains(results, "Mật khẩu phải chứa ký tự hoa")


def test_register_password_missing_lowercase(register_page):
    username, password, confirm = REGISTER_USERS["missing_lowercase"]
    register_page.register(username, password, confirm)
    time.sleep(1)
    results = register_page.result()
    register_page.screen_register("TC9_missing_lowercase.png")
    assert check_contains(results, "Mật khẩu phải chứa ký tự thường")


def test_register_password_missing_number(register_page):
    username, password, confirm = REGISTER_USERS["missing_number"]
    register_page.register(username, password, confirm)
    time.sleep(1)
    results = register_page.result()
    register_page.screen_register("TC10_missing_number.png")
    assert check_contains(results, "Mật khẩu phải chứa số")


def test_register_password_missing_special(register_page):
    username, password, confirm = REGISTER_USERS["missing_special"]
    register_page.register(username, password, confirm)
    time.sleep(1)
    results = register_page.result()
    register_page.screen_register("TC11_missing_special.png")
    assert check_contains(results, "Mật khẩu phải chứa ký tự đặc biệt")


def test_register_password_space(register_page):
    username, password, confirm = REGISTER_USERS["password_space"]
    register_page.register(username, password, confirm)
    time.sleep(1)
    results = register_page.result()
    register_page.screen_register("TC12_password_space.png")
    assert check_contains(results, "Mật khẩu không được chứa khoảng trắng")


def test_register_password_too_short(register_page):
    username, password, confirm = REGISTER_USERS["password_too_short"]
    register_page.register(username, password, confirm)
    time.sleep(1)
    results = register_page.result()
    register_page.screen_register("TC13_password_too_short.png")
    assert check_contains(results, "Mật khẩu phải từ 8-30 ký tự")


def test_register_password_too_long(register_page):
    username, password, confirm = REGISTER_USERS["password_too_long"]
    register_page.register(username, password, confirm)
    time.sleep(1)
    results = register_page.result()
    register_page.screen_register("TC14_password_too_long.png")
    assert check_contains(results, "Mật khẩu phải từ 8-30 ký tự")


def test_register_empty_confirm(register_page):
    username, password, confirm = REGISTER_USERS["empty_confirm"]
    register_page.register(username, password, confirm)
    time.sleep(1)
    confirm_input = register_page.find(*RegisterLocators.COMFIRM_INPUT)
    msg = register_page.driver.execute_script("return arguments[0].validationMessage;", confirm_input)
    register_page.screen_register("TC15_empty_confirm.png")
    assert msg != ""


def test_register_confirm_not_match(register_page):
    username, password, confirm = REGISTER_USERS["confirm_not_match"]
    register_page.register(username, password, confirm)
    time.sleep(1)
    results = register_page.result()
    register_page.screen_register("TC16_confirm_not_match.png")
    assert check_contains(results, "Mật khẩu nhập lại không khớp")


def test_register_all_invalid(register_page):
    username, password, confirm = REGISTER_USERS["all_invalid"]
    register_page.register(username, password, confirm)
    time.sleep(1)
    results = register_page.result()
    register_page.screen_register("TC17_all_invalid.png")
    assert check_contains(results, "Mật khẩu phải chứa ký tự thường")
    assert check_contains(results, "Tên người dùng không được chứa khoảng trắng")