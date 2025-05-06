from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class RoutePage(BasePage):
    # Tabs
    OPTIMAL = (By.XPATH, "//button[contains(text(), 'Оптимальный')]")
    FAST = (By.XPATH, "//div[text()='Быстрый']")
    CUSTOM = (By.XPATH, "//div[text()='Свой']")
    ACTIVE_TAB = (By.CSS_SELECTOR, ".mode.active")

    # Transport types for "Свой"
    DRIVE_TYPE = (By.XPATH, "//div[contains(@class, 'drive')]")

    # Buttons
    CALL_TAXI = (By.XPATH, "//button[contains(text(), 'Вызвать')]")
    BOOK_DRIVE = (By.XPATH, "//button[contains(text(), 'Забронировать')]")
    TAXI_BUTTON = (By.CSS_SELECTOR, "button.button.round")

    # Duration text block
    DURATION = (By.CLASS_NAME, "duration")

    def switch_to_custom_and_check_types(self):
        self.click(self.CUSTOM)
        return self.is_visible(self.DRIVE_TYPE)

    def switch_to_fast_and_check_active(self):
        self.click(self.FAST)
        return "Быстрый" in self.find(self.ACTIVE_TAB).text

    def select_fast_and_check_call(self):
        self.click(self.FAST)
        return self.is_visible(self.CALL_TAXI)

    def select_drive_and_check_book(self):
        self.click(self.CUSTOM)
        self.click(self.DRIVE_TYPE)
        return self.is_visible(self.BOOK_DRIVE)

    def click_taxi_button(self):
        self.click(self.TAXI_BUTTON)

    def get_duration_text(self):
        return self.find(self.DURATION).text
