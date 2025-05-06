import time
import pytest
import allure
from selenium.common import TimeoutException

from pages.main_page import MainPage
from pages.route_page import RoutePage
from pages.order_page import OrderPage

ADDRESS_1 = "Хамовнический вал, 34"
ADDRESS_2 = "Зубовский бульвар, 37"

@allure.feature("Маршруты")
@pytest.mark.ui
def test_route_points_display(driver):
    with allure.step("Открыта главная страница"):
        page = MainPage(driver)
        page.open()
    with allure.step("Ввод адресов для заказа такси"):
        page.enter_addresses(ADDRESS_1, ADDRESS_2)
    with allure.step("Проверка отображения адресов"):
        assert page.route_points_displayed()

@allure.feature("Блок маршрута")
@pytest.mark.ui
def test_route_block_shown(driver):
    with allure.step("Открыта главная страница"):
        page = MainPage(driver)
        page.open()
    with allure.step("Ввод адресов для заказа такси"):
        page.enter_addresses(ADDRESS_1, ADDRESS_2)
    with allure.step("Проверка отображения маршрута"):
        assert page.is_route_block_visible()

@allure.feature("Блок маршрута")
@pytest.mark.ui
@pytest.mark.xfail(reason="Неверный текст или блок не появляется")
def test_same_address_route_block(driver):
    with allure.step("Открыта главная страница"):
        page = MainPage(driver)
        page.open()
    with allure.step("Ввод адресов для заказа такси"):
        page.enter_addresses(ADDRESS_1, ADDRESS_1)
    with allure.step("Проверка времени в пути при совпадении адреса отправления и адреса назначения"):
        page.find_duration_text("0 мин.")

@allure.feature("Виды маршрутов")
@pytest.mark.ui
def test_switch_route_types(driver):
    with allure.step("Открыта главная страница"):
        page = MainPage(driver)
        page.open()
    with allure.step("Ввод адресов для заказа такси"):
        page.enter_addresses(ADDRESS_1, ADDRESS_2)
        route = RoutePage(driver)
        assert route.switch_to_custom_and_check_types()

@allure.feature("Такси и Драйв")
@pytest.mark.ui
def test_taxi_and_drive_buttons(driver):
    with allure.step("Открыта главная страница"):
        page = MainPage(driver)
        page.open()
    with allure.step("Ввод адресов для заказа такси"):
        page.enter_addresses(ADDRESS_1, ADDRESS_2)
        route = RoutePage(driver)
    with allure.step("При выборе маршрута Свой, типа передвижения Драйв активна кнопка Забронировать"):
        assert route.select_fast_and_check_call()
        assert route.select_drive_and_check_book()

@allure.feature("Hover тарифов")
@pytest.mark.ui
def test_tariff_info_hover(driver):
    with allure.step("Открыта главная страница"):
        page = MainPage(driver)
        page.open()
    with allure.step("Ввод адресов для заказа такси"):
        page.enter_addresses(ADDRESS_1, ADDRESS_2)
    with allure.step("Выбор быстрого маршрута и переход к заказу"):
        route = RoutePage(driver)
        route.select_fast_and_check_call()
        route.click_taxi_button()
        order = OrderPage(driver)
        time.sleep(5)
        tooltip = order.hover_tariff_info_and_get_tooltip()
    with allure.step("Проверка отображение тултипов у тарифа"):
        assert "Для деловых" in tooltip or "Для тех" in tooltip

@allure.feature("Тарифы")
@pytest.mark.ui
def test_tariff_list_and_active(driver):
    with allure.step("Открыта главная страница"):
        page = MainPage(driver)
        page.open()
    with allure.step("Ввод адресов для заказа такси"):
        page.enter_addresses(ADDRESS_1, ADDRESS_2)

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


@allure.feature("Форма заказа")
@pytest.mark.ui
def test_order_form_fields_visible(driver):
    with allure.step("Открытие главной страницы и ввод адресов"):
        page = MainPage(driver)
        page.open()
        page.enter_addresses(ADDRESS_1, ADDRESS_2)
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


@allure.feature("Оформление заказа")
@pytest.mark.ui
def test_taxi_order_flow(driver):
    with allure.step("Открытие главной страницы и ввод адресов"):
        main_page = MainPage(driver)
        main_page.open()
        main_page.enter_addresses(ADDRESS_1, ADDRESS_2)

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

@allure.feature("Оформление заказа")
@pytest.mark.ui
def test_taxi_order_and_find_car_flow(driver):
    with allure.step("Открытие главной страницы и ввод адресов"):
        main_page = MainPage(driver)
        main_page.open()
        main_page.enter_addresses(ADDRESS_1, ADDRESS_2)

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
        assert order.is_pickup_address_correct(ADDRESS_1), "Адрес подачи не соответствует"
        assert order.is_dropoff_address_correct(ADDRESS_2), "Адрес назначения не соответствует"
        assert order.is_payment_method_displayed(), "Способ оплаты не отображается"
        assert order.is_trip_info_header_displayed(), "Заголовок 'Еще про поездку' не отображается"
        assert order.is_trip_price_displayed(), "Стоимость поездки не отображается"

#   Кнопка отмены не работает в интерфейсе приложения
#    with allure.step("Отмена заказа и проверка закрытия окна"):
#        order.cancel_order()
#        assert order.order_window_closed(), "Окно заказа не закрылось после отмены"
