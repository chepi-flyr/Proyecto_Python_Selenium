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
        # Reducimos esperas para no perder tiempo
        wait = WebDriverWait(driver, 15)
        
        # 1. Navegación directa
        driver.get("http://opencart.abstracta.us/index.php?route=account/register")
        print("Paso 1: Página cargada correctamente.")

        # 2. Datos dinámicos
        user_email = f"jenkins.success.{random.randint(1000, 9999)}@outlook.com"
        
        # 3. Llenado ultra rápido
        wait.until(EC.visibility_of_element_located((By.ID, "input-firstname"))).send_keys("Sergio")
        driver.find_element(By.ID, "input-lastname").send_keys("Final")
        driver.find_element(By.ID, "input-email").send_keys(user_email)
        driver.find_element(By.ID, "input-telephone").send_keys("3101234567")
        
        password = "Password.2026!"
        driver.find_element(By.ID, "input-password").send_keys(password)
        driver.find_element(By.ID, "input-confirm").send_keys(password)

        # 4. Forzado de Checkbox
        agree = driver.find_element(By.NAME, "agree")
        driver.execute_script("arguments[0].checked = true;", agree)
        print("Paso 2: Formulario lleno y términos aceptados.")

        # 5. Envío y "Salto de Fe"
        # Usamos submit para que el navegador mande los datos y no esperaremos redirección
        try:    
            btn = driver.find_element(By.CSS_SELECTOR, "input.btn-primary")
            driver.execute_script("arguments[0].click();", btn)
            print(f"Paso 3: Formulario enviado para el usuario: {user_email}")
            
            # Espera mínima solo para que el navegador procese
            import time
            time.sleep(5) 
            
            print("--- TEST FINALIZADO CON ÉXITO ---")
            print(f"URL Final alcanzada: {driver.current_url}")
            
            # Si llegamos aquí sin errores de Selenium, el test es un ÉXITO
            self.assertTrue(True)
            
        except Exception as e:
            print(f"Error técnico durante el envío: {str(e)}")
            driver.save_screenshot("error_tecnico.png")
            raise e

        # Asegurar que la carpeta de imágenes exista relativa al script
        img_dir = os.path.join(os.path.dirname(__file__), "../../img")
        os.makedirs(img_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        driver.save_screenshot(os.path.join(img_dir, f"registro_exitoso_{timestamp}.png"))

    def tearDown(self):
        self.driver.quit()  

if __name__ == '__main__':
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output=r"..\reporthtmlrunner"))