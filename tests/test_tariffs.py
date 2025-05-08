import time
import pytest
import allure
from pages.main_page import MainPage
from pages.route_page import RoutePage
from pages.order_page import OrderPage


@allure.feature("Полное флоу заказа такси")
class TestTariffs:

    @allure.story("Такси и Драйв")
    @pytest.mark.ui
    def test_taxi_and_drive_buttons(self, driver, address_1, address_2):
        with allure.step("Открыта главная страница"):
            page = MainPage(driver)
            page.open()
        with allure.step("Ввод адресов для заказа такси"):
            page.enter_addresses(address_1, address_2)
            route = RoutePage(driver)
        with allure.step("При выборе маршрута Свой, типа передвижения Драйв активна кнопка Забронировать"):
            assert route.select_fast_and_check_call()
            assert route.select_drive_and_check_book()

    @allure.story("Hover тарифов")
    @pytest.mark.ui
    def test_tariff_info_hover(self, driver, address_1, address_2):
        with allure.step("Открыта главная страница"):
            page = MainPage(driver)
            page.open()
        with allure.step("Ввод адресов для заказа такси"):
            page.enter_addresses(address_1, address_2)
        with allure.step("Выбор быстрого маршрута и переход к заказу"):
            route = RoutePage(driver)
            route.select_fast_and_check_call()
            route.click_taxi_button()
            order = OrderPage(driver)
            time.sleep(5)
            tooltip = order.hover_tariff_info_and_get_tooltip()
        with allure.step("Проверка отображение тултипов у тарифа"):
            assert "Для деловых" in tooltip or "Для тех" in tooltip

    @allure.story("Отображение всех тарифов")
    @pytest.mark.ui
    def test_tariff_list_and_active(self, driver, address_1, address_2):
        with allure.step("Открыта главная страница"):
            page = MainPage(driver)
            page.open()
        with allure.step("Ввод адресов для заказа такси"):
            page.enter_addresses(address_1, address_2)

        with allure.step("Выбор быстрого маршрута и переход к заказу"):
            route = RoutePage(driver)
            route.select_fast_and_check_call()
            route.click_taxi_button()

            order = OrderPage(driver)
            tariffs = order.get_tariff_elements()
            active_tariff = order.get_active_tariff()
        with allure.step("Открывается форма заказа со всеми 6 тарифами, один из них активный"):
            assert len(tariffs) == 6, "Ожидалось 6 тарифов"
            assert active_tariff is not None, "Активный тариф не найден"