# Proyecto de Automatización: Urban Routes (QA)

Este proyecto forma parte del sprint 9 de automatización de pruebas para la plataforma de servicios de transporte **Urban Routes**. 
El objetivo principal es validar de punta a punta (End-to-End) el flujo completo de reservación de un taxi, asegurando que todos 
los componentes críticos de la interfaz de usuario y los procesos en segundo plano funcionen correctamente.

---

## Estructura del Proyecto

El proyecto sigue estrictamente el patrón de diseño **Page Object Model (POM)**, modularizando el código en componentes independientes:

* **`main.py`:** Contiene la suite de pruebas automatizadas (`TestUrbanRoutes`) estructurada en métodos secuenciales e independientes.
* **`pages.py`:** Aloja la clase `UrbanRoutesPage` con la definición de localizadores y los métodos de interacción con la interfaz de usuario.
* **`helpers.py`:** Contiene funciones utilitarias de soporte para las pruebas, aislando procesos complejos de red.
* **`data.py`:** Centraliza todos los datos de prueba, URLs y configuraciones dinámicas para evitar el hardcoding.

---

## Tecnologías y Técnicas Utilizadas

* **Lenguaje de Programación:** Python 3.x
* **Framework de Pruebas:** Pytest (para la ejecución, reporte y estructuración de los casos de prueba)
* **Herramienta de Automatización:** Selenium WebDriver (versión 4.x)
* **Patrón de Diseño:** **Page Object Model (POM)**, desacoplando los selectores del flujo lógico de verificación.
* **Tipos de Localizadores Aplicados:** Uso balanceado de selectores estratégicos para robustecer las búsquedas (`By.ID`, `By.CLASS_NAME`, `By.XPATH`, y `By.CSS_SELECTOR`).
* **Sincronización:** Implementación consistente de esperas explícitas (`WebDriverWait` y `expected_conditions`) para mitigar la latencia en la carga de modales.
* **Intercepción de Red:** Captura de registros de rendimiento de Chrome para interceptar de manera dinámica el código de confirmación SMS.

---

## Casos de Prueba Automatizados

La suite de pruebas en `main.py` fue refactorizada en métodos secuenciales e independientes para garantizar la visibilidad individual de cada aserción en los reportes de Pytest:

1.  **`test_1_set_route`:** Configura las direcciones de origen/destino y valida que los campos almacenen los valores correctos.
2.  **`test_2_select_comfort_tariff`:** Selecciona la tarifa Comfort y verifica la correcta transición visual del plan.
3.  **`test_3_fill_phone_number`:** Abre el modal de teléfono, ingresa el número de prueba, intercepta el código SMS de confirmación y valida el guardado.
4.  **`test_4_add_credit_card`:** Vincula una tarjeta de crédito rellenando los campos del modal y gestionando la pérdida de enfoque del CVV mediante `Keys.TAB` para activar el botón de enlace.
5.  **`test_5_write_driver_comment`:** Escribe un mensaje dinámico para el conductor y comprueba que el input retenga el texto esperado.
6.  **`test_6_order_blanket_and_tissues`:** Activa el switch de requisitos adicionales (manta y pañuelos) y valida su visibilidad y estado.
7.  **`test_7_order_two_ice_creams`:** Agrega dos helados al pedido mediante interacciones controladas sobre el contador y valida que el string del elemento marque exactamente `"2"`.
8.  **`test_8_click_order_taxi`:** Presiona el botón final de solicitud, desplegando el modal de búsqueda de automóvil.
9.  **`test_9_driver_info_appears`:** Aplica una espera avanzada (timeout extendido) para verificar la correcta asignación del conductor y la aparición de su tarjeta informativa.

---

## Instrucciones para Ejecutar las Pruebas

### 1. Prerrequisitos
Asegúrate de tener instalado Python en tu sistema y un entorno virtual configurado.

### 2. Instalar Dependencias
Instala los paquetes necesarios en tu entorno virtual ejecutando:
```bash
pip install selenium pytest

3. Ejecución desde la Terminal
Para correr todas las pruebas del proyecto y ver un resumen detallado paso a paso, ejecuta el siguiente comando en la raíz del directorio:

Bash
pytest main.py -v
4. Ejecución en PyCharm
Abre el proyecto en PyCharm.

Asegúrate de que el intérprete del proyecto apunte a tu entorno virtual (.venv).

Haz clic derecho sobre el archivo main.py y selecciona Run 'pytest in main.py'.

Automation Project: Urban Routes (QA)
This project is part of the test automation sprint 9 for the Urban Routes transportation service platform. The main objective is to validate the complete taxi booking flow from end to end (E2E), ensuring that all critical user interface components and background processes function correctly.

Project Structure
The repository strictly adheres to the Page Object Model (POM) design pattern, modularizing the code into separate components:

main.py: Contains the automated test suite (TestUrbanRoutes) structured into sequential and independent test methods.

pages.py: Houses the UrbanRoutesPage class, containing locator definitions and UI interaction methods.

helpers.py: Contains utility functions supporting the tests, isolating network log processing.

data.py: Centralizes all test data, URLs, and variables to prevent hardcoding.

Technologies and Techniques Used
Programming Language: Python 3.x

Testing Framework: Pytest (for test execution, reporting, and structuring)

Automation Tool: Selenium WebDriver (version 4.x)

Design Pattern: Page Object Model (POM), decoupling selectors from the logical verification flow.

Locator Types Applied: Balanced use of strategic locators to reinforce element queries (By.ID, By.CLASS_NAME, By.XPATH, and By.CSS_SELECTOR).

Synchronization: Consistent implementation of explicit waits (WebDriverWait and expected_conditions) to mitigate latency during modal transitions.

Network Interception: Capturing Chrome performance logs to dynamically retrieve the SMS confirmation code.

Automated Test Cases
The test suite in main.py has been refactored into independent methods to ensure clean, isolated assertion reporting in Pytest:

test_1_set_route: Sets the origin/destination addresses and validates that the fields store the correct values.

test_2_select_comfort_tariff: Selectes the Comfort tariff and verifies the correct visual plan transition.

test_3_fill_phone_number: Opens the phone modal, inputs the test number, intercepts the confirmation SMS code, and validates that it is successfully saved.

test_4_add_credit_card: Links a credit card by filling in the modal fields and handles losing focus on the CVV using Keys.TAB to activate the link button.

test_5_write_driver_comment: Writes a dynamic message for the driver and checks that the input field holds the expected text.

test_6_order_blanket_and_tissues: Toggles the additional requirements switch (blanket and tissues) and validates its visibility and state.

test_7_order_two_ice_creams: Adds two ice creams through controlled counter clicks and asserts the counter string displays exactly "2".

test_8_click_order_taxi: Submits the final taxi request, triggering the vehicle search modal display.

test_9_driver_info_appears: Applies an advanced explicit wait (extended timeout) to verify successful driver assignment and the appearance of the driver info card.

Instructions to Run the Tests
1. Prerequisites
Make sure you have Python installed on your system and a virtual environment configured.

2. Install Dependencies
Install the required packages in your virtual environment by running:

Bash
pip install selenium pytest
3. Execution from the Terminal
To run all the tests in the project and see a clean, verbose summary, execute the following command in the root directory:

Bash
pytest main.py -v
4. Execution in PyCharm
Open the project in PyCharm.

Ensure the project interpreter points to your virtual environment (.venv).

Right-click on the main.py file and select Run 'pytest in main.py'.