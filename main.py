import data
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from pages import UrbanRoutesPage

class TestUrbanRoutes:
    driver = None

    @classmethod
    def setup_class(cls):
        options = Options()
        options.set_capability("goog:loggingPrefs", {'performance': 'ALL'})
        cls.driver = webdriver.Chrome(options=options)
        cls.driver.maximize_window()

    # 1. Configurar la dirección
    def test_1_set_route(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.address_from, data.address_to)
        assert routes_page.get_from() == data.address_from
        assert routes_page.get_to() == data.address_to

    # 2. Seleccionar la tarifa Comfort
    def test_2_select_comfort_tariff(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.select_comfort_tariff()
        # Valida que el contenedor de la tarifa Comfort tenga la clase activa o esté visible
        assert routes_page.get_active_tariff() == 'Comfort'

    # 3. Rellenar el número de teléfono
    def test_3_fill_phone_number(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.fill_phone_number(data.phone_number)
        # Valida que el botón del teléfono guarde el estado del número ingresado
        assert routes_page.get_phone_number() == data.phone_number

    # 4. Agregar tarjeta de crédito
    def test_4_add_credit_card(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.add_credit_card(data.card_number, data.card_code)
        # Valida que el texto del método de pago se actualice
        assert routes_page.get_payment_method() == 'Tarjeta'

    # 5. Escribir el mensaje para el conductor
    def test_5_write_driver_comment(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.write_driver_comment(data.message_for_driver)
        assert routes_page.get_driver_comment() == data.message_for_driver

    # 6. Pedir manta y pañuelos
    def test_6_order_blanket_and_tissues(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.order_blanket_and_tissues()
        assert routes_page.is_blanket_selected() is True

    # 7. Pedir 2 helados
    def test_7_order_two_ice_creams(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.order_two_ice_creams()
        assert routes_page.get_ice_cream_count() == "2", "El contador de helados no es igual a 2"

    # 8. Pedir el taxi (Se abre el modal de búsqueda)
    def test_8_click_order_taxi(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.click_order_taxi()
        assert self.driver.find_element(*UrbanRoutesPage.order_modal_header).is_displayed()

    # 9. Ver la tarjeta del conductor asignado
    def test_9_driver_info_appears(self):
        wait_advanced = WebDriverWait(self.driver, 40)
        driver_assigned = wait_advanced.until(EC.visibility_of_element_located(UrbanRoutesPage.driver_info_modal))
        assert driver_assigned.is_displayed(), "No se mostró la información del viaje del conductor asignado"

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()