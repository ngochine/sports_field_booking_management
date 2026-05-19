import time, pytest
from tests.selenium.pages import LoginPage, DetailFieldPage, FieldsPage, RegisterPage
from tests.test_base import driver, test_app ,driver2
from tests.selenium.data.user_data import LOGIN_USERS, REGISTER_USERS
from tests.selenium.guest_fixture import register_page


def test_register_valid(register_page):
    for username, password, confirm in REGISTER_USERS["valid_user"]:
        register_page.register(username,password,confirm)
        time.sleep(1)
        register_page.open_page()
    assert True


def login(driver, username, password):
    page = LoginPage.LoginPage(driver)
    page.open_page()
    page.login(username, password)
    time.sleep(1)
    return driver

def open_detail_page(driver, username, password):
    driver = login(driver, username, password)
    fields_page = FieldsPage.FieldsPage(driver)
    fields_page.open_page()
    link = fields_page.get_link(0)
    page = DetailFieldPage.DetailFieldPage(driver)
    page.open_page(link)
    return page

@pytest.fixture
def auth_driver(driver):
    return login(driver,LOGIN_USERS["valid_user"][0],LOGIN_USERS["valid_user"][1])

@pytest.fixture
def auth_driver2(driver2):
    return login(driver2, LOGIN_USERS["valid_user_3"][0], LOGIN_USERS["valid_user_3"][1])

@pytest.fixture
def fields_page(auth_driver):
    page = FieldsPage.FieldsPage(driver=auth_driver)
    page.open_page()
    return page

@pytest.fixture
def detail_page(driver):
    return open_detail_page(driver,LOGIN_USERS["valid_user"][0],LOGIN_USERS["valid_user"][1])

