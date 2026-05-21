from selenium.webdriver.common.by import By


class DetailBookingLocators(object):
    PAY_BUTTON = (By.XPATH, '//button[contains(@onclick,"payBooking(")]')
    CANCEL_BUTTON=(By.XPATH, '//button[contains(@onclick,"cancelBooking(")]')
    BOOKING_DATE=(By.CSS_SELECTOR,'//div[contains(text(),"Ngày đặt sân")]''/parent::div/div[last()]')
    BOOKING_TIME=(By.CSS_SELECTOR,'//div[contains(text(),"Thời gian")]''/parent::div/div[last()]')
    TOTAL_PRICE=(By.CSS_SELECTOR,'//span[contains(text(),"Tổng tiền")]''/parent::div/span[last()]')
    TAG_STATUS=(By.CSS_SELECTOR,'.col-lg-8 > .card-body > div:nth-child(1) > span')
    LOCATION=(By.CSS_SELECTOR,'.col-lg-8 > .card-body > div:nth-child(1) > div > div:nth-child(1)')
    NAME_FIELD=(By.CSS_SELECTOR,'.col-lg-8 > .card-body > div:nth-child(1) > div > h4')