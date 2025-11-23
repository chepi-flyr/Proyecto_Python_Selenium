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

class TestPractica(unittest.TestCase):
    def setUp(self):
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

    def test_validacion_titulo_pagina(self): 
        self.driver.get("https://opencart.abstracta.us/")
        print(f'Ingreso al sitio de la prueba: {self.driver.title}')

        self.driver.find_element("xpath","//a[@title='My Account']").click()
        self.driver.find_element("xpath","//a[normalize-space()='Login']").click()
        print(f'Pagina Login: {self.driver.title}')

        self.driver.find_element("xpath","//input[@id='input-email']").send_keys("dmefrain.52@gmail.com")
        self.driver.find_element("xpath","//input[@id='input-password']").send_keys("114660137")
        print(f'Ingreso Datos Login')

        self.driver.find_element("xpath","//input[@value='Login']").click()
        print(f'Login Exitoso')
        time.sleep(5)

        print(f'Validacion de Texto')
        self.assertEqual(self.driver.find_element("xpath","//h2[normalize-space()='My Account']").text,"My Account","Texto fallido")

        os.makedirs("src/img/", exist_ok = True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"screenshot_{timestamp}.png"
        file_path = os.path.join("src/img/",file_name)
        self.driver.save_screenshot(file_path)

    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output=r'src\reporthtmlrunner'))
    #unittest.main()