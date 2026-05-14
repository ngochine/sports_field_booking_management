import time, pytest
from tests.selenium.pages import LoginPage, DetailFieldPage, FieldsPage, RegisterPage
from tests.test_base import driver, test_app
from tests.selenium.data.user_data import LOGIN_USERS

@pytest.fixture
def auth_driver(driver):
    page = LoginPage.LoginPage(driver)
    page.open_page()
    page.login(LOGIN_USERS["valid_user"][0], LOGIN_USERS["valid_user"][1])
    time.sleep(1)
    return driver

# @pytest.fixture
# def register_page(guest_driver):
#     page = RegisterPage.RegisterPage(driver=guest_driver)
#     page.open_page()
#     return page
#
# @pytest.fixture
# def login_page(guest_driver):
#     page = LoginPage.LoginPage(driver=guest_driver)
#     page.open_page()
#     return page

@pytest.fixture
def fields_page(auth_driver):
    page = FieldsPage.FieldsPage(driver=auth_driver)
    page.open_page()
    return page

@pytest.fixture
def detail_page(driver,fields_page):
    list_page = FieldsPage.ListComponent(driver=fields_page.driver)
    time.sleep(1)
    link = list_page.get_link(0)
    page = DetailFieldPage.DetailFieldPage(driver=fields_page.driver)
    page.open_page(link)
    return page

@pytest.fixture
def booking_page(driver,detail_page):
    return DetailFieldPage.BookingInfoComponent(driver=detail_page.driver)

@pytest.fixture
def popup(driver,detail_page):
    return DetailFieldPage.PopupComponent(driver=detail_page.driver)



# def find_field_with_adjacent_slots(fields_page, start_id=1, max_id=10):
#     for fid in range(start_id, max_id + 1):
#         detail_page(fields_page,id=fid)
#         booking_page(detail_page.driver)
#         start, end = booking_page.get_adjacent_slots_time()
#         if start is not None and end is not None:
#             return booking_page, start, end, fid
#
#     return None, None, None, None