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
import mysql.connector
from sqlalchemy import create_engine


############### CREATING DF + CONN TO MSQL DB ###############

# create the dataframe that everything will be stored in
df = pd.DataFrame(columns = ['query', 'search_engine', 'url', 'term_count'])


# create connection
conn = mysql.connector.connect(
  host="localhost",
  user= "esther",
  password= "Chopsticks7!"
)

# preparing the cursor object
cursor = conn.cursor()

'''
if mysql.database('my_custom_bot').exists():
     # add df to sql
    df.to_sql(con = conn, if_exists='append', name='search')

else:
    # creating the database
    cursor.execute('CREATE DATABASE MY_CUSTOM_BOT')

    # creating table
    cursor.execute('CREATE TABLE MY_CUSTOM_BOT.search (search_term VARCHAR(255), search_output VARCHAR(255), url_results VARCHAR(255),term_in_url VARCHAR(255));')
'''




############### WEB SEARCH + SCREENSHOTS ###############

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
df = pd.DataFrame(columns = ['query', 'search_engine', 'img_paths', 'txt_paths', 'url', 'term_count'])

search_engines = {"http://www.google.com/search?q=": "google",
                  "https://www.bing.com/search?q=": "bing",
                  "https://search.yahoo.com/search?p=": "yahoo",
                  "https://duckduckgo.com/?q=": "duckduckgo"}

# ask for query input
query = input("Enter search query: ").strip()

if query:
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

else:
    print("No search query provided.")






############### OCR TEXT RECOGNITION, URL SCRAPING, URL CLEANING ###############

# ask user to specify where text files will be stored
text_folder = input("Enter folder name where text files will be stored: ")

if os.path.exists(text_folder):
    for img_path in df['img_paths']:
        pic_name = df['query'].replace(' ', '_')

        # extract text from image
        image = cv2.imread(img_path)
        text = pytesseract.image_to_string(image)
        txt_path = os.path.join(str(text_folder), str(pic_name.iloc[0]) + '.txt')


        # write contents to file
        with open(txt_path, 'w') as text_file:
            text_file.write(text)

        # append text file path to df
        df['txt_paths'] = txt_path



    url_lists = []

    for txt_path in df['txt_paths']:
        with open(txt_path, 'r') as text_file:
            file_contents = text_file.read()
            urls = re.findall(r'(www\.[^\s]+|https?://[^\s]+)', file_contents)
            url_lists.append(urls)

    # Assign the URL lists to the DataFrame column
    df['urls'] = url_lists
    

    # clean URLs 
    for k, v in df['urls'].items():
        for i, url in enumerate(v):
            v[i] = re.sub(r'^h[a-z]*:', 'https:', url)
            v[i] = re.sub(r':/A\w\w\w\.', 'https://www.', url)

    df = df.explode('urls')

    print("Successfully cleaned URLS and appended to df.")
    print(df.head())

else:
    print("Please provide valid folder names.")



############### ADDING QUERY SEARCH TERM COUNT ###############

def count_term_occurrences(query, url):
    return sum(1 for word in query.split() if word in url)

# Apply the function to each row
df['term_count'] = df.apply(lambda row: count_term_occurrences(row['query'], row['urls']), axis=1)

print("Successfully counted search terms in URL.")
print(df)


############### APPENDING THE DF TO THE SQL DB ###############

# Define the connection string
connection_string = 'mysql+mysqlconnector://esther:Chopsticks7!@localhost/MY_CUSTOM_BOT'

# Create a SQLAlchemy engine
engine = create_engine(connection_string)

# Append the DataFrame to the existing table in the database
df.to_sql(name='search', con=engine, if_exists='replace', index=False)

# Dispose the engine
engine.dispose()

sql_query = "SELECT * FROM MY_CUSTOM_BOT.search"
sql_df = pd.read_sql(sql_query, conn)
print(sql_df)