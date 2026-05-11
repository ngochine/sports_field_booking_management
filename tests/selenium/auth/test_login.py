import pytest , time, os
from tests.selenium.pages.LoginPage import LoginPage
from  tests.test_base import driver,test_app

SCREENSHOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "screenshots", "login")

def check_contains(text_list, expected):
    return any(expected in t for t in text_list)

@pytest.fixture
def login_page(driver):
    page = LoginPage(driver=driver)
    page.open_page()
    return page

def test_login_valid(login_page):
    login_page.login("user01", "Aa@123456")
    time.sleep(1)
    login_page.screen(SCREENSHOT_DIR, "TC1_login_valid.png")
    assert "login" not in login_page.driver.current_url


def test_login_user_not_exist(login_page):
    login_page.login("user08", "Aa@123456")
    time.sleep(1)
    results = login_page.result()
    login_page.screen(SCREENSHOT_DIR, "TC2_user_not_exist.png")
    assert check_contains(results, "Sai tài khoản hoặc mật khẩu")


def test_login_empty_username(login_page):
    login_page.login("", "Aa@123456")
    time.sleep(1)
    username_input = login_page.find(*login_page.USERNAME_INPUT)
    msg = login_page.driver.execute_script("return arguments[0].validationMessage;", username_input)
    login_page.screen(SCREENSHOT_DIR, "TC3_empty_username.png")
    assert msg != ""


def test_login_empty_password(login_page):
    login_page.login("user01", "")
    time.sleep(1)
    password_input = login_page.find(*login_page.PASSWORD_INPUT)
    msg = login_page.driver.execute_script("return arguments[0].validationMessage;", password_input)
    login_page.screen(SCREENSHOT_DIR, "TC4_empty_password.png")
    assert msg != ""


def test_login_wrong_password(login_page):
    login_page.login("user01", "Aa@678912")
    time.sleep(1)
    results = login_page.result()
    login_page.screen(SCREENSHOT_DIR, "TC5_wrong_password.png")
    assert check_contains(results, "Sai tài khoản hoặc mật khẩu")


def test_login_wrong_user_and_password(login_page):
    login_page.login("us", "Aa@678912")
    time.sleep(1)
    results = login_page.result()
    login_page.screen(SCREENSHOT_DIR, "TC6_wrong_both.png")
    assert check_contains(results, "Sai tài khoản hoặc mật khẩu")