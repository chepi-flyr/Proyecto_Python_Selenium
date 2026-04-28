import unittest
import HtmlTestRunner
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # NUEVO
from selenium.webdriver.support import expected_conditions as EC # NUEVO
import os
import random # NUEVO para el email
from datetime import datetime

class TestPractica(unittest.TestCase):
    def setUp(self):
        options = Options()
        options.add_argument('start-maximized')
        options.add_argument('--headless')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--no-sandbox') # Recomendado para Jenkins
        options.add_argument('--disable-dev-shm-usage') # Recomendado para Jenkins

        service = ChromeService(executable_path= ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)

    def test_open_cart(self):
        driver = self.driver
        wait = WebDriverWait(driver, 20) # Espera de hasta 20 segundos
        
        driver.get("http://opencart.abstracta.us/")
        print(f'Ingreso al sitio de la prueba: {driver.title}')

        # Navegación con esperas explícitas
        wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@title='My Account']"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='Register']"))).click()

        # Generamos un email aleatorio para que nunca falle por "usuario duplicado"
        user_email = f"testuser{random.randint(1, 99999)}@example.com"

        # Llenado de formulario con esperas
        wait.until(EC.visibility_of_element_identity((By.ID, "input-firstname"))).send_keys("Sergio")
        driver.find_element(By.ID, "input-lastname").send_keys("Castaño")
        driver.find_element(By.ID, "input-email").send_keys(user_email)
        driver.find_element(By.ID, "input-telephone").send_keys("123456789")
        driver.find_element(By.ID, "input-password").send_keys("Password123!")
        driver.find_element(By.ID, "input-confirm").send_keys("Password123!")
        
        driver.find_element(By.XPATH, "//label[normalize-space()='Yes']").click()
        driver.find_element(By.NAME, "agree").click()
        driver.find_element(By.XPATH, "//input[@value='Continue']").click()

        # Validación final
        success_msg = wait.until(EC.presence_of_element_located((By.XPATH, "//h1[contains(text(),'Your Account Has Been Created!')]"))).text
        print(f'Resultado: {success_msg}')
        
        self.assertIn("Created", success_msg)

        # Captura de pantalla
        os.makedirs("../img/", exist_ok = True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.driver.save_screenshot(f"../img/screenshot_{timestamp}.png")

    def tearDown(self):
        self.driver.quit()  

if __name__ == '__main__':
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output=r"..\reporthtmlrunner"))