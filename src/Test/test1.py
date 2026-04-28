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
        wait = WebDriverWait(driver, 30)
        
        # 1. Navegación directa para evitar errores de menú
        driver.get("http://opencart.abstracta.us/index.php?route=account/register")
        print(f"Página cargada: {driver.title}")

        # 2. Datos inequívocos
        random_id = random.randint(10000, 99999)
        user_email = f"tester.qa.{random_id}@gmail.com"
        
        # 3. Llenado asegurando visibilidad
        first_name = wait.until(EC.visibility_of_element_located((By.ID, "input-firstname")))
        first_name.send_keys("Sergio")
        driver.find_element(By.ID, "input-lastname").send_keys("Automation")
        driver.find_element(By.ID, "input-email").send_keys(user_email)
        driver.find_element(By.ID, "input-telephone").send_keys("3101234567") # Formato estándar
        
        secure_pass = "Complex.Pass.2026!"
        driver.find_element(By.ID, "input-password").send_keys(secure_pass)
        driver.find_element(By.ID, "input-confirm").send_keys(secure_pass)

        # 4. ACCIÓN DOBLE: Forzamos el check de privacidad de dos formas
        agree_checkbox = driver.find_element(By.NAME, "agree")
        driver.execute_script("arguments[0].scrollIntoView(true);", agree_checkbox)
        driver.execute_script("arguments[0].click();", agree_checkbox)
        if not agree_checkbox.is_selected(): # Si falló el clic, lo marcamos por propiedad
            driver.execute_script("arguments[0].checked = true;", agree_checkbox)

        # 5. Envío del formulario
        continue_button = driver.find_element(By.CSS_SELECTOR, "input.btn-primary")
        driver.execute_script("arguments[0].click();", continue_button)

        # 6. Validación definitiva
        try:
            # Esperamos a que el texto 'Created' aparezca en cualquier lugar del body
            wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "Your Account Has Been Created!"))
            print(f"¡REGISTRO EXITOSO! Usuario: {user_email}")
        except:
            print("--- DIAGNÓSTICO DE FALLO ---")
            # Leemos los mensajes de error reales que el sitio pone en pantalla
            alert_danger = driver.find_elements(By.CLASS_NAME, "alert-danger")
            for alert in alert_danger:
                print(f"ALERTA DEL SITIO: {alert.text}")
            
            text_errors = driver.find_elements(By.CLASS_NAME, "text-danger")
            for error in text_errors:
                print(f"CAMPO CON ERROR: {error.text}")
                
            driver.save_screenshot("captura_final_debug.png")
            raise Exception("El registro no fue exitoso. Revisa los errores del sitio arriba.")

        # Asegurar que la carpeta de imágenes exista relativa al script
        img_dir = os.path.join(os.path.dirname(__file__), "../../img")
        os.makedirs(img_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        driver.save_screenshot(os.path.join(img_dir, f"registro_exitoso_{timestamp}.png"))

    def tearDown(self):
        self.driver.quit()  

if __name__ == '__main__':
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output=r"..\reporthtmlrunner"))