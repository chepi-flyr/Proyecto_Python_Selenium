from behave import given, when, then
from selenium.webdriver.common.by import By
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
import src.Functions_Utilitaries.Functions as func

@given('el usuario abre el navegador')
def step_open_navegador(context):
    options = Options()
    prefs = {
        "profile.default_content_settings.popups": 0,
        "directory_upgrade":True
    }
    options.add_experimental_option("prefs",prefs)
    options.add_argument('start-maximized')
    #options.add_argument("--headless")
    service = ChromeService(executable_path=ChromeDriverManager().install())
    context.driver = webdriver.Chrome(service=service, options=options)

@when('ingresa a la pagina de DemoQA')
def step_ingresa_pagina_demoqa(context):
    context.driver.get("https://demoqa.com/droppable")
    time.sleep(2)

@when('usuario arrastra el elemento "Draggable" a la nueva posición')
def step_arrastrar_elemento(context):
    elemento_a_arrastrar = context.driver.find_element(By.XPATH,"//div[@id='draggable']")
    elemento_destino = context.driver.find_element(By.XPATH,"//div[@id='simpleDropContainer']//div[@id='droppable']")

    action = ActionChains(context.driver)
    action.drag_and_drop(elemento_a_arrastrar,elemento_destino).perform()
    time.sleep(3)

@then('verifica que el elemento se ha movido a la nueva posición')
def step_verifica_elemento(context):
    elemento_destino = context.driver.find_element(By.XPATH,"//div[@id='simpleDropContainer']//div[@id='droppable']")
    assert "Dropped!" in elemento_destino.text, "El elemento no se ha movido correctamente"
    context.driver.quit()