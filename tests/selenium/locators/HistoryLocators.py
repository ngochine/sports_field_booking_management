from selenium.webdriver.common.by import By

class HistoryLocators(object):
    BOOKING_CARD=(By.CLASS_NAME,'card-body')
    FILTER_SELECT=(By.CLASS_NAME,'form-select')
    PAGINATION=(By.CLASS_NAME,'pagination')
    CANCEL_POPUP=(By.CLASS_NAME,'modal-content')
    PAGE_ITEMS = (By.CSS_SELECTOR, '.pagination .page-item a.page-link')
    NEXT_PAGE = (By.XPATH,'//ul[contains(@class,"pagination")]//*[contains(text(),"»")]')
    ACTIVE_PAGE = (By.CSS_SELECTOR,'.pagination .page-item.active')

class BookingCardLocators(object):
    PAY_BUTTON = (By.XPATH, './/button[contains(@onclick,"payBooking(")]')
    CANCEL_BUTTON=(By.XPATH, './/a[contains(text(),"Hủy đặt vé")]')
    DETAIL_BUTTON=(By.XPATH, './/a[contains(text(),"Chi tiết")]')
    BOOKING_DATE=(By.CSS_SELECTOR,'div.row.g-3.mb-4 > div:nth-child(1) > div > div.fw-semibold')
    BOOKING_TIME=(By.CSS_SELECTOR,'div.row.g-3.mb-4 > div:nth-child(2) > div > div.fw-semibold')
    TOTAL_PRICE=(By.CSS_SELECTOR,'div.row.g-3.mb-4 > div:nth-child(3) > div > div.fw-bold')
    TAG_STATUS=(By.CSS_SELECTOR,'div.d-flex.gap-2.mb-3 > div:nth-child(2) > span')
    LOCATION=(By.CSS_SELECTOR,'div.d-flex.gap-2.mb-3 > div:nth-child(1) > div:nth-child(2)')
    NAME_FIELD=(By.CSS_SELECTOR,'div.d-flex.gap-2.mb-3 > div:nth-child(1) > h4')

class CancelPopupLocators(object):
    POPUP_NAME_FIELD = (By.XPATH,'//div[contains(@class,"modal") and contains(@class,"show")]''//span[contains(text(),"Tên sân")]''/parent::div/span[last()]')
    POPUP_BOOKING_DATE = (By.XPATH,'//div[contains(@class,"modal") and contains(@class,"show")]''//span[contains(text(),"Ngày đặt")]''/parent::div/span[last()]')
    POPUP_BOOKING_TIME = (By.XPATH,'//div[contains(@class,"modal") and contains(@class,"show")]''//span[contains(text(),"Thời gian")]''/parent::div/span[last()]')
    POPUP_TOTAL_PRICE = (By.XPATH,'//div[contains(@class,"modal") and contains(@class,"show")]''//span[contains(text(),"Tổng tiền")]''/parent::div/span[last()]')
    POPUP_BACK_BUTTON = (By.XPATH,'//div[contains(@class,"modal") and contains(@class,"show")]''//button[contains(text(),"Quay lại")]')
    POPUP_CANCEL_BUTTON = (By.XPATH,'//div[contains(@class,"modal") and contains(@class,"show")]''//button[contains(@onclick,"cancelBooking(")]')
    POPUP_CLOSE_BUTTON = (By.XPATH,'//div[contains(@class,"modal") and contains(@class,"show")]''//button[contains(@class,"btn-close")]')