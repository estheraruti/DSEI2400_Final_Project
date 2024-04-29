import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os
import pandas as pd
import cv2
import pytesseract
import os
import re


######################## MAIN ########################

# entry point of our script
def main():
    
    query = input("Enter search query: ").strip()  # Strip leading/trailing whitespace
    if query:
        web_search(query)

    if os.path.exists(pic_folder) and os.path.exists(text_folder):
         pic_folder = input("Enter folder name where pictures are stored: ")
         text_folder = input("Enter folder name where text files will be stored: ")
         
         image_text_extract(pic_folder, text_folder)
         
         url_dict = get_urls(text_folder)
         
         clean_urls(url_dict)
         
         # append clean urls to corresponding
         if url_dict.key().str.contains(re.findall(r'*google*')):
            df['urls'] = url_dict.values() where search_engine == 'google'

        elif url_dict.key().str.contains(re.findall(r'*bing*')):
            df['urls'] = url_dict.values() where search_engine == 'bing'

        elif url_dict.key().str.contains(re.findall(r'*yahoo*')):
            df['urls'] = url_dict.values() where search_engine == 'yahoo'
        
        elif url_dict.key().str.contains(re.findall(r'*duckduckgo*')):
            df['urls'] = url_dict.values() where search_engine == 'duckduckgo'

        print(df.head())
        

    
    
    else:
        print("No search query provided.")

# check that the script is being run directly and not being imported
if __name__ == "__main__":
    main()  # if script is being run directly, execute the main function

######################## WEB SEARCH AND SCREENSHOT ########################

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
df = pd.DataFrame(columns = ['query', 'search_engine', 'url', 'term_count'])

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
        screenshot_name = query + "_" + engine + ".png"
        save_path = os.path.join(SAVE_FOLDER, screenshot_name)
        driver.save_screenshot(save_path)

        # Create a DataFrame for the current query and engine
        new_df = pd.DataFrame({'query': [query], 'search_engine': [engine]})
        dfs.append(new_df)

    # Concatenate all DataFrames in the list
    df = pd.concat(dfs, ignore_index=True)

    #print(df.head())

######################## OCR AND URL CLEANING ########################

# define function to extract text from image
def image_text_extract(pic_folder, text_folder):
    for pic_name in os.listdir(pic_folder):
        image_path = os.path.join(pic_folder, pic_name)
        image = cv2.imread(image_path)
        text = pytesseract.image_to_string(image)
        txt_path = os.path.join(text_folder, os.path.splitext(pic_name)[0] + '.txt')
        
        with open(txt_path, 'w') as text_file:
            text_file.write(text)

# define function to extract URLs from text
def get_urls(text_folder):
    url_dict = {}
    for text_name in os.listdir(text_folder):
        txt_path = os.path.join(text_folder, text_name)
        
        with open(txt_path, 'r') as text_file:
            file_contents = text_file.read()
            urls = re.findall(r'(www\.[^\s]+|https?://[^\s]+)', file_contents)
            url_dict[text_name] = urls
    return url_dict

# define function to clean extracted URLs
def clean_urls(url_dict):
    for k, v in url_dict.items():
        for i, url in enumerate(v):
            v[i] = re.sub(r'^h[a-z]*:', 'https:', url)
            v[i] = re.sub(r':/A\w\w\w\.', '://www.', url)

######################## SEARCH TERM COUNT ########################

def term_counts(df, query):
    for term in query:
        df['term_count_' + term] = 0
        for index, row in df.iterrows():
            match = re.findall(term, row.iloc[1], re.IGNORECASE)
            count = len(match)
            df.loc[index, 'term_count_' + term] = count
    return df

######################## APPEND TO SQL DATABASE ########################






