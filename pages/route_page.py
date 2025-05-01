from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class RoutePage(BasePage):
    OPTIMAL = (By.XPATH, "//button[contains(text(), 'Оптимальный')]")
    FAST = (By.XPATH, "//div[text()='Быстрый']")
    CUSTOM = (By.XPATH, "//div[text()='Свой']")
    DRIVE_TYPE = (By.XPATH, "//div[contains(@class, 'drive')]")
    CALL_TAXI = (By.XPATH, "//button[contains(text(), 'Вызвать')]")
    BOOK_DRIVE = (By.XPATH, "//button[contains(text(), 'Забронировать')]")
    TAXI_BUTTON = (By.CSS_SELECTOR, "button.button.round")

    def switch_to_custom_and_check_types(self):
        self.click(self.CUSTOM)
        return self.is_visible(self.DRIVE_TYPE)

    def select_fast_and_check_call(self):
        self.click(self.FAST)
        return self.is_visible(self.CALL_TAXI)

    def select_drive_and_check_book(self):
        self.click(self.CUSTOM)
        self.click(self.DRIVE_TYPE)
        return self.is_visible(self.BOOK_DRIVE)

    def click_taxi_button(self):
        self.click(self.TAXI_BUTTON)
