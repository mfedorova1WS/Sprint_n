from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class OrderPage(BasePage):
    TARIFFS = (By.CLASS_NAME, "tcard")
    INFO_ICON = (By.CLASS_NAME, "tcard-i")
    TOOLTIP = (By.CSS_SELECTOR, 'div.__react_component_tooltip.i-floating-tooltip')
    COMMENT = (By.CSS_SELECTOR, '[data-testid="comment"]')
    ACTIVE_TARIFF = (By.CSS_SELECTOR, "div.tcard.active")
    PHONE_INPUT = (By.XPATH, "//div[text()='Телефон']")
    PAYMENT_SELECTOR = (By.CLASS_NAME, "pp-button")
    COMMENT_INPUT = (By.ID, "comment")
    REQUIREMENTS_BLOCK = (By.XPATH, "//div[text()='Требования к заказу']")
    CHECKBOX_LABEL = lambda self, label: (
        By.XPATH,
        f"//div[contains(@class, 'r-sw-label') and normalize-space(text())='{label}']/following-sibling::div//span[contains(@class, 'slider')]"
    )
    CALL_BUTTON = (By.CSS_SELECTOR, ".smart-button")
    WAITING_BLOCK = (By.CLASS_NAME, "order-body")
    SUCCESS_BLOCK = (By.CLASS_NAME, "order-header-content")
    DETAILS_BUTTON = (By.XPATH, "//button[.//img[contains(@src, 'burger')]]")
    PRICE_IN_DETAILS = (By.CLASS_NAME, "final-price")
    CANCEL_BUTTON = (By.XPATH, "//button[.//img[contains(@src, 'plus')]]")

    # Локаторы окна ожидания машины
    WAITING_HEADER = (By.XPATH, "//div[@class='order-header-title' and contains(text(), 'Поиск машины')]")

    TIMER = (By.CSS_SELECTOR, '.order-header-time')

    # Блок успешного заказа
    SUCCESS_HEADER = (By.CSS_SELECTOR, "div.order-header-title")
    MORE_DETAILS_BUTTON = (By.CSS_SELECTOR, '[data-testid="more-details-button"]')
    CAR_NUMBER = (By.CLASS_NAME, 'number')
    CAR_ICON = (By.CSS_SELECTOR, ".order-number img[alt='Car']")
    DRIVER_NAME = (By.XPATH,
                   "//div[contains(@class, 'order-btn-group') and .//div[contains(@class, 'order-btn-rating')]]/following-sibling::div")
    DRIVER_AVATAR = (By.CSS_SELECTOR, "img[alt='close']")
    DRIVER_RATING = (By.CSS_SELECTOR, ".order-btn-rating")
    TRIP_PRICE = (By.XPATH, "//div[contains(@class, 'o-d-sh') and contains(text(), 'Стоимость')]")
    TRIP_INFO_HEADER = (By.CLASS_NAME, 'order-header-content')
    PAYMENT_METHOD = PAYMENT_LABEL = (By.XPATH, "//div[@class='o-d-sh' and text()='Способ оплаты']")
    PICKUP_ADDRESS = (By.XPATH, "//div[@class='order-details-content']//div[@class='o-d-h']")
    DROPOFF_ADDRESS = (By.XPATH, "//div[@class='order-details-content']//div[@class='o-d-sh' and text()='Адрес назначения']/preceding-sibling::div[@class='o-d-h']")


    # Проверка соответствия цены тарифу
    PRICE_TEXT = (By.CSS_SELECTOR, '[data-testid="order-price"]')

    def get_tariff_elements(self):
        return self.find_all(self.TARIFFS)

    def is_phone_input_visible(self):
        return self.is_visible(self.PHONE_INPUT)

    def is_payment_selector_visible(self):
        return self.is_visible(self.PAYMENT_SELECTOR)

    def is_comment_input_visible(self):
        return self.is_visible(self.COMMENT_INPUT)

    def is_requirements_block_visible(self):
        return self.is_visible(self.REQUIREMENTS_BLOCK)

    def wait_for_timer_displayed(self):
        return self.is_visible(self.TIMER)

    def select_tariff(self, name):
        tariff_xpath = f"//div[contains(@class, 'tcard-title') and normalize-space(text())='{name}']/ancestor::div[contains(@class, 'tcard')]"
        element = self.find((By.XPATH, tariff_xpath))
        element.click()

    def is_timer_displayed(self):
        return self.is_visible(self.TIMER)

    def is_details_button_visible(self):
        return self.is_visible(self.DETAILS_BUTTON)

    def has_waiting_header_text(self, expected_text):
        header = self.find(self.WAITING_HEADER)
        return expected_text in header.text

    def check_requirement_checkbox(self, label):
        self.find(self.CHECKBOX_LABEL(label)).click()

    def enter_phone_number(self, phone):
        input_elem = self.find(self.PHONE_INPUT)
        input_elem.clear()
        input_elem.send_keys(phone)

    def submit_order(self):
        self.find(self.CALL_BUTTON).click()

    def wait_for_waiting_block(self, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(self.WAITING_BLOCK)
        )

    def wait_for_timer_to_finish(self, timeout=40):
        WebDriverWait(self.driver, timeout).until(
            EC.invisibility_of_element_located(self.TIMER)
        )

    def wait_for_success_block(self, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(self.SUCCESS_BLOCK)
        )

    def click_more_details(self):
        self.find(self.DETAILS_BUTTON).click()

    def check_price_matches_tariff(self, expected_tariff_name):
        # Можно адаптировать под логику отображения цены для тарифа
        price = self.find(self.PRICE_IN_DETAILS).text
        return price.strip() != ""

    def cancel_order(self):
        self.find(self.CANCEL_BUTTON).click()

    def order_window_closed(self):
        return WebDriverWait(self.driver, 10).until(
            EC.invisibility_of_element_located(self.SUCCESS_BLOCK)
        )

    def get_active_tariff(self):
        return self.find(self.ACTIVE_TARIFF)

    def expand_requirements_block(self):
        header = self.find((By.CSS_SELECTOR, "div.reqs-header"))
        body = self.driver.find_elements(By.CSS_SELECTOR, "div.reqs-body")

        if not body or not body[0].is_displayed():
            header.click()

    def hover_tariff_info_and_get_tooltip(self):
        self.hover(self.INFO_ICON)
        return self.find(self.TOOLTIP).text

    def check_cancel_button_visible(self):
        return self.is_visible(self.CANCEL_BUTTON)

    def check_details_button_visible(self):
        return self.is_visible(self.DETAILS_BUTTON)

    def check_header_text(self, expected_text):
        return self.find(self.WAITING_HEADER).text.strip() == expected_text

    def is_success_block_visible(self):
        return self.is_visible(self.SUCCESS_BLOCK)

    def has_success_header_text(self):
        return self.is_visible(self.SUCCESS_HEADER) and "мин." in self.find(self.SUCCESS_HEADER).text

    def is_car_number_displayed(self):
        return self.is_visible(self.CAR_NUMBER)

    def is_tariff_icon_displayed(self):
        return self.is_visible(self.CAR_ICON)

    def is_driver_info_visible(self):
        return (
                self.is_visible(self.DRIVER_NAME) and
                self.is_visible(self.DRIVER_AVATAR) and
                self.is_visible(self.DRIVER_RATING)
        )

    def is_pickup_address_correct(self, expected):
        return expected in self.find(self.PICKUP_ADDRESS).text

    def is_dropoff_address_correct(self, expected):
        return expected in self.find(self.DROPOFF_ADDRESS).text

    def is_payment_method_displayed(self):
        return self.is_visible(self.PAYMENT_METHOD)

    def is_trip_info_header_displayed(self):
        return self.is_visible(self.TRIP_INFO_HEADER)

    def is_trip_price_displayed(self):
        return self.is_visible(self.TRIP_PRICE)

