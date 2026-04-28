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
        wait = WebDriverWait(driver, 30) # Aumentamos a 30 por si la red va lenta
        
        # CAMBIO CLAVE: Vamos directo a la URL de registro
        driver.get("http://opencart.abstracta.us/index.php?route=account/register")
        print(f'Ingreso directo al registro. Título: {driver.title}')

        # Generamos el email dinámico
        user_email = f"tester{random.randint(1, 999999)}@example.com"

        # Esperamos a que el primer campo sea visible
        # Usamos visibility_of_element_located correctamente
        first_name = wait.until(EC.visibility_of_element_located((By.ID, "input-firstname")))
        
        # Llenado de formulario
        first_name.send_keys("Sergio")
        driver.find_element(By.ID, "input-lastname").send_keys("Castaño")
        driver.find_element(By.ID, "input-email").send_keys(user_email)
        driver.find_element(By.ID, "input-telephone").send_keys("555123456")
        driver.find_element(By.ID, "input-password").send_keys("ProPassword123!")
        driver.find_element(By.ID, "input-confirm").send_keys("ProPassword123!")
        
        # Aceptar términos (usamos JavaScript para asegurar el clic en modo headless)
        agree_check = driver.find_element(By.NAME, "agree")
        driver.execute_script("arguments[0].click();", agree_check)
        
        # Botón continuar
        continue_btn = driver.find_element(By.XPATH, "//input[@value='Continue']")
        driver.execute_script("arguments[0].click();", continue_btn)

        # Validación final con espera
        # Validación final más flexible
        try:
            # Esperamos a que la URL cambie a 'success' o que aparezca el texto de éxito
            wait.until(EC.url_contains("success"))
            print(f"Registro completado. URL actual: {driver.current_url}")
            
            # Buscamos el texto en todo el cuerpo de la página para no fallar por etiquetas h1/h2
            success_body = wait.until(EC.presence_of_element_located((By.TAG_NAME, "body"))).text
            
            if "Your Account Has Been Created!" in success_body or "Success" in driver.title:
                print("¡Validación exitosa! Cuenta creada.")
            else:
                print("Aviso: No se encontró el texto exacto, pero la URL es de éxito.")
        
        except Exception as e:
            print("Error en la validación final. Guardando captura de pantalla...")
            # Guardamos la captura directamente en el espacio de trabajo para verla en Jenkins
            driver.save_screenshot("debug_final_error.png")
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