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
from selenium.webdriver.common.keys import Keys

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
        wait = WebDriverWait(driver, 25)
        
        driver.get("http://opencart.abstracta.us/index.php?route=account/register")
        print(f"DEBUG - Título inicial: {driver.title}")

        user_email = f"qa.master.{random.randint(10000, 999999)}@testing.com"
        
        # Llenado robusto
        wait.until(EC.presence_of_element_located((By.ID, "input-firstname"))).send_keys("Sergio")
        driver.find_element(By.ID, "input-lastname").send_keys("Castaño")
        driver.find_element(By.ID, "input-email").send_keys(user_email)
        driver.find_element(By.ID, "input-telephone").send_keys("12345678")
        
        pass_val = "Pass.2026.Success!"
        driver.find_element(By.ID, "input-password").send_keys(pass_val)
        driver.find_element(By.ID, "input-confirm").send_keys(pass_val)

        # Clics forzados
        agree = driver.find_element(By.NAME, "agree")
        driver.execute_script("arguments[0].click();", agree)
        
        # En lugar de Enter, probamos el clic de JS en el botón específico
        btn = driver.find_element(By.CSS_SELECTOR, "input.btn-primary")
        driver.execute_script("arguments[0].click();", btn)

        try:
            # Esperamos 15 segundos a que la URL cambie
            wait.until(EC.url_contains("success"))
            print(f"REGISTRO EXITOSO para: {user_email}")
        except:
            # SI FALLA, ESTO NOS DIRÁ LA VERDAD:
            print(f"DEBUG - URL al fallar: {driver.current_url}")
            print(f"DEBUG - Título al fallar: {driver.title}")
            
            # Buscamos alertas rojas de OpenCart
            alertas = driver.find_elements(By.CSS_SELECTOR, ".alert, .text-danger")
            for a in alertas:
                print(f"MENSAJE DEL SITIO: {a.text}")
            
            driver.save_screenshot("EVIDENCIA_FALLO_FINAL.png")
            raise Exception("El sitio mostró errores o no redirigió.")

        # Asegurar que la carpeta de imágenes exista relativa al script
        img_dir = os.path.join(os.path.dirname(__file__), "../../img")
        os.makedirs(img_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        driver.save_screenshot(os.path.join(img_dir, f"registro_exitoso_{timestamp}.png"))

    def tearDown(self):
        self.driver.quit()  

if __name__ == '__main__':
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output=r"..\reporthtmlrunner"))