from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Iniciar drivers de selenium
def iniciar_driver():
    chrome_options = Options()
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--start-maximized')
    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=chrome_options)
    return driver

# Pausar ejecución del programa
def mySleep(nTimeOut):
    nTimeInit = time.time()
    nTimeDifference = time.time() - nTimeInit
    while nTimeDifference < nTimeOut:
        nTimeDifference = time.time() - nTimeInit

# Scrap de instagram
def scrap_instagram(cuenta, driver):
    # Abrir perfil de instagram
    driver.get('https://www.instagram.com/' + cuenta)
    mySleep(5)
    # Conseguir el primer post
    post = driver.find_element(By.CSS_SELECTOR, 'div.x1lliihq.x1n2onr6.xh8yej3.x4gyw5p.xfllauq.xo2y696.x11i5rnm.x2pgyrj')
    post.click()
    # Recorrer los post
    for i in range(5):
        mySleep(2)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        html_file = open(f"{i}_html.html", "w", encoding='utf-8')
        html_file.write(html)
        html_file.close()
        soup_file = open(f"{i}_soup.txt", "w", encoding='utf-8')
        soup_file.write(str(soup))
        soup_file.close()
        # Conseguir la fecha del post
        time_elements = soup.find_all('time', datetime=True)
        print(time_elements[-1].get('datetime'))
        # Apretar el botón de siguiente
        button = driver.find_element(By.CSS_SELECTOR, 'div._aaqg._aaqh button._abl-')
        button.click()
    driver.quit()
    return soup

# Iniciar sesión en instagram
def iniciar_sesion(driver, user, password):
    driver.get('https://www.instagram.com/')
    mySleep(5)  # Wait for 5 seconds
    user_input = driver.find_element(By.CSS_SELECTOR, 'input[name="username"]')
    password_input = driver.find_element(By.CSS_SELECTOR, 'input[name="password"]')
    user_input.send_keys(user)
    password_input.send_keys(password)
    password_input.send_keys(Keys.RETURN)
    mySleep(5)  # Wait for 5 seconds after sending the password
    return driver

if __name__ == '__main__':
    cuenta = 'sanmiguel_cl'
    driver = iniciar_driver()
    driver = iniciar_sesion(driver, "diegoimlp@gmail.com", "Diegoimlp14")
    soup = scrap_instagram(cuenta, driver)
    print(soup)