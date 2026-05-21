import time, pytest, uuid

from tests.selenium.data.booking_data import CANCEL_CASE
from tests.selenium.pages import LoginPage, DetailFieldPage, FieldsPage, RegisterPage,HistoryPage
from tests.test_base import driver, test_app ,driver2
from tests.selenium.data.user_data import LOGIN_USERS, REGISTER_USERS


def register(driver, username, password):
    page = RegisterPage.RegisterPage(driver)
    page.open_page()
    page.register(username, password, password)
    time.sleep(1)
    return driver


def login(driver, username, password):
    page = LoginPage.LoginPage(driver)
    page.open_page()
    page.login(username, password)
    time.sleep(1)
    return driver

def generate_user():
    return {
        "username": f"user_{uuid.uuid4().hex[:10]}",
        "password": "Aa@123456"
    }

def register_login(driver, username="",password="",get_account=False):
    if username == "" and password == "":
        account = generate_user()
        driver = register(driver, account["username"], account["password"])
        driver = login(driver, account["username"], account["password"])
        if get_account == True:
            return driver, account
    else:
        driver = login(driver, username, password)
    return driver

def open_detail_page(driver):
    fields_page = FieldsPage.FieldsPage(driver)
    fields_page.open_page()
    link = fields_page.get_link(0)
    page = DetailFieldPage.DetailFieldPage(driver)
    page.open_page(link)
    return page

def open_history_page(driver):
    page = HistoryPage.HistoryPage(driver)
    page.open_page()
    return page


@pytest.fixture
def register_page(driver):
    page = RegisterPage.RegisterPage(driver=driver)
    page.open_page()
    return page

@pytest.fixture
def login_page(driver):
    page = LoginPage.LoginPage(driver=driver)
    page.open_page()
    return page


@pytest.fixture
def fields_page(driver):
    driver=register_login(driver=driver)
    page = FieldsPage.FieldsPage(driver=driver)
    page.open_page()
    return page

@pytest.fixture
def guest_fields_page(driver):
    page = FieldsPage.FieldsPage(driver=driver)
    page.open_page()
    return page


@pytest.fixture
def detail_page(driver):
    driver = register_login(driver)
    return open_detail_page(driver)

@pytest.fixture
def detail_page_2(driver2):
    driver2 = register_login(driver2)
    return open_detail_page(driver2)

@pytest.fixture
def guest_detail_page(driver):
    return open_detail_page(driver)


@pytest.fixture
def history_page(driver):
    driver = register_login(driver)
    return open_history_page(driver)

@pytest.fixture
def cancel_history_page(driver):
    driver= login(driver=driver,username=CANCEL_CASE["valid_user"][0], password=CANCEL_CASE["valid_user"][1])
    return open_history_page(driver)

@pytest.fixture
def cancel_detail_page(driver2):
    driver2= login(driver=driver2,username=CANCEL_CASE["valid_user"][0], password=CANCEL_CASE["valid_user"][1])
    return open_detail_page(driver2)
