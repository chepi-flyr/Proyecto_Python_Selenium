import unittest
import HtmlTestRunner
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By # AÑADIDO: Importación necesaria para selectores modernos
import os
from datetime import datetime

class TestPractica(unittest.TestCase):
    def setUp(self):
        options = Options()
        options.add_argument('start-maximized')
        
        # AÑADIDO: Modo Headless obligatorio para Jenkins y tamaño de ventana fijo
        options.add_argument('--headless')
        options.add_argument('--window-size=1920,1080')

        preferences = {
            "profile.default_content_settings.popups": 0,
            "directory_upgrade":True,
            "download.default_directory": r"C:\Users\dmefr\Downloads"
        }
        options.add_experimental_option("prefs", preferences)

        service = ChromeService(executable_path= ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        
        # CORREGIDO: La espera implícita se define UNA sola vez al inicio del navegador
        self.driver.implicitly_wait(10)

    def test_open_cart(self):
        self.driver.get("http://opencart.abstracta.us/")
        print(f'Ingreso al sitio de la prueba: {self.driver.title}')

        # CORREGIDO: Uso de sintaxis moderna "By.XPATH", "By.ID", etc.
        self.driver.find_element(By.XPATH, "//a[@title='My Account']").click()
        self.driver.find_element(By.XPATH, "//a[normalize-space()='Register']").click()

        self.driver.find_element(By.ID, "input-firstname").send_keys("Username")
        self.driver.find_element(By.ID, "input-lastname").send_keys("Lastname")
        self.driver.find_element(By.ID, "input-email").send_keys("user90@example.com") # OJO: Si corres el test 2 veces, este email dará error de duplicado
        self.driver.find_element(By.ID, "input-telephone").send_keys("123456789")
        self.driver.find_element(By.CSS_SELECTOR, "#input-password").send_keys("password")
        self.driver.find_element(By.CSS_SELECTOR, "#input-confirm").send_keys("password")
        self.driver.find_element(By.XPATH, "//label[normalize-space()='Yes']").click()
        self.driver.find_element(By.NAME, "agree").click()

        self.driver.find_element(By.XPATH, "//input[@value='Continue']").click()

        elementoText = self.driver.find_element(By.XPATH, "//p[contains(text(),'Congratulations! Your new account has been success')]").text
        print(f'El mensaje de registro exitoso es: {elementoText}')
        self.assertEqual(elementoText,"Congratulations! Your new account has been successfully created!","El mensaje de registro no coincide con el esperado")

        os.makedirs("../img/", exist_ok = True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"screenshot_{timestamp}.png"
        file_path = os.path.join("../img/",file_name)
        self.driver.save_screenshot(file_path)

    # CORREGIDO: Indentación correcta dentro de la clase y 'D' mayúscula
    def tearDown(self):
        self.driver.quit()  

if __name__ == '__main__':
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output=r"..\reporthtmlrunner"))