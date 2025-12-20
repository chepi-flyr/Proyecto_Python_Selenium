import unittest
import HtmlTestRunner
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time
import os
from datetime import datetime
import allure

class TestPractica(unittest.TestCase):
    @allure.feature("Pruebas de Login")
    @allure.story("Validacion de titulo de pagina despues del login")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description_html("""
    <p>Esta prueba automatiza el proceso de login en el sitio OpenCart y valida que el titulo de la pagina sea correcto despues del login.</p>
    """)

    def setUp(self):
        with allure.step("Configuracion del entorno de prueba"):
            option = Options()
            preferences = {
                "profile.default_content_settings.popups": 0,
                "directory_upgrade":True,
                "download.default_directory": r"C:\Users\dmefr\Downloads\ClaseSelenium"
            }
            option.add_experimental_option("prefs",preferences)
            option.add_argument('start-maximized')
            #option.add_argument("--headless")

            service = ChromeService(executable_path= ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service = service, options=option)
            print("Inicia la prueba")

    def test_busqueda_mercado_libre(self): 
        with allure.step("Navegacion al sitio de prueba"):
            self.driver.get("https://www.mercadolibre.co.cr/")
            print(f'Ingreso al sitio de la prueba: {self.driver.title}')

        with allure.step("Realizacion de busqueda"):
            self.driver.find_element("xpath","//input[@id='cb1-edit']").send_keys("Laptop")
            allure.attach(self.driver.get_screenshot_as_png(),"Evidencia",allure.attachment_type.PNG)
            
        with allure.step("Busqueda realizada"):
            self.driver.find_element("xpath","//input[@id='cb1-edit']").send_keys(Keys.ENTER)
            print(f'Realizo la busqueda de Laptop')
            allure.attach(self.driver.get_screenshot_as_png(),"Evidencia",allure.attachment_type.PNG)

        with allure.step("Validacion de productos encontrados"):
            producto = self.driver.find_element("xpath","//a[contains(text(),'Lenovo Ideapad Slim 3 Gen 8 - Ordenador Portátil 1')]").text
            print(f'Producto encontrado: {producto}')
            self.assertEqual("Lenovo Ideapad Slim 3 Gen 8 - Ordenador Portátil 15.6''", producto, "Producto no encontrado")
            allure.attach(self.driver.get_screenshot_as_png(),"Evidencia",allure.attachment_type.PNG)

        with allure.step("Captura de pantalla despues del login"):
            os.makedirs("../img/", exist_ok = True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_name = f"screenshot_{timestamp}.png"
            file_path = os.path.join("../img/",file_name)
            self.driver.save_screenshot(file_path)

    def test_completar_seleccion_radiobutton_demo_qa(self):
        with allure.step("Navegacion al sitio de demo QA"):
            self.driver.get("https://demoqa.com/radio-button")
            print(f'Ingreso al sitio de demo QA: {self.driver.title}')

        with allure.step("Seleccion de opcion en radio button"):
            self.driver.find_element("xpath","//label[normalize-space()='Impressive']").click()
            print(f'Seleccion de Radio Button')
            time.sleep(3)

        #en modal que se abre, validar seleccion
        with allure.step("Validacion de seleccion de radio button"):
            selected_text = self.driver.find_element("xpath","//label[normalize-space()='Impressive']").text
            self.assertEqual(selected_text, "Impressive", "Radio button selection failed")
            allure.attach(self.driver.get_screenshot_as_png(), "Radio Button Selection Evidence", allure.attachment_type.PNG)

        with allure.step("Captura de pantalla despues del login"):
            os.makedirs("../img/", exist_ok = True)#Cambio realizado
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_name = f"screenshot_{timestamp}.png"
            file_path = os.path.join("../img/",file_name)#Cambio realizado
            self.driver.save_screenshot(file_path)

    def test_completar_textbox_demo_qa(self):
        with allure.step("Navegacion al sitio de demo QA Text Box"):
            self.driver.get("https://demoqa.com/text-box")
            print(f'Ingreso al sitio de demo QA Text Box: {self.driver.title}')

        with allure.step("Completando el formulario de Text Box"):
            self.driver.find_element("id","userName").send_keys("Juan Perez")
            self.driver.find_element("xpath","//input[@id='userEmail']").send_keys("d@d.com")
            self.driver.find_element("xpath","//textarea[@id='currentAddress']").send_keys("Direccion Actual")
            self.driver.find_element("xpath","//textarea[@id='permanentAddress']").send_keys("Direccion Permanente")
            self.driver.find_element("id","submit").click()
            print(f'Formulario de Text Box completado')
            time.sleep(3)
            allure.attach(self.driver.get_screenshot_as_png(), "Text Box Form Evidence", allure.attachment_type.PNG)

        with allure.step("Validacion de datos ingresados en Text Box"):
            name_output = self.driver.find_element("id","name").text
            email_output = self.driver.find_element("id","email").text
            current_address_output = self.driver.find_element("xpath","//p[@id='currentAddress']").text
            permanent_address_output = self.driver.find_element("xpath","//p[@id='permanentAddress']").text

            self.assertIn("Juan Perez", name_output, "Valor Incorrecto en el nombre")
            self.assertIn("d@d.com", email_output, "Valor incorrecto en el email")
            self.assertIn("Direccion Actual", current_address_output, "Valor incorrecto en la direccion actual")
            self.assertIn("Direccion Permanente", permanent_address_output, "Valor incorrecto en la direccion permanente")

        with allure.step("Captura de pantalla despues del Text Box"):
            os.makedirs("../img/", exist_ok = True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_name = f"screenshot_{timestamp}.png"
            file_path = os.path.join("../img/",file_name)
            self.driver.save_screenshot(file_path)

    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    unittest.main()