
import os
from time import sleep
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import NoSuchElementException
from chromedriver_autoupdate import get_chrome_version, update_chrome_driver

#funciones selenium
def get_web_element(web_element):
    """returns web element"""
    selected_element = driver.find_element(By.XPATH, web_element)
    return selected_element


def get_web_elements(web_elements):
    """returns list of web elements"""
    selected_elements = driver.find_elements(By.XPATH, web_elements)
    return selected_elements


def is_web_element(element):
    """check if element is present in web page.Returns True or False"""
    try:
        driver.find_element(By.XPATH, element)
        return True
    except NoSuchElementException:
        return False


# elementos de la pagina
WEL_REGISTER = "//th[text()='Registro de condenas']"
WEL_NEW_REGISTER = "//a[text()='Nuevo registro']"
WEL_REGISTER_TYPE = "//*[@id='selectTipoRegistroRM']//ancestor::select"
WEL_REGISTER_REGION = "//*[@id='selectRegionRegistroRM']//ancestor::select"
WEL_REGISTER_UNIT = "//*[@id='selectUnidadRegistroRM']//ancestor::select"
WEL_INPUT_FILE = "//input[@type='file']"
WEL_SEND_BUTTON = "//input[@id='btnRegistrar']"
WEL_LOADING = "//img[@alt='Un momento por favor...']"
WEL_LOADING_II = "//img[contains(@src, 'cargando')]"

# verificar la version actual de chrome
chrome_version = get_chrome_version()
if chrome_version is None:
    print("Google Chrome no está instalado.")
    exit()
print(f"Versión de Google Chrome: {chrome_version}")

#actualizar chromedriver
update_chrome_driver(chrome_version)


#credenciales para ingresar. extraer de primeras dos lineas de config.txt
#formato USUARIO=usuario, PASSWORD=password

with open('config.txt', 'r') as f:
    lines = f.readlines()
    usuario = lines[0].split('=')[1].strip()
    password = lines[1].split('=')[1].strip()
    url = lines[2].split('=')[1].strip()

# ruta de los pdfs a subir

pdfs_path = fr'{os.getcwd()}\pdfs'
pdfs_list = os.listdir(pdfs_path)
#pdfs_list= [pdf.replace(' 1','') for pdf in pdfs_list]
pdfs_list = set(pdfs_list)
print('Total de pdfs para subir: ', len(pdfs_list))


#activar selenium

ChromeOptions = Options()
ChromeOptions.add_argument("--start-minimized")
s = Service('chromedriver.exe')



driver = webdriver.Chrome(service=s, options=ChromeOptions)
action = ActionChains(driver)
driver.get(url)

sleep(10)


standar_wait = WebDriverWait(driver, 10)


#ingresar credenciales

# login
starting_button = driver.find_element(By.XPATH, "//input[@class='IngresarBoton']")
input_user = driver.find_element(By.XPATH, "//input[@name='username']")
input_password = driver.find_element(By.XPATH, "//input[@name='password']")

input_user.send_keys(usuario)
input_password.send_keys(password)
starting_button.click()

print('login successful')
sleep(1)

counter = 1
for pdf in pdfs_list:
    register_menu = standar_wait.until(EC.presence_of_element_located((By.XPATH, WEL_REGISTER)))
    register_menu.click()

    select_new_register = get_web_element(WEL_NEW_REGISTER)
    select_new_register.click()


    select_register_type = Select(get_web_element(WEL_REGISTER_TYPE))
    select_register_type.select_by_index(1)

    select_register_region = Select(get_web_element(WEL_REGISTER_REGION))
    select_register_region.select_by_index(1)

    select_register_unit = Select(get_web_element(WEL_REGISTER_UNIT))
    select_register_unit.select_by_index(1)

    #upload pdf
    input_file= get_web_element(WEL_INPUT_FILE)
    input_file.send_keys(fr'{pdfs_path}\{pdf}')

    send_button = get_web_element(WEL_SEND_BUTTON)
    send_button.click()

    #esperar a que cargue
    while True:
        try:
            if is_web_element(WEL_LOADING) or is_web_element(WEL_LOADING_II):
                sleep(1)
            else:
                break
        
        except UnexpectedAlertPresentException:
            sleep(1)
            try:
                driver.refresh()
                break
            except UnexpectedAlertPresentException:
                driver.refresh()
                break

    
    print(f'{counter}. {pdf} uploaded successfully')
    counter += 1
    
