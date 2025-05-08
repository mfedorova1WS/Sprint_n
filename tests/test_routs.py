import pytest
import allure
from pages.main_page import MainPage
from pages.route_page import RoutePage


@allure.feature("Маршруты")
class TestRouts:
    @allure.story("Проверка отображения адресов")
    @pytest.mark.ui
    def test_route_points_display(self, driver, address_1, address_2):
        with allure.step("Открыта главная страница"):
            page = MainPage(driver)
            page.open()
        with allure.step("Ввод адресов для заказа такси"):
            page.enter_addresses(address_1, address_2)
        with allure.step("Проверка отображения адресов"):
            assert page.route_points_displayed()

    @allure.story("Проверка отображения маршрута")
    @pytest.mark.ui
    def test_route_block_shown(self, driver, address_1, address_2):
        with allure.step("Открыта главная страница"):
            page = MainPage(driver)
            page.open()
        with allure.step("Ввод адресов для заказа такси"):
            page.enter_addresses(address_1, address_2)
        with allure.step("Проверка отображения маршрута"):
            assert page.is_route_block_visible()

    @allure.story("Проверка времени в пути")
    @pytest.mark.ui
    @pytest.mark.xfail(reason="Неверный текст или блок не появляется")
    def test_same_address_route_block(self, driver, address_1, address_2):
        with allure.step("Открыта главная страница"):
            page = MainPage(driver)
            page.open()
        with allure.step("Ввод адресов для заказа такси"):
            page.enter_addresses(address_1, address_1)
        with allure.step("Проверка времени в пути при совпадении адреса отправления и адреса назначения"):
            page.find_duration_text("0 мин.")

    @allure.story("Виды маршрутов")
    @pytest.mark.ui
    def test_switch_route_types(self, driver, address_1, address_2):
        with allure.step("Открыта главная страница"):
            page = MainPage(driver)
            page.open()
        with allure.step("Ввод адресов для заказа такси"):
            page.enter_addresses(address_1, address_2)
            route = RoutePage(driver)
            assert route.switch_to_custom_and_check_types()