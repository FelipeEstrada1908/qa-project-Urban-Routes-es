from typing import Literal

import data
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


# no modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""
    import json
    import time
    from selenium.common import WebDriverException
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
        return code


class UrbanRoutesPage:
    # --- Localizadores Base ---
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')

    # --- Localizadores del Entregable ---
    call_taxi_button = (By.XPATH, "//button[contains(text(), 'Pedir un taxi')]")
    comfort_tariff = (By.XPATH, "//div[contains(text(), 'Comfort')]")

    # Teléfono
    phone_button = (By.CLASS_NAME, "np-button")
    phone_input = (By.ID, "phone")
    next_button = (By.XPATH, "//button[contains(text(), 'Siguiente')]")
    confirm_code_input = (By.ID, "code")
    confirm_code_button = (By.XPATH, "//button[contains(text(), 'Confirmar')]")

    # Tarjeta de Crédito
    payment_method_button = (By.CLASS_NAME, "pp-button")
    payment_method_button = (By.CLASS_NAME, "pp-button")
    add_card_button = (By.XPATH, "//div[@class='pp-title' and contains(text(), 'Agregar tarjeta')]")
    card_number_input = (By.XPATH, "//input[@id='number' or @name='number']")
    card_cvv_input = (By.XPATH, "//div[@class='card-code-input']//input[@id='code']")
    link_card_button = (By.XPATH, "//button[@type='submit' and contains(text(), 'Agregar')]")
    close_payment_modal = (By.XPATH, "//div[contains(@class, 'payment-picker')]//button[contains(@class, 'close-button')]")

    # Requisitos Adicionales
    comment_input = (By.ID, "comment")
    blanket_and_tissues_switch = (By.XPATH, "//*[contains(text(), 'Manta y pañuelos')]/..//span[@class='slider round'] | //*[contains(text(), 'Manta y pañuelos')]/following-sibling::div//span[contains(@class, 'slider')]")
    ice_cream_plus_button = (By.XPATH, "//div[contains(text(), 'Helado')]/..//div[@class='counter-plus']")
    ice_cream_counter = (By.XPATH, "//div[contains(text(), 'Helado')]/..//div[@class='counter-value']")

    # Modales Finales
    order_taxi_final_button = (By.CLASS_NAME, "smart-button")
    order_modal_header = (By.CLASS_NAME, "order-header")
    driver_info_modal = (By.XPATH,
                         "//div[contains(@class, 'order-number') or contains(text(), 'en camino') or contains(text(), 'estará aquí')]")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # --- Métodos Base ---
    def set_from(self, from_address):
        self.driver.find_element(*self.from_field).send_keys(from_address)

    def set_to(self, to_address):
        self.driver.find_element(*self.to_field).send_keys(to_address)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    # --- Métodos de Flujo Avanzado ---
    def set_route(self, from_address, to_address):
        self.wait.until(EC.visibility_of_element_located(self.from_field)).send_keys(from_address)
        self.driver.find_element(*self.to_field).send_keys(to_address)
        self.wait.until(EC.element_to_be_clickable(self.call_taxi_button)).click()

    def select_comfort_tariff(self):
        comfort = self.wait.until(EC.element_to_be_clickable(self.comfort_tariff))
        comfort.click()

    def fill_phone_number(self, phone_number):
        self.wait.until(EC.element_to_be_clickable(self.phone_button)).click()
        self.wait.until(EC.visibility_of_element_located(self.phone_input)).send_keys(phone_number)
        self.driver.find_element(*self.next_button).click()

        # Intercepta el SMS inyectando el driver actual
        sms_code = retrieve_phone_code(self.driver)

        self.wait.until(EC.visibility_of_element_located(self.confirm_code_input)).send_keys(sms_code)
        self.driver.find_element(*self.confirm_code_button).click()

    def add_credit_card(self, card_number, cvv_code):
        # 1. Abrir menú de métodos de pago
        self.wait.until(EC.element_to_be_clickable(self.payment_method_button)).click()

        # 2. Buscar botón "Agregar una tarjeta" e intentar clic robusto
        btn_agregar = self.wait.until(EC.presence_of_element_located(self.add_card_button))
        try:
            btn_agregar.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", btn_agregar)

        # 3. Llenar campos del modal de la tarjeta
        input_tarjeta = self.wait.until(EC.visibility_of_element_located(self.card_number_input))
        input_tarjeta.send_keys(card_number)

        cvv_field = self.wait.until(EC.visibility_of_element_located(self.card_cvv_input))
        cvv_field.send_keys(cvv_code)

        # TAB para quitar enfoque del CVV y activar botón 'Enlace'
        cvv_field.send_keys(Keys.TAB)

        # 4. Vincular y cerrar modal
        self.wait.until(EC.element_to_be_clickable(self.link_card_button)).click()
        self.wait.until(EC.element_to_be_clickable(self.close_payment_modal)).click()

    def write_driver_comment(self, comment):
        self.wait.until(EC.visibility_of_element_located(self.comment_input)).send_keys(comment)

    def order_blanket_and_tissues(self):
        self.wait.until(EC.element_to_be_clickable(self.blanket_and_tissues_switch)).click()

    def order_two_ice_creams(self):
        plus_btn = self.wait.until(EC.element_to_be_clickable(self.ice_cream_plus_button))
        plus_btn.click()
        plus_btn.click()

    def click_order_taxi(self):
        self.wait.until(EC.element_to_be_clickable(self.order_taxi_final_button)).click()

    def get_ice_cream_count(self):
        return self.driver.find_element(*self.ice_cream_counter).text


class TestUrbanRoutes:
    driver = None

    @classmethod
    def setup_class(cls):
        from selenium.webdriver.chrome.options import Options

        options = Options()
        options.set_capability("goog:loggingPrefs", {'performance': 'ALL'})

        cls.driver = webdriver.Chrome(options=options)
        cls.driver.maximize_window()

    def test_set_route(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to

    def test_complete_taxi_booking_flow(self):
        routes_page = UrbanRoutesPage(self.driver)

        # 2. Seleccionar la tarifa Comfort
        routes_page.select_comfort_tariff()

        # 3. Rellenar el número de teléfono con los datos de data.py
        routes_page.fill_phone_number(data.phone_number)

        # 4. Agregar tarjeta de crédito con los datos de data.py
        routes_page.add_credit_card(data.card_number, data.card_code)

        # 5. Escribir el mensaje dinámico para el controlador
        routes_page.write_driver_comment(data.message_for_driver)

        # 6. Pedir manta y pañuelos
        routes_page.order_blanket_and_tissues()

        # 7. Pedir 2 helados
        routes_page.order_two_ice_creams()
        assert routes_page.get_ice_cream_count() == "2", "El contador de helados no es igual a 2"

        # 8. Pedir el taxi (Se abre el modal de búsqueda)
        routes_page.click_order_taxi()
        assert self.driver.find_element(*UrbanRoutesPage.order_modal_header).is_displayed()

        # 9. PASO OPCIONAL: Esperar el contador y ver la tarjeta del conductor asignado
        wait_advanced = WebDriverWait(self.driver, 40)
        driver_assigned = wait_advanced.until(EC.visibility_of_element_located(UrbanRoutesPage.driver_info_modal))
        assert driver_assigned.is_displayed(), "No se mostró la información del viaje del conductor asignado"

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()