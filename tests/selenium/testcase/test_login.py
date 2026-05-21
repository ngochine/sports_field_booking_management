import time, os
from  tests.test_base import driver,test_app
from tests.selenium.fixture import login_page
from tests.selenium.data.user_data import LOGIN_USERS
from tests.selenium.locators.LoginLocators import LoginLocator


def check_contains(text_list, expected):
    return any(expected in t for t in text_list)

def test_tc1_login_valid(login_page):
    username, password = LOGIN_USERS["valid_user"]
    login_page.login(username, password)
    time.sleep(1)
    login_page.screen_login("TC1_login_valid.png")
    assert "/login" not in login_page.get_url()


def test_tc2_login_user_not_exist(login_page):
    username, password = LOGIN_USERS["not_exist_user"]
    login_page.login(username, password)
    time.sleep(1)
    results = login_page.result()
    login_page.screen_login( "TC2_user_not_exist.png")
    assert check_contains(results, "Sai tài khoản hoặc mật khẩu")
    assert "/login" in login_page.get_url()


def test_tc3_login_empty_username(login_page):
    username, password = LOGIN_USERS["empty_username"]
    login_page.login(username, password)
    time.sleep(1)
    username_input = login_page.find(*LoginLocator.USERNAME_INPUT)
    msg = login_page.driver.execute_script("return arguments[0].validationMessage;", username_input)
    login_page.screen_login( "TC3_empty_username.png")
    assert msg != ""
    assert "/login" in login_page.get_url()


def test_tc4_login_empty_password(login_page):
    username, password = LOGIN_USERS["empty_password"]
    login_page.login(username, password)
    time.sleep(1)
    password_input = login_page.find(*LoginLocator.PASSWORD_INPUT)
    msg = login_page.driver.execute_script("return arguments[0].validationMessage;", password_input)
    login_page.screen_login( "TC4_empty_password.png")
    assert msg != ""
    assert "/login" in login_page.get_url()


def test_tc5_login_wrong_password(login_page):
    username, password = LOGIN_USERS["wrong_password"]
    login_page.login(username, password)
    time.sleep(1)
    results = login_page.result()
    login_page.screen_login( "TC5_wrong_password.png")
    assert check_contains(results, "Sai tài khoản hoặc mật khẩu")
    assert "/login" in login_page.get_url()


def test_tc6_login_wrong_user_and_password(login_page):
    username, password = LOGIN_USERS["wrong_both"]
    login_page.login(username, password)
    time.sleep(1)
    results = login_page.result()
    login_page.screen_login( "TC6_wrong_both.png")
    assert check_contains(results, "Sai tài khoản hoặc mật khẩu")
    assert "/login" in login_page.get_url()


def test_tc8_SQL_Injection(login_page):
    username, password = LOGIN_USERS["injection"]
    login_page.login(username, password)
    time.sleep(1)
    results = login_page.result()
    login_page.screen_login( "TC8_SQL_Injection.png")
    assert check_contains(results, "Sai tài khoản hoặc mật khẩu")
    assert "/login" in login_page.get_url()

def test_tc9_xss(login_page):
    username, password = LOGIN_USERS["xss"]
    login_page.login(username, password)
    time.sleep(1)
    results = login_page.result()
    login_page.screen_login( "TC9_xss.png")
    assert check_contains(results, "Sai tài khoản hoặc mật khẩu")
    assert "/login" in login_page.get_url()