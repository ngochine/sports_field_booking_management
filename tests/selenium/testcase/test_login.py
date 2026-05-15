import time, os
from tests.selenium.guest_fixture import login_page
from tests.selenium.data.user_data import LOGIN_USERS

SCREENSHOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "screenshots", "login")

def check_contains(text_list, expected):
    return any(expected in t for t in text_list)

def test_tc1_login_valid(login_page):
    username, password = LOGIN_USERS["valid_user"]
    login_page.login(username, password)
    time.sleep(1)
    login_page.screen(SCREENSHOT_DIR, "TC1_login_valid.png")
    assert "/login" not in login_page.get_url()


def test_tc2_login_user_not_exist(login_page):
    username, password = LOGIN_USERS["not_exist_user"]
    login_page.login(username, password)
    time.sleep(1)
    results = login_page.result()
    login_page.screen(SCREENSHOT_DIR, "TC2_user_not_exist.png")
    assert check_contains(results, "Sai tài khoản hoặc mật khẩu")
    assert "/login" in login_page.get_url()


def test_tc3_login_empty_username(login_page):
    username, password = LOGIN_USERS["empty_username"]
    login_page.login(username, password)
    time.sleep(1)
    username_input = login_page.find(*login_page.USERNAME_INPUT)
    msg = login_page.driver.execute_script("return arguments[0].validationMessage;", username_input)
    login_page.screen(SCREENSHOT_DIR, "TC3_empty_username.png")
    assert msg != ""
    assert "/login" in login_page.get_url()


def test_tc4_login_empty_password(login_page):
    username, password = LOGIN_USERS["empty_password"]
    login_page.login(username, password)
    time.sleep(1)
    password_input = login_page.find(*login_page.PASSWORD_INPUT)
    msg = login_page.driver.execute_script("return arguments[0].validationMessage;", password_input)
    login_page.screen(SCREENSHOT_DIR, "TC4_empty_password.png")
    assert msg != ""
    assert "/login" in login_page.get_url()


def test_tc5_login_wrong_password(login_page):
    username, password = LOGIN_USERS["wrong_password"]
    login_page.login(username, password)
    time.sleep(1)
    results = login_page.result()
    login_page.screen(SCREENSHOT_DIR, "TC5_wrong_password.png")
    assert check_contains(results, "Sai tài khoản hoặc mật khẩu")
    assert "/login" in login_page.get_url()


def test_tc6_login_wrong_user_and_password(login_page):
    username, password = LOGIN_USERS["wrong_both"]
    login_page.login(username, password)
    time.sleep(1)
    results = login_page.result()
    login_page.screen(SCREENSHOT_DIR, "TC6_wrong_both.png")
    assert check_contains(results, "Sai tài khoản hoặc mật khẩu")
    assert "/login" in login_page.get_url()