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
import random # NUEVO para el email.
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
        wait = WebDriverWait(driver, 20)
        import time # Añadido para pausas breves
        
        driver.get("http://opencart.abstracta.us/index.php?route=account/register")
        print(f'Ingreso al registro. Título: {driver.title}')

        # Datos dinámicos
        user_email = f"tester.automation.{random.randint(1000, 999999)}@gmail.com"
        
        # Llenado con pequeñas pausas para burlar bloqueos básicos
        wait.until(EC.visibility_of_element_located((By.ID, "input-firstname"))).send_keys("Sergio")
        time.sleep(0.5)
        driver.find_element(By.ID, "input-lastname").send_keys("Tester")
        driver.find_element(By.ID, "input-email").send_keys(user_email)
        driver.find_element(By.ID, "input-telephone").send_keys("3001234567")
        
        # Usamos una contraseña muy robusta
        secure_pass = "Automation.2026!"
        driver.find_element(By.ID, "input-password").send_keys(secure_pass)
        driver.find_element(By.ID, "input-confirm").send_keys(secure_pass)
        time.sleep(0.5)

        # Clics con JS para evitar problemas de visibilidad en Headless
        agree_check = driver.find_element(By.NAME, "agree")
        driver.execute_script("arguments[0].click();", agree_check)
        
        continue_btn = driver.find_element(By.XPATH, "//input[@value='Continue']")
        driver.execute_script("arguments[0].click();", continue_btn)

        # VALIDACIÓN MEJORADA
        try:
            # Esperamos a ver si la URL cambia
            wait.until(EC.url_contains("success"))
            print("¡Registro exitoso detectado por URL!")
        except:
            print("No se detectó redirección. Buscando mensajes de error en la página...")
            # Si no redirigió, buscamos los textos de error que pone OpenCart (clase text-danger)
            errors = driver.find_elements(By.CLASS_NAME, "text-danger")
            for err in errors:
                print(f"ERROR ENCONTRADO EN PÁGINA: {err.text}")
            
            # Guardamos captura para que la veas en el workspace de Jenkins
            driver.save_screenshot("DEBUG_REGISTRO_FALLIDO.png")
            raise Exception("El registro falló. Revisa los errores impresos arriba.")

        # Asegurar que la carpeta de imágenes exista relativa al script
        img_dir = os.path.join(os.path.dirname(__file__), "../../img")
        os.makedirs(img_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        driver.save_screenshot(os.path.join(img_dir, f"registro_exitoso_{timestamp}.png"))

    def tearDown(self):
        self.driver.quit()  

if __name__ == '__main__':
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output=r"..\reporthtmlrunner"))