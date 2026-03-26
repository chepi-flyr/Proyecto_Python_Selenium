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

class TestPractica(unittest.TestCase):
    def setUp(self):
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

    def test_open_cart(self):
        #Navegamos al sitio de prueba
        self.driver.get("http://opencart.abstracta.us/")
        print(f'Ingreso al sitio de la prueba: {self.driver.title}')

        #Realizamos el proceso de registro, navegando a la sección de registro.
        self.driver.find_element("xpath","//a[@title='My Account']").click()
        self.driver.find_element("xpath","//a[normalize-space()='Register']").click()

        #Esperamos de forma implícita hasta que los elementos estén disponibles para interactuar
        self.driver.implicitly_wait(10) 

        #Realizamos el proceso de registro de un nuevo usuario en el sitio de prueba encontrando
        #los elementos necesarios para el proceso de registro mediante los selectoresy realizando
        #las acciones necesarias para completar el proceso de registro
        self.driver.find_element("id","input-firstname").send_keys("Username")
        self.driver.find_element("id","input-lastname").send_keys("Lastname")
        self.driver.find_element("id","input-email").send_keys("user90@example.com")
        self.driver.find_element("id","input-telephone").send_keys("123456789")
        self.driver.find_element("css selector","#input-password").send_keys("password")
        self.driver.find_element("css selector","#input-confirm").send_keys("password")
        self.driver.find_element("xpath","//label[normalize-space()='Yes']").click()
        self.driver.find_element("name","agree").click()

        #Esperamos de forma implícita hasta que los elementos estén disponibles para interactuar
        self.driver.implicitly_wait(15) 

        #Realizamos el proceso de registro, haciendo clic en el botón de continuar para completar el proceso de registro
        self.driver.find_element("xpath","//input[@value='Continue']").click()

        #Esperamos de forma implícita hasta que los elementos estén disponibles para interactuar
        self.driver.implicitly_wait(15) 

        #Validamos que el proceso de registro se haya realizado exitosamente, encontrando el elemento que contiene el mensaje de registro exitoso
        #y comparando su texto con el mensaje esperado utilizando una aserción
        elementoText = self.driver.find_element("xpath","//p[contains(text(),'Congratulations! Your new account has been success')]").text
        print(f'El mensaje de registro exitoso es: {elementoText}')
        self.assertEqual(elementoText,"Congratulations! Your new account has been successfully created!","El mensaje de registro no coincide con el esperado")

        #Realizamos una captura de pantalla del resultado de la prueba,
        #guardando la imagen en una carpeta específica con un nombre que incluye un timestamp para evitar sobrescribir imágenes anteriores
        os.makedirs("../img/", exist_ok = True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"screenshot_{timestamp}.png"
        file_path = os.path.join("../img/",file_name)
        self.driver.save_screenshot(file_path)

def teardown(self):
    #Cerramos el navegador al finalizar la prueba
    self.driver.quit()  

#Ejecución de la prueba utilizando el runner de HTMLTestRunner para generar un reporte en formato HTML o 
#sin utilizar el runner para generar la información de la ejecución en consola, no ambos a la vez
if __name__ == '__main__':
    #unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output=r"..\reporthtmlrunner"))
    unittest.main()