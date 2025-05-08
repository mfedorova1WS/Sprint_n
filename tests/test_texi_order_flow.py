import pytest
import allure
from selenium.common import TimeoutException
from pages.main_page import MainPage
from pages.route_page import RoutePage
from pages.order_page import OrderPage


@allure.feature("Оформление заказа такси")
class TestTaxiOrderFlow:

    @allure.story("Отображение элементов формы заказа")
    @pytest.mark.ui
    def test_order_form_fields_visible(self, driver, address_1, address_2):
        with allure.step("Открытие главной страницы и ввод адресов"):
            page = MainPage(driver)
            page.open()
            page.enter_addresses(address_1, address_2)
        with allure.step("Выбор быстрого маршрута и переход к заказу"):
            route = RoutePage(driver)
            route.select_fast_and_check_call()
            route.click_taxi_button()

            order = OrderPage(driver)
        with allure.step("Проверка элементов оформления заказа"):
            assert order.is_phone_input_visible(), "Поле ввода телефона не отображается"
            assert order.is_payment_selector_visible(), "Выбор способа оплаты не отображается"
            assert order.is_comment_input_visible(), "Поле комментария не отображается"
            assert order.is_requirements_block_visible(), "Блок требований не отображается"


    @allure.story("Проверка оформление заказа и элементов на форме поиска машины")
    @pytest.mark.ui
    def test_taxi_order_flow(self, driver, address_1, address_2):
        with allure.step("Открытие главной страницы и ввод адресов"):
            main_page = MainPage(driver)
            main_page.open()
            main_page.enter_addresses(address_1, address_2)

        with allure.step("Выбор быстрого маршрута и переход к заказу"):
            route = RoutePage(driver)
            route.select_fast_and_check_call()
            route.click_taxi_button()

        with allure.step("Выбор тарифа и требований"):
            order = OrderPage(driver)
            order.select_tariff("Рабочий")
            order.expand_requirements_block()
            order.check_requirement_checkbox("Столик для ноутбука")
            order.submit_order()

        with allure.step("Проверка элементов окна ожидания машины"):
            assert order.wait_for_waiting_block(), "Окно ожидания машины не появилось"

            assert order.wait_for_timer_displayed(), "Таймер не отображается"
            assert order.check_cancel_button_visible(), "Кнопка 'Отменить' не отображается"
            assert order.check_details_button_visible(), "Кнопка 'Детали' не отображается"
            assert order.check_header_text("Поиск машины"), "Заголовок 'Поиск машины' не найден"

    @allure.story("Оформление заказа и элементов на форме ожидания машины")
    @pytest.mark.ui
    @pytest.mark.xfail(reason="Кнопка отмены не работает — окно не закрывается")
    def test_taxi_order_and_find_car_flow(self, driver, address_1, address_2):
        with allure.step("Открытие главной страницы и ввод адресов"):
            main_page = MainPage(driver)
            main_page.open()
            main_page.enter_addresses(address_1, address_2)

        with allure.step("Выбор быстрого маршрута и переход к заказу"):
            route = RoutePage(driver)
            route.select_fast_and_check_call()
            route.click_taxi_button()

        with allure.step("Выбор тарифа и требований"):
            order = OrderPage(driver)
            order.select_tariff("Рабочий")
            order.expand_requirements_block()
            order.check_requirement_checkbox("Столик для ноутбука")
            order.submit_order()

        with allure.step("Проверка окна ожидания машины"):
            assert order.wait_for_waiting_block(), "Окно ожидания машины не появилось"
            assert order.is_timer_displayed(), "Таймер не отображается"
            assert order.check_cancel_button_visible, "Кнопка 'Отменить' не отображается"
            assert order.is_details_button_visible(), "Кнопка 'Детали' не отображается"
            assert order.has_waiting_header_text("Поиск машины"), "Заголовок 'Поиск машины' не найден"

        with allure.step("Ожидание завершения таймера (исчезновения таймера)"):
            try:
                order.wait_for_timer_to_finish()
            except TimeoutException:
                pytest.fail("Таймер не исчез в течение ожидаемого времени")

        with allure.step("Проверка окна найденной машины"):
            assert order.is_success_block_visible(), "Окно найденной машины не появилось"
            assert order.has_success_header_text(), "Заголовок с временем прибытия не отображается"
            assert order.is_car_number_displayed(), "Номер машины не отображается"
            assert order.is_tariff_icon_displayed(), "Иконка тарифа не отображается"
            assert order.is_driver_info_visible(), "Информация о водителе не полная"

        with allure.step("Проверка окна деталей поездки"):
            order.click_more_details()
            assert order.is_pickup_address_correct(address_1), "Адрес подачи не соответствует"
            assert order.is_dropoff_address_correct(address_2), "Адрес назначения не соответствует"
            assert order.is_payment_method_displayed(), "Способ оплаты не отображается"
            assert order.is_trip_info_header_displayed(), "Заголовок 'Еще про поездку' не отображается"
            assert order.is_trip_price_displayed(), "Стоимость поездки не отображается"

        with allure.step("Отмена заказа и проверка закрытия окна"):
            order.cancel_order()
            assert order.order_window_closed(), "Окно заказа не закрылось после отмены"
