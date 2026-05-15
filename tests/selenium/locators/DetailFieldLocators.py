from selenium.webdriver.common.by import By


class DetailFieldLocators(object):
    FIELD_NAME = (By.CSS_SELECTOR, "body > div:nth-child(3) > div.position-relative.mb-5  h1")
    ADDRESS = (By.CSS_SELECTOR, "body > div:nth-child(3) > div.position-relative.mb-5  span.me-3")

class BookingInfoLocators(object):
    DATE_INPUT = (By.ID, 'dateSelectedValue')
    START_TIME = (By.ID, 'startTime')
    END_TIME = (By.ID, 'endTime')
    TOTAL_TIME = (By.ID, 'totalTime')
    TOTAL_PRICE = (By.ID, 'totalPrice')
    BOOK_BUTTON = (By.CSS_SELECTOR, '.col-lg-4 .card-body > div:nth-child(5) > button')
    TABLE_PRICE = (By.CSS_SELECTOR, '#fieldPriceContainer tbody tr')
    END_INPUT = ('body > div:nth-child(6) input.flatpickr-hour','body > div:nth-child(6) input.flatpickr-minute')
    START_INPUT = ('body > div:nth-child(7) input.flatpickr-hour','body > div:nth-child(7) input.flatpickr-minute')

class PopupLocator(object):
    CONFIRM_MODAL = (By.CSS_SELECTOR, "#confirmBookingModal .modal-content")
    CONFIRM_FIELD_NAME = (By.CSS_SELECTOR,"#confirmBookingModal .modal-content > .modal-body > div:nth-child(2) > div:nth-child(1) > span:nth-child(2)")
    CONFIRM_ADDRESS = (By.ID, "confirmFieldAddress")
    DATE = (By.ID, "confirmDate")
    START_TIME = (By.ID, "confirmStartTime")
    END_TIME = (By.ID, "confirmEndTime")
    DURATION = (By.ID, "confirmDuration")
    TOTAL_PRICE = (By.ID, "confirmTotalPrice")
    CLOSE_BTN = (By.CSS_SELECTOR, "#confirmBookingModal .btn-close")
    CANCEL_BTN = (By.CSS_SELECTOR, "#confirmBookingModal .modal-footer > button:nth-child(1)")
    CONFIRM_BTN = (By.CSS_SELECTOR, "#confirmBookingModal .modal-footer > button:nth-child(2)")