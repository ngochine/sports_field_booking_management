import time, pytest
from tests.selenium.pages import LoginPage, DetailFieldPage, FieldsPage, RegisterPage
from tests.test_base import driver, test_app
from tests.selenium.data.user_data import LOGIN_USERS

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
def guest_fields_page(driver):
    page = FieldsPage.FieldsPage(driver=driver)
    page.open_page()
    return page

@pytest.fixture
def guest_detail_page(driver,guest_fields_page):
    list_page = FieldsPage.FieldsPage(driver=guest_fields_page.driver)
    time.sleep(1)
    link = list_page.get_link(1)
    page = DetailFieldPage.DetailFieldPage(driver=guest_fields_page.driver)
    page.open_page(link)
    return page
