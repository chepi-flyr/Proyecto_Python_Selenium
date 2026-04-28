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
        wait = WebDriverWait(driver, 25)
        import time
        
        # 1. Navegación directa
        driver.get("http://opencart.abstracta.us/index.php?route=account/register")
        
        # 2. Datos frescos y seguros
        user_email = f"auto.test.{random.randint(1000, 999999)}@gmail.com"
        password_final = "Secret.Pass.2026!" # Contraseña compleja e inequívoca

        # 3. Llenado con esperas precisas
        name_field = wait.until(EC.element_to_be_clickable((By.ID, "input-firstname")))
        name_field.send_keys("Sergio")
        driver.find_element(By.ID, "input-lastname").send_keys("QA")
        driver.find_element(By.ID, "input-email").send_keys(user_email)
        driver.find_element(By.ID, "input-telephone").send_keys("1234567890")
        
        driver.find_element(By.ID, "input-password").send_keys(password_final)
        driver.find_element(By.ID, "input-confirm").send_keys(password_final)

        # 4. Forzar Clics de Consentimiento con JavaScript (Garantiza éxito en Headless)
        # Política de privacidad
        agree = driver.find_element(By.NAME, "agree")
        driver.execute_script("arguments[0].checked = true;", agree)
        
        # Botón Continue
        submit = driver.find_element(By.CSS_SELECTOR, "input.btn-primary")
        driver.execute_script("arguments[0].click();", submit)

        # 5. Validación de Éxito
        try:
            # Esperamos a que el encabezado de éxito aparezca
            success_h1 = wait.until(EC.presence_of_element_located((By.XPATH, "//h1[contains(text(),'Created')]")))
            print(f"¡ÉXITO TOTAL!: {success_h1.text}")
        except:
            # Captura de errores visibles si no hubo éxito
            print("--- ERRORES DETECTADOS EN LA PÁGINA ---")
            page_errors = driver.find_elements(By.CLASS_NAME, "text-danger")
            for error in page_errors:
                print(f"ALERTA: {error.text}")
            
            driver.save_screenshot("captura_error_final.png")
            print(f"URL al fallar: {driver.current_url}")
            raise Exception("No se pudo completar el registro.")

        # Asegurar que la carpeta de imágenes exista relativa al script
        img_dir = os.path.join(os.path.dirname(__file__), "../../img")
        os.makedirs(img_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        driver.save_screenshot(os.path.join(img_dir, f"registro_exitoso_{timestamp}.png"))

    def tearDown(self):
        self.driver.quit()  

if __name__ == '__main__':
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output=r"..\reporthtmlrunner"))