import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

@pytest.fixture(scope="session")
def driver():
    options = Options()
    #options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

@pytest.fixture
def address_1():
    return "Хамовнический вал, 34"

@pytest.fixture
def address_2():
    return "Зубовский бульвар, 37"
