from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import csv
import os
from dotenv import load_dotenv

# Post class
class Post:
    def __init__(self, id, post_info, date, like):
        self.id = id
        self.post_info = post_info
        self.date = date
        self.like = like

# Start the driver
def iniciar_driver():
    chrome_options = Options()
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--start-maximized')
    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=chrome_options)
    return driver

# Sleep function
def mySleep(nTimeOut):
    nTimeInit = time.time()
    nTimeDifference = time.time() - nTimeInit
    while nTimeDifference < nTimeOut:
        nTimeDifference = time.time() - nTimeInit

# Instagram Scrap
def instagramScrap(accountToScrap, driver, postAmountToScrap):
    # Open the profile account
    driver.get('https://www.instagram.com/' + accountToScrap)
    mySleep(5)
    # Get the first post
    post = driver.find_element(By.CSS_SELECTOR, 'div.x1lliihq.x1n2onr6.xh8yej3.x4gyw5p.xfllauq.xo2y696.x11i5rnm.x2pgyrj')
    post.click()
    # Create a list to store the posts
    posts = []
    # Loop to get the posts
    for _ in range(postAmountToScrap):
        mySleep(1)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        # Get post information
        postInfo = soup.find_all('div', class_='_a9zs')
        try:
            postInfo = postInfo[0].text
        except:
            postInfo = 'No post info'
        # Get the date
        timeElements = soup.find_all('time', datetime=True)
        try:
            date = timeElements[-1].get('datetime')
        except:
            date = 'No date'
        # Get the likes
        likes = soup.find_all('span', class_='html-span xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x1hl2dhg x16tdsg8 x1vvkbs')
        try:
            likes = likes[-1].text
        except:
            likes = 0
        # Create a post object
        post = Post(_, postInfo, date, likes)
        # Append the post to the list
        posts.append(post)
        # Click the next button
        button = driver.find_element(By.CSS_SELECTOR, 'div._aaqg._aaqh button._abl-')
        button.click()
    return posts

# Login to Instagram
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

# Convert list to csv
def listToCsv(list, filename):
    with open(filename, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['ID', 'Post Info', 'Date', 'Likes'])
        for item in list:
            writer.writerow([item.id, item.post_info, item.date, item.like])

if __name__ == '__main__':
    # Start the driver
    driver = iniciar_driver()
    # Load environment variables from .env file
    load_dotenv()
    # Get the values from environment variables
    user = os.getenv("INSTAGRAM_USER")
    password = os.getenv("INSTAGRAM_PASSWORD")
    driver = iniciar_sesion(driver, user, password)
    # Read the accounts to scrap
    with open('accounts_to_scrap.txt', 'r') as file:
        accounts = file.read().splitlines()
    # Set the amount of posts to scrap
    postAmountToScrap = 10
    # Scrap the accounts
    for account in accounts:
        posts = instagramScrap(account, driver, postAmountToScrap)
        listToCsv(posts, f'csv/{account}.csv')
    driver.quit()
