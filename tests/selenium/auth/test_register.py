import pytest , time, os
from tests.selenium.pages.RegisterPage import RegisterPage
from  tests.test_base import driver,test_app

SCREENSHOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "screenshots" ,"register")

@pytest.fixture
def register_page(driver):
    page = RegisterPage(driver=driver)
    page.open_page()
    return page

def check_contains(text_list, expected):
    return any(expected in t for t in text_list)

def test_register_valid(register_page):
    register_page.register("user01","Aa@123456", "Aa@123456")
    time.sleep(1)
    results = register_page.result()
    register_page.screen(SCREENSHOT_DIR,"TC1_valid.png")
    assert check_contains(results, "Đăng ký thành công")


def test_register_empty_username(register_page):
    register_page.register("", "Aa@123456", "Aa@123456")
    time.sleep(1)
    username_input = register_page.find(*register_page.USERNAME_INPUT)
    msg = register_page.driver.execute_script("return arguments[0].validationMessage;", username_input)
    register_page.screen(SCREENSHOT_DIR,"TC2_empty_username.png")
    assert msg != ""


def test_register_username_space(register_page):
    register_page.register("us er02", "Aa@123456", "Aa@123456")
    time.sleep(1)
    results = register_page.result()
    register_page.screen(SCREENSHOT_DIR,"TC3_username_space.png")
    assert check_contains(results, "Tên người dùng không được chứa khoảng trắng")


def test_register_username_too_long(register_page):
    username = "a" * 31
    register_page.register(username, "Aa@123456", "Aa@123456")
    time.sleep(1)
    results = register_page.result()
    register_page.screen(SCREENSHOT_DIR,"TC4_username_too_long.png")
    assert check_contains(results, "Tên người dùng phải từ 3-30 ký tự")


def test_register_username_too_short(register_page):
    register_page.register("us", "Aa@123456", "Aa@123456")
    time.sleep(1)
    results = register_page.result()
    register_page.screen(SCREENSHOT_DIR,"TC5_username_too_short.png")
    assert check_contains(results, "Tên người dùng phải từ 3-30 ký tự")


def test_register_duplicate_username(register_page):
    register_page.register("user01", "Aa@123456", "Aa@123456")
    time.sleep(1)
    results = register_page.result()
    register_page.screen(SCREENSHOT_DIR,"TC6_duplicate_username.png")
    assert check_contains(results, "Tên người dùng đã tồn tại")


def test_register_empty_password(register_page):
    register_page.register("user02", "", "Aa@123456")
    time.sleep(1)
    password_input = register_page.find(*register_page.PASSWORD_INPUT)
    msg = register_page.driver.execute_script("return arguments[0].validationMessage;", password_input)
    register_page.screen(SCREENSHOT_DIR,"TC7_empty_password.png")
    assert msg != ""


def test_register_password_missing_uppercase(register_page):
    register_page.register("user02", "aa@123456", "aa@123456")
    time.sleep(1)
    results = register_page.result()
    register_page.screen(SCREENSHOT_DIR,"TC8_missing_uppercase.png")
    assert check_contains(results, "Mật khẩu phải chứa ký tự hoa")


def test_register_password_missing_lowercase(register_page):
    register_page.register("user02", "AA@123456", "AA@123456")
    time.sleep(1)
    results = register_page.result()
    register_page.screen(SCREENSHOT_DIR,"TC9_missing_lowercase.png")

    assert check_contains(results, "Mật khẩu phải chứa ký tự thường")


def test_register_password_missing_number(register_page):
    register_page.register("user02", "Aa@aaaaa", "Aa@aaaaa")
    time.sleep(1)
    results = register_page.result()
    register_page.screen(SCREENSHOT_DIR,"TC10_missing_number.png")
    assert check_contains(results, "Mật khẩu phải chứa số")


def test_register_password_missing_special(register_page):
    register_page.register("user02", "Aaa123456", "Aaa123456")
    time.sleep(1)
    results = register_page.result()
    register_page.screen(SCREENSHOT_DIR,"TC11_missing_special.png")
    assert check_contains(results, "Mật khẩu phải chứa ký tự đặc biệt")


def test_register_password_space(register_page):
    register_page.register("user02", " Aa@123456", " Aa@123456")
    time.sleep(1)
    results = register_page.result()
    register_page.screen(SCREENSHOT_DIR,"TC12_password_space.png")
    assert check_contains(results, "Mật khẩu không được chứa khoảng trắng")


def test_register_password_too_short(register_page):
    register_page.register("user02", "Aa@123", "Aa@123")
    time.sleep(1)
    results = register_page.result()
    register_page.screen(SCREENSHOT_DIR,"TC13_password_too_short.png")
    assert check_contains(results, "Mật khẩu phải từ 8-30 ký tự")


def test_register_password_too_long(register_page):
    password = "A" + ("a" * 20) + "@0123456789"
    register_page.register("user02", password, password)
    time.sleep(1)
    results = register_page.result()
    register_page.screen(SCREENSHOT_DIR,"TC14_password_too_long.png")
    assert check_contains(results, "Mật khẩu phải từ 8-30 ký tự")


def test_register_empty_confirm(register_page):
    register_page.register("user02", "Aa@123456", "")
    time.sleep(1)
    confirm_input = register_page.find(*register_page.COMFIRM_INPUT)
    msg = register_page.driver.execute_script("return arguments[0].validationMessage;", confirm_input)
    register_page.screen(SCREENSHOT_DIR,"TC15_empty_confirm.png")
    assert msg != ""


def test_register_confirm_not_match(register_page):
    register_page.register("user02", "Aa@123456", "Aacde123")
    time.sleep(1)
    results = register_page.result()
    register_page.screen(SCREENSHOT_DIR,"TC16_confirm_not_match.png")
    assert check_contains(results, "Mật khẩu nhập lại không khớp")


def test_register_all_invalid(register_page):
    register_page.register("ue 01", "A@123456", "Aa@123")
    time.sleep(1)
    results = register_page.result()
    register_page.screen(SCREENSHOT_DIR,"TC17_all_invalid.png")
    assert check_contains(results, "Mật khẩu phải chứa ký tự thường")
    assert check_contains(results, "Tên người dùng không được chứa khoảng trắng")