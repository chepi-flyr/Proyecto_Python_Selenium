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
@allure.story(u'Realizar Registro y Login')
@allure.testcase(u'Test Case')
@allure.severity(allure.severity_level.CRITICAL)
@allure.description(u"""Caso de prueba para verificar el</br> login y </br> registro en el aplicativo web de pruebas""")
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