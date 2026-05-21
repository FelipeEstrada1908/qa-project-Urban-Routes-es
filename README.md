# Proyecto de Automatización: Urban Routes (QA)

Este proyecto forma parte del sprint 9 automatización de pruebas para la plataforma de servicios de transporte **Urban Routes**. El objetivo principal es validar de punta a punta (End-to-End) el flujo completo de reservación de un taxi, asegurando que todos los componentes críticos de la interfaz de usuario y los procesos en segundo plano funcionen correctamente.

---

## Tecnologías y Técnicas Utilizadas

* **Lenguaje de Programación:** Python 3.x
* **Framework de Pruebas:** Pytest (para la ejecución y estructuración de los casos de prueba)
* **Herramienta de Automatización:** Selenium WebDriver (versión 4.x)
* **Patrón de Diseño:** **Page Object Model (POM)**, separando la lógica de los selectores y métodos de la página (`UrbanRoutesPage`) de la lógica de las pruebas (`TestUrbanRoutes`).
* **Manejo de Datos Dinámicos:** Archivo de configuración centralizado (`data.py`) para mantener las variables de prueba limpias y separadas del código.
* **Técnicas Avanzadas:** * Sincronización mediante esperas explícitas (`WebDriverWait` y `expected_conditions`).
    * Intercepción de llamadas de red simuladas (logs de rendimiento de Chrome) para capturar códigos de confirmación por SMS de forma dinámica.
    * Inyección de scripts de JavaScript para clics forzados en elementos complejos de la interfaz.

---

## Casos de Prueba Automatizados

El script incluye los siguientes escenarios de prueba dentro de la suite:

1.  **`test_set_route`:** Valida la correcta configuración de las direcciones de origen y destino, asegurando que el botón para pedir el taxi se vuelva interactivo.
2.  **`test_complete_taxi_booking_flow`:** Cubre el flujo feliz completo:
    * Selección de tarifa (Comfort).
    * Vinculación de número telefónico e intercepción del código SMS.
    * Asignación y validación del modal de tarjeta de crédito.
    * Adición de comentarios para el conductor.
    * Activación de requisitos adicionales (Manta, pañuelos y contador de helados).
    * Confirmación final y espera de asignación de chofer.

---

## Instrucciones para Ejecutar las Pruebas

### 1. Prerrequisitos
Asegúrate de tener instalado Python en tu sistema y un entorno virtual configurado.

### 2. Instalar Dependencias
Instala los paquetes necesarios en tu entorno virtual ejecutando:
```bash
pip install selenium pytest

## Ejecución desde la Terminal
Para correr todas las pruebas del proyecto y ver un resumen limpio, ejecuta el siguiente comando en la raíz del directorio:
pytest main.py -v

## Ejecución en PyCharm
-Abre el proyecto en PyCharm.
-Asegúrate de que el intérprete del proyecto apunte a tu entorno virtual (.venv).
-Haz clic derecho sobre el archivo main.py y selecciona Run 'pytest in main.py'.

---

# Automation Project: Urban Routes (QA)

This project is part of Sprint 9, focusing on test automation for the **Urban Routes** transportation service platform. The main objective is to validate the complete taxi booking flow from end to end (E2E), ensuring that all critical user interface components and background processes function correctly.

---

## Technologies and Techniques Used

* **Programming Language:** Python 3.x
* **Testing Framework:** Pytest (for test execution and structuring)
* **Automation Tool:** Selenium WebDriver (version 4.x)
* **Design Pattern:** **Page Object Model (POM)**, separating page selectors and methods (`UrbanRoutesPage`) from the actual test logic (`TestUrbanRoutes`).
* **Dynamic Data Handling:** Centralized configuration file (`data.py`) to keep test variables clean and separated from the code.
* **Advanced Techniques:**
    * Synchronization using explicit waits (`WebDriverWait` and `expected_conditions`).
    * Interception of simulated network calls (Chrome performance logs) to dynamically capture SMS confirmation codes.
    * JavaScript script injection for forced clicks on complex UI elements.

---

## Automated Test Cases

The script includes the following test scenarios within the suite:

1. **`test_set_route`:** Validates the correct configuration of the origin and destination addresses, ensuring the "Call a taxi" button becomes interactive.
2. **`test_complete_taxi_booking_flow`:** Covers the complete happy path:
    * Selecting the tariff (Comfort).
    * Linking a phone number and intercepting the SMS confirmation code.
    * Adding and validating the credit card modal.
    * Writing a message/comment for the driver.
    * Ordering additional requirements (Blanket, tissues, and ice cream counter).
    * Final booking confirmation and waiting for driver assignment.

---

## Instructions to Run the Tests

### 1. Prerequisites
Make sure you have Python installed on your system and a virtual environment configured.

### 2. Install Dependencies
Install the required packages in your virtual environment by running:
```bash
pip install selenium pytest

## Execution from the Terminal
To run all the tests in the project and see a clean summary, execute the following command in the root directory:
pytest main.py -v

## Execution in PyCharm
-Open the project in PyCharm.
-Ensure the project interpreter points to your virtual environment (.venv).
-Right-click on the main.py file and select Run 'pytest in main.py'.

