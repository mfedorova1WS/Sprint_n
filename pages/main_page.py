from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class MainPage(BasePage):
    URL = "https://ez-route.stand.praktikum-services.ru/"

    FROM = (By.ID, 'from')
    TO = (By.ID, 'to')
    MAP_POINTS = (By.CSS_SELECTOR, 'ymaps.ymaps-2-1-79-route-pin__label')
    ROUTE_BLOCK = (By.CLASS_NAME, 'workflow-subcontainer')
    DURATION = (By.CLASS_NAME, "duration")

    def open(self):
        self.driver.get(self.URL)

    def enter_addresses(self, from_addr, to_addr):
        self.input(self.FROM, from_addr)
        self.input(self.TO, to_addr)

    def route_points_displayed(self):
        return len(self.driver.find_elements(*self.MAP_POINTS)) == 2

    def is_route_block_visible(self):
        return self.is_visible(self.ROUTE_BLOCK)

    def find_duration_text(self, text):
        return self.find_and_wait_for_text(self.DURATION, text)
