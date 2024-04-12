
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(options=chrome_options)

# maximizing the window size
driver.maximize_window()

# Define the folder path to save the images
SAVE_FOLDER = input("Enter the folder path to save the screenshots: ")

search_engines = {"http://www.google.com/search?q=": "google",
                  "https://www.bing.com/search?q=": "bing",
                  "https://search.yahoo.com/search?p=": "yahoo",
                  "https://duckduckgo.com/?q=": "duckduckgo"}

for url, engine in search_engines.items():
    # getting the webpage
    driver.get(url + "Childhood cancer early diagnosis methods")
    time.sleep(10)
    driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
    time.sleep(10)
    width = 1920
    height = driver.execute_script("return Math.max(document.body.scrollHeight,document.body.offsetHeight,document.documentElement.clientHeight,document.documentElement.scrollHeight,document.documentElement.offsetHeight);")
    driver.set_window_size(width, height)

    # take a screenshot
    screenshot_name = engine + ".png"
    save_path = os.path.join(SAVE_FOLDER, screenshot_name)
    driver.save_screenshot(save_path)









