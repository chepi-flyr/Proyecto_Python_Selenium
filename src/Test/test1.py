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
        
        # 2. Datos aleatorios
        user_email = f"final.test.{random.randint(10000, 999999)}@example.com"
        
        # 3. Llenado asegurando interacción
        first_name = wait.until(EC.element_to_be_clickable((By.ID, "input-firstname")))
        first_name.send_keys("Sergio")
        driver.find_element(By.ID, "input-lastname").send_keys("Tester")
        driver.find_element(By.ID, "input-email").send_keys(user_email)
        driver.find_element(By.ID, "input-telephone").send_keys("3001234567")
        
        secure_pass = "Admin.12345!"
        pass_field = driver.find_element(By.ID, "input-password")
        pass_field.send_keys(secure_pass)
        driver.find_element(By.ID, "input-confirm").send_keys(secure_pass)

        # 4. Forzar el check de privacidad
        agree = driver.find_element(By.NAME, "agree")
        driver.execute_script("arguments[0].click();", agree)

        # 5. EL CAMBIO CLAVE: Simular presionar ENTER en lugar de hacer clic en el botón
        # Esto dispara el formulario directamente desde el teclado
        pass_field.send_keys(Keys.ENTER)

        # 6. Validación definitiva con la URL
        try:
            # Si el registro funciona, la URL DEBE cambiar a algo que contenga 'success'
            wait.until(EC.url_contains("success"))
            print(f"¡LO LOGRAMOS! URL de éxito: {driver.current_url}")
        except:
            print(f"URL al fallar: {driver.current_url}")
            driver.save_screenshot("ERROR_FINAL_ESTA_SI.png")
            # Imprime el texto de la página para ver si hay errores ocultos
            print("Contenido de la página al fallar: " + driver.title)
            raise Exception("El sitio no redirigió a la página de éxito.")

        # Asegurar que la carpeta de imágenes exista relativa al script
        img_dir = os.path.join(os.path.dirname(__file__), "../../img")
        os.makedirs(img_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        driver.save_screenshot(os.path.join(img_dir, f"registro_exitoso_{timestamp}.png"))

    def tearDown(self):
        self.driver.quit()  

if __name__ == '__main__':
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output=r"..\reporthtmlrunner"))