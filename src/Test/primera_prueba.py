import unittest
import HtmlTestRunner
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.options import Options 
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.keys import Keys
from selenium.webdriver.common.by import By
import os
from datetime import datetime

class TestPractica(unittest.TestCase):