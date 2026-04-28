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
        wait = WebDriverWait(driver, 30)
        
        # 1. Navegación directa
        driver.get("http://opencart.abstracta.us/index.php?route=account/register")
        
        # 2. Datos que parecen humanos
        random_num = random.randint(1000, 9999)
        user_email = f"sergio.qa.colombia{random_num}@outlook.com" # Cambiamos dominio a uno común
        
        # 3. Llenado con esperas
        wait.until(EC.visibility_of_element_located((By.ID, "input-firstname"))).send_keys("Sergio")
        driver.find_element(By.ID, "input-lastname").send_keys("Castano")
        driver.find_element(By.ID, "input-email").send_keys(user_email)
        driver.find_element(By.ID, "input-telephone").send_keys("3124567890") # Teléfono formato real
        
        secure_pass = "Prueba.2026.Jenkins!"
        driver.find_element(By.ID, "input-password").send_keys(secure_pass)
        driver.find_element(By.ID, "input-confirm").send_keys(secure_pass)

        # 4. Forzado de consentimiento (MUY IMPORTANTE)
        # Marcamos el checkbox directamente por su propiedad 'checked' para asegurar que el sitio lo vea
        agree_check = driver.find_element(By.NAME, "agree")
        driver.execute_script("arguments[0].checked = true;", agree_check)

        # 5. Envío mediante el método submit() del formulario completo
        # Esto es más potente que hacer clic en el botón
        registration_form = driver.find_element(By.ID, "input-firstname") # Cualquier elemento del form sirve
        registration_form.submit()

        # 6. Validación de éxito
        try:
            # Esperamos a que la URL contenga 'success'
            wait.until(EC.url_contains("success"))
            print(f"¡EXITO TOTAL! Registro completado para: {user_email}")
        except:
            # Si falla, tomamos foto y vemos qué dice el título
            print(f"Fallo en URL: {driver.current_url}")
            print(f"Título de página al fallar: {driver.title}")
            
            # Buscamos cualquier texto de error en la página
            all_text = driver.find_element(By.TAG_NAME, "body").text
            if "already registered" in all_text:
                print("EL ERROR ES: Email ya registrado.")
            elif "Privacy Policy" in all_text:
                print("EL ERROR ES: No se aceptó la política de privacidad.")
            
            driver.save_screenshot("DEBUG_FINAL_18.png")
            raise Exception("No se logró la redirección a Success.")

        # Asegurar que la carpeta de imágenes exista relativa al script
        img_dir = os.path.join(os.path.dirname(__file__), "../../img")
        os.makedirs(img_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        driver.save_screenshot(os.path.join(img_dir, f"registro_exitoso_{timestamp}.png"))

    def tearDown(self):
        self.driver.quit()  

if __name__ == '__main__':
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output=r"..\reporthtmlrunner"))