from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class OrderPage(BasePage):
    TARIFFS = (By.CSS_SELECTOR, '[data-testid^="tariff-option"]')
    INFO_ICON = (By.CLASS_NAME, "tcard-i")
    TOOLTIP = (By.CSS_SELECTOR, 'div.__react_component_tooltip.i-floating-tooltip')
    INPUT_PHONE = (By.CSS_SELECTOR, '[data-testid="phone-input"]')
    PAY_METHOD = (By.CSS_SELECTOR, '[data-testid="pay-method"]')
    COMMENT = (By.CSS_SELECTOR, '[data-testid="comment"]')
    SUBMIT = (By.CSS_SELECTOR, '[data-testid="submit-order"]')

    def hover_tariff_info_and_get_tooltip(self):
        self.hover(self.INFO_ICON)
        return self.find(self.TOOLTIP).text
