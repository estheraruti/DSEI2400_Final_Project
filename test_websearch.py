import webbrowser
import pyautogui
import time
import os

# Define the folder path where you want to save the images
SAVE_FOLDER = "DSEI2400\\Web_Photos"



# Ensure the folder exists, create it if it doesn't
os.makedirs(SAVE_FOLDER, exist_ok=True)

search_engines = {"http://www.google.com/search?q=": "google",
                  "https://www.bing.com/search?q=": "bing",
                  "https://search.yahoo.com/search?p=": "yahoo",
                  "https://duckduckgo.com/?q=": "duckgo"}

# define function that takes in query for google search
def web_search(query):
    for url,engine in search_engines.items():
        base_url = url
        search_url = base_url + query
        webbrowser.open(search_url)
        
        # Wait for a few seconds for the page to load
        time.sleep(5)  # Adjust the delay time as needed
        
        # Take a screenshot after waiting
        screen = pyautogui.screenshot()
        save_path = os.path.join(SAVE_FOLDER, query + "_" + engine + ".png")  # Extract engine name from URL
        screen.save(save_path)

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
