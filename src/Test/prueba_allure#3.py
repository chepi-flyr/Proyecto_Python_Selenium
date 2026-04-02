import unittest #Importamos el módulo unittest para crear y ejecutar pruebas unitarias, proporcionando una estructura para definir casos de prueba, configurar el entorno de prueba y realizar aserciones para validar los resultados de las pruebas.
import HtmlTestRunner #Importamos el módulo HtmlTestRunner para generar reportes en formato HTML de las pruebas realizadas, permitiendo una visualización más clara y detallada de los resultados de las pruebas con información sobre las pruebas 
                      #ejecutadas, los resultados obtenidos y cualquier error que haya ocurrido durante la ejecución de las pruebas.
from selenium import webdriver #Importamos la clase webdriver para controlar el navegador y realizar las acciones necesarias para la prueba
from selenium.webdriver.chrome.service import Service as ChromeService #Importamos la clase Service para configurar el servicio del navegador, indicando la ruta del driver
from selenium.webdriver.chrome.options import Options #Importamos la clase Options para configurar las opciones del navegador, como el modo headless o el tamaño de la ventana
from webdriver_manager.chrome import ChromeDriverManager #Importamos el ChromeDriverManager para gestionar la instalación y actualización del driver de Chrome de forma automática
from selenium.webdriver.common.keys import Keys #Importamos la clase Keys para simular la pulsación de teclas en el navegador
import os #Importamos el módulo os para interactuar con el sistema operativo, como crear directorios o guardar archivos
from datetime import datetime #Importamos la clase datetime para obtener la fecha y hora actual, utilizada para generar nombres de archivos únicos al guardar capturas de pantalla o reportes
import allure
import Functions_Utilitaries.Functions as Utilities #Importamos las funciones de captura de pantalla desde el módulo Functions para utilizarlas en la prueba, 
                                                                                             #permitiendo agregar capturas de pantalla a los reportes de Allure y guardar capturas de pantalla 
                                                                                             #en una carpeta específica durante la ejecución de la prueba.


@allure.feature(u'Pruebas')
@allure.story(u'Realizar Prueba en DemoQA')
@allure.testcase(u'Test Case')
@allure.severity(allure.severity_level.NORMAL)
@allure.description(u"""Esta prueba automatizada realiza el proceso de registro de un nuevo usuario en el sitio de prueba DemoQA, utilizando Selenium WebDriver
                        para interactuar con el navegador y realizar las acciones necesarias para completar el proceso de registro.""")
