import time
import pytest
import allure

from pages.main_page import MainPage
from pages.route_page import RoutePage
from pages.order_page import OrderPage

ADDRESS_1 = "Хамовнический вал, 34"
ADDRESS_2 = "Зубовский бульвар, 37"

@allure.feature("Маршруты")
@pytest.mark.ui
def test_route_points_display(driver):
    page = MainPage(driver)
    page.open()
    page.enter_addresses(ADDRESS_1, ADDRESS_2)
    assert page.route_points_displayed()

@allure.feature("Блок маршрута")
@pytest.mark.ui
def test_route_block_shown(driver):
    page = MainPage(driver)
    page.open()
    page.enter_addresses(ADDRESS_1, ADDRESS_2)
    assert page.is_route_block_visible()

@allure.feature("Блок маршрута")
@pytest.mark.ui
@pytest.mark.xfail(reason="Неверный текст или блок не появляется")
def test_same_address_route_block(driver):
    page = MainPage(driver)
    page.open()
    page.enter_addresses(ADDRESS_1, ADDRESS_1)
    page.find_duration_text("0 мин.")

@allure.feature("Виды маршрутов")
@pytest.mark.ui
def test_switch_route_types(driver):
    page = MainPage(driver)
    page.open()
    page.enter_addresses(ADDRESS_1, ADDRESS_2)
    route = RoutePage(driver)
    assert route.switch_to_custom_and_check_types()

@allure.feature("Такси и Драйв")
@pytest.mark.ui
def test_taxi_and_drive_buttons(driver):
    page = MainPage(driver)
    page.open()
    page.enter_addresses(ADDRESS_1, ADDRESS_2)
    route = RoutePage(driver)
    assert route.select_fast_and_check_call()
    assert route.select_drive_and_check_book()

@allure.feature("Hover тарифов")
@pytest.mark.ui
def test_tariff_info_hover(driver):
    page = MainPage(driver)
    page.open()
    page.enter_addresses(ADDRESS_1, ADDRESS_2)
    route = RoutePage(driver)
    route.select_fast_and_check_call()
    route.click_taxi_button()
    order = OrderPage(driver)
    time.sleep(5)
    tooltip = order.hover_tariff_info_and_get_tooltip()
    assert "Для деловых" in tooltip or "Для тех" in tooltip
