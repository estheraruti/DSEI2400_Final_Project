import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os
import pandas as pd

# create the dataframe that everything will be stored in
df = pd.DataFrame(columns = ['query', 'search_engine', 'url', 'term_count'])

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(options=chrome_options)

# maximizing the window size
driver.maximize_window()

# Define the folder path to save the images
SAVE_FOLDER = 'Web_Photos'

# Ensure the folder exists, create it if it doesn't
os.makedirs(SAVE_FOLDER, exist_ok=True)

# create the dataframe that everything will be stored in
df = pd.DataFrame(columns = ['query', 'search_engine', 'img_paths', 'url', 'term_count'])

search_engines = {"http://www.google.com/search?q=": "google",
                  "https://www.bing.com/search?q=": "bing",
                  "https://search.yahoo.com/search?p=": "yahoo",
                  "https://duckduckgo.com/?q=": "duckduckgo"}


def web_search(query):
    # declare df as global
    global df

    dfs = []  # List to store DataFrames for each iteration

    for url, engine in search_engines.items():
        # getting the webpage
        driver.get(url + query)

        # wait for a few seconds for the page to load
        time.sleep(10)

        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)

        # wait a few seconds for the page to load
        time.sleep(10)

        # set the width and height of screenshot
        width = 1920
        height = driver.execute_script("return Math.max(document.body.scrollHeight,document.body.offsetHeight,document.documentElement.clientHeight,document.documentElement.scrollHeight,document.documentElement.offsetHeight);")
        driver.set_window_size(width, height)

        # take a screenshot
        screenshot_name = query.replace(' ', '_') + "_" + engine + ".png"
        save_path = os.path.join(SAVE_FOLDER, screenshot_name)
        driver.save_screenshot(save_path)

        # Create a DataFrame for the current query and engine
        new_df = pd.DataFrame({'query': [query], 'search_engine': [engine], 'img_paths': save_path})
        dfs.append(new_df)

    # Concatenate all DataFrames in the list
    df = pd.concat(dfs, ignore_index=True)

    print(df.head())



# entry point of our script
def main():
    
    query = input("Enter search query: ").strip()  # Strip leading/trailing whitespace
    if query:
        web_search(query)
    else:
        print("No search query provided.")

# check that the script is being run directly and not being imported
if __name__ == "__main__":
    main()  # if script is being run directly, execute the main function