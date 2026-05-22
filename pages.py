from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from helpers import retrieve_phone_code

class UrbanRoutesPage:
    # --- Localizadores---
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    call_taxi_button = (By.XPATH, "//button[contains(text(), 'Pedir un taxi')]")
    comfort_tariff = (By.XPATH, "//div[contains(text(), 'Comfort')]")

    # Teléfono
    phone_button = (By.CLASS_NAME, "np-button")
    phone_input = (By.ID, "phone")
    next_button = (By.XPATH, "//button[contains(text(), 'Siguiente')]")
    confirm_code_input = (By.ID, "code")
    confirm_code_button = (By.XPATH, "//button[contains(text(), 'Confirmar')]")

    # Tarjeta de Crédito (Línea duplicada eliminada)
    payment_method_button = (By.CLASS_NAME, "pp-button")
    add_card_button = (By.XPATH, "//div[@class='pp-title' and contains(text(), 'Agregar tarjeta')]")
    card_number_input = (By.XPATH, "//input[@id='number' or @name='number']")
    card_cvv_input = (By.XPATH, "//div[@class='card-code-input']//input[@id='code']")
    link_card_button = (By.XPATH, "//button[@type='submit' and contains(text(), 'Agregar')]")
    close_payment_modal = (By.XPATH, "//div[contains(@class, 'payment-picker')]//button[contains(@class, 'close-button')]")

    # Requisitos Adicionales (comment_input cambiado a By.CSS_SELECTOR)
    comment_input = (By.CSS_SELECTOR, "input#comment")
    blanket_and_tissues_switch = (By.XPATH, "//*[contains(text(), 'Manta y pañuelos')]/..//span[@class='slider round'] | //*[contains(text(), 'Manta y pañuelos')]/following-sibling::div//span[contains(@class, 'slider')]")
    blanket_and_tissues_checkbox = (By.XPATH, "//*[contains(text(), 'Manta y pañuelos')]/..//input[@class='custom-cb']")
    ice_cream_plus_button = (By.XPATH, "//div[contains(text(), 'Helado')]/..//div[@class='counter-plus']")
    ice_cream_counter = (By.XPATH, "//div[contains(text(), 'Helado')]/..//div[@class='counter-value']")

    # Modales Finales
    order_taxi_final_button = (By.CLASS_NAME, "smart-button")
    order_modal_header = (By.CLASS_NAME, "order-header")
    driver_info_modal = (By.XPATH, "//div[contains(@class, 'order-number') or contains(text(), 'en camino') or contains(text(), 'estará aquí')]")

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

    # --- Métodos de Flujo ---
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

        sms_code = retrieve_phone_code(self.driver)

        self.wait.until(EC.visibility_of_element_located(self.confirm_code_input)).send_keys(sms_code)
        self.driver.find_element(*self.confirm_code_button).click()

    def add_credit_card(self, card_number, cvv_code):
        self.wait.until(EC.element_to_be_clickable(self.payment_method_button)).click()
        btn_agregar = self.wait.until(EC.presence_of_element_located(self.add_card_button))
        try:
            btn_agregar.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", btn_agregar)

        input_tarjeta = self.wait.until(EC.visibility_of_element_located(self.card_number_input))
        input_tarjeta.send_keys(card_number)

        cvv_field = self.wait.until(EC.visibility_of_element_located(self.card_cvv_input))
        cvv_field.send_keys(cvv_code)
        cvv_field.send_keys(Keys.TAB)

        self.wait.until(EC.element_to_be_clickable(self.link_card_button)).click()
        self.wait.until(EC.element_to_be_clickable(self.close_payment_modal)).click()

    def write_driver_comment(self, comment):
        self.wait.until(EC.visibility_of_element_located(self.comment_input)).send_keys(comment)

    def get_driver_comment(self):
        return self.driver.find_element(*self.comment_input).get_attribute('value')

    def order_blanket_and_tissues(self):
        self.wait.until(EC.element_to_be_clickable(self.blanket_and_tissues_switch)).click()

    def is_blanket_selected(self):
        return self.driver.find_element(*self.blanket_and_tissues_switch).is_displayed()

    def order_two_ice_creams(self):
        plus_btn = self.wait.until(EC.element_to_be_clickable(self.ice_cream_plus_button))
        plus_btn.click()
        plus_btn.click()

    def click_order_taxi(self):
        self.wait.until(EC.element_to_be_clickable(self.order_taxi_final_button)).click()

    def get_ice_cream_count(self):
        return self.driver.find_element(*self.ice_cream_counter).text