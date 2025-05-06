from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def find(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )

    def find_all(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_all_elements_located(locator)
        )

    def find_and_wait_for_text(self, locator, text, timeout=10):
        element = WebDriverWait(self.driver, timeout).until(
            EC.text_to_be_present_in_element(locator, text)
        )
        return element

    def click(self, locator):
        self.find(locator).click()

    def input(self, locator, text):
        field = self.find(locator)
        field.clear()
        field.send_keys(text)

    def hover(self, locator):
        from selenium.webdriver.common.action_chains import ActionChains
        element = self.find(locator)
        ActionChains(self.driver).move_to_element(element).perform()

    def is_visible(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))
