import unittest
import HtmlTestRunner
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

class GoogleTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_title(self):

        options = Options()
        prefs = {
            "profile.default_content_settings.popups": 0,
            "directory_upgrade":True
        }
        options.add_experimental_option("prefs",prefs)
        options.add_argument('start-maximized')
        #options.add_argument("--headless")

        #self.driver = webdriver.Chrome(service=ChromeService("../Drivers/chromedriver.exe"), options=options)

        service = ChromeService(executable_path=ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        
        self.driver.get("https://www.google.com")
        self.assertIn("Google", self.driver.title)

    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output=r'..\src\reporthtmlrunner'))