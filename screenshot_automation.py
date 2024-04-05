import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(options=chrome_options)
# maximizing the window size
driver.maximize_window()
# getting the webpage
driver.get("http://google.com/search?q=" + "Childhood cancer early diagnosis methods")
time.sleep(10)
driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
time.sleep(10)
width = 1920
height = driver.execute_script("return Math.max(document.body.scrollHeight,document.body.offsetHeight,document.documentElement.clientHeight,document.documentElement.scrollHeight,document.documentElement.offsetHeight);")
driver.set_window_size(width, height)
page_body = driver.find_element(By.TAG_NAME,"body")

page_body.screenshot("screenshot.png")
driver.quit()












