import allure
import time
import os
from datetime import datetime

def add_screenshot(context, name = "Captura de pantalla"):
    screenshoot = context.driver.get_screenshot_as_png()
    allure.attach(
        screenshoot,
        name,
        attachment_type=allure.attachment_type.PNG
    )
    time.sleep(2)

def screenshot_test(context, screenshoot_dir = "src/img/"):
    os.makedirs(screenshoot_dir, exist_ok = True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"screenshot_{timestamp}.png"
    file_path = os.path.join(screenshoot_dir,file_name)
    context.driver.save_screenshot(file_path)