class Test(unittest.TestCase):

    def setUp(self):
        with allure.step(u'Paso 1: Preparar configuraciones instancia del navegador'):
            #Objeto en el cual se configuran las opciones del navegador
            options = Options()
            options.add_argument('start-maximized')
            #options.headless = True #Ejecuta el navegador en modo headless (sin interfaz gráfica)

            #Objeto en el cual se configura las preferencias del navegador
            preferences = {
                "profile.default_content_settings.popups": 0,
                "directory_upgrade":True,
                "download.default_directory": r"C:\Users\dmefr\Downloads"
            }
            #Agregamos las preferencias al objeto de opciones del navegador
            options.add_experimental_option("prefs", preferences)

            #Utilizamos sólo alguno de los servicios para configurar el driver, no ambos
            #Configuramos el servicio del navegador, indicando la ruta del driver
            #service = ChromeService(executable_path= "C:\Users\dmefr\OneDrive\Escritorio\Proyecto_Python_Selenium\src\Drivers\chromedriver.exe")
            #Configuramos el servicio del navegador, utilizando el webdriver manager para indicar el driver
            service = ChromeService(executable_path= ChromeDriverManager().install())
            
            #Inicializamos el driver del navegador, utilizando el servicio y las opciones configuradas
            self.driver = webdriver.Chrome(service=service, options=options)

    def test_demoQA_text_box(self):
        with allure.step(u"Paso 2: Navegar al sitio de la prueba"):
            #Navegar al sitio de la prueba
            self.driver.get("https://demoqa.com/text-box")
            print(f"Ingreso al sitio de la prueba: {self.driver.title}")

            #Agregamos una captura de pantalla del ingreso a la sección de registro, utilizando la función add_screenshot para agregar la captura de pantalla al reporte de Allure, 
            #y la función screenshot_test para guardar la captura de pantalla en una carpeta específica con un nombre que incluye un timestamp para evitar sobrescribir imágenes anteriores.
            Utilities.add_screenshot(self, "Ingreso a la seccion de registro")
            Utilities.screenshot_test(self)            
            #Esperamos de forma implícita hasta que los elementos estén disponibles para interactuar
            self.driver.implicitly_wait(10) 

        with allure.step(u"Paso 3: Ingresar datos en el campo Nombre del formulario"):
            self.driver.find_element("id","userName").send_keys("Prueba_Allure")
            
            #Agregamos una captura de pantalla del ingreso a la sección de registro, utilizando la función add_screenshot para agregar la captura de pantalla al reporte de Allure, 
            #y la función screenshot_test para guardar la captura de pantalla en una carpeta específica con un nombre que incluye un timestamp para evitar sobrescribir imágenes anteriores.
            Utilities.add_screenshot(self, "Ingreso a la seccion de registro")
            Utilities.screenshot_test(self)            
            #Esperamos de forma implícita hasta que los elementos estén disponibles para interactuar
            self.driver.implicitly_wait(10)
        
        with allure.step(u"Paso 4: Ingresar datos en el campo Email del formulario"):
            self.driver.find_element("xpath","//input[@id='userEmail']").send_keys("user975@example.com")
            
            #Agregamos una captura de pantalla del ingreso a la sección de registro, utilizando la función add_screenshot para agregar la captura de pantalla al reporte de Allure, 
            #y la función screenshot_test para guardar la captura de pantalla en una carpeta específica con un nombre que incluye un timestamp para evitar sobrescribir imágenes anteriores.
            Utilities.add_screenshot(self, "Ingreso a la seccion de registro")
            Utilities.screenshot_test(self)            
            #Esperamos de forma implícita hasta que los elementos estén disponibles para interactuar
            self.driver.implicitly_wait(10)
        
        with allure.step(u"Paso 5: Ingresar datos en el campo Dirección del formulario"):
            self.driver.find_element("css selector","#currentAddress").send_keys("Direccion Actual 123")
            
            #Agregamos una captura de pantalla del ingreso a la sección de registro, utilizando la función add_screenshot para agregar la captura de pantalla al reporte de Allure, 
            #y la función screenshot_test para guardar la captura de pantalla en una carpeta específica con un nombre que incluye un timestamp para evitar sobrescribir imágenes anteriores.
            Utilities.add_screenshot(self, "Ingreso a la seccion de registro")
            Utilities.screenshot_test(self)            
            #Esperamos de forma implícita hasta que los elementos estén disponibles para interactuar
            self.driver.implicitly_wait(10)

        with allure.step(u"Paso 6: Ingresar datos en el campo Dirección de Permanencia del formulario"):
            self.driver.find_element("xpath","//textarea[@id='permanentAddress']").send_keys("Permanencia 123")
            
            #Agregamos una captura de pantalla del ingreso a la sección de registro, utilizando la función add_screenshot para agregar la captura de pantalla al reporte de Allure, 
            #y la función screenshot_test para guardar la captura de pantalla en una carpeta específica con un nombre que incluye un timestamp para evitar sobrescribir imágenes anteriores.
            Utilities.add_screenshot(self, "Ingreso a la seccion de registro")
            Utilities.screenshot_test(self)            
            #Esperamos de forma implícita hasta que los elementos estén disponibles para interactuar
            self.driver.implicitly_wait(10)

        with allure.step(u"Paso 7: Hacer clic en el botón de enviar para completar el proceso de registro"):
            self.driver.find_element("id","submit").click()
            
            #Agregamos una captura de pantalla del ingreso a la sección de registro, utilizando la función add_screenshot para agregar la captura de pantalla al reporte de Allure, 
            #y la función screenshot_test para guardar la captura de pantalla en una carpeta específica con un nombre que incluye un timestamp para evitar sobrescribir imágenes anteriores.
            Utilities.add_screenshot(self, "Ingreso a la seccion de registro")
            Utilities.screenshot_test(self)            
            #Esperamos de forma implícita hasta que los elementos estén disponibles para interactuar
            self.driver.implicitly_wait(10)

        with allure.step(u'Paso 8: Validar que el proceso de registro se haya realizado exitosamente'):
            #Validamos que el proceso de registro se haya realizado exitosamente, encontrando el elemento que contiene el mensaje de registro exitoso
            textoElemento = self.driver.find_element("xpath","//p[@id='name']").text

        with allure.step(u"Paso 9: Capturar el resultado de la prueba"):
            
            #Agregamos una captura de pantalla del ingreso a la sección de registro, utilizando la función add_screenshot para agregar la captura de pantalla al reporte de Allure, 
            #y la función screenshot_test para guardar la captura de pantalla en una carpeta específica con un nombre que incluye un timestamp para evitar sobrescribir imágenes anteriores.
            Utilities.add_screenshot(self, "Ingreso a la seccion de registro")
            Utilities.screenshot_test(self)            
            #Esperamos de forma implícita hasta que los elementos estén disponibles para interactuar
            self.driver.implicitly_wait(10)

#Para ejecutar las pruebas Allure utilzamos los archivos .bat con los comandos necesarios para ejecutar las pruebas y generar los reportes de Allure.
#Estos archivos .bat se encuentran en la carpeta src del proyecto, y se pueden ejecutar haciendo doble clic sobre ellos o ejecutándolos desde la terminal.

#Para generar los reportes de Allure, utilizamos los siguientes comando en la terminal.
#Abrir el reporte Allure en carpeta temporal a partir de los resultados generados
#allure serve ../reports/allure-results
#allure serve allure-results

#Abrir el reporte Allure a partir de la carpeta allure report generada con los resultados
#allure generate ../reports/allure-results -o ../reports/allure-report --clean
#allure generate allure-results -o allure-report --clean
#allure open ../reports/allure-report

#Si da error al ejecutar la pruebas, verificar que la version de Allure-Pytest sea compatible con la version de Allure Commandline instalada en el equipo, para esto se pueden consultar 
#las versiones compatibles en la documentación oficial de Allure-Pytest.
#Allure Pytest version 2.15.3 y pytest en una version superior a la 8.0.0.

#En caso de necesitar actualizar la version de Allure-Pytest, se puede hacer utilizando el siguiente comando en la terminal: pip install --upgrade allure-pytest
#Revisan las librerias instaladas en el ambiente virtual creado para validar las versiones de las librerias instaladas, para esto pueden utilizar el comando pip list en la terminal,
#y verificar las versiones de allure-pytest y pytest instaladas en el ambiente virtual.
#Ejecución de la prueba utilizando el runner de HTMLTestRunner para generar un reporte en formato HTML o  sin utilizar el runner para generar la información de la ejecución en consola,
# no ambos a la vez.
if __name__ == '__main__':
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output=r"..\reporthtmlrunner"))
    #unittest.main()