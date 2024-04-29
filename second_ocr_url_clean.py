import cv2
import pytesseract
import os
import re
import first_query_websearch
from first_query_websearch import df

# define function to extract text from image
def image_text_extract(img_path, text_folder):
        pic_name = df['query'].replace(' ', '_')
        image = cv2.imread(img_path)
        text = pytesseract.image_to_string(image)
        txt_path = os.path.join(text_folder, os.path.splitext(pic_name)[0] + '.txt')

        # append text file path to df
        df['txt_paths'] = txt_path
        
        # write contents to file
        with open(txt_path, 'w') as text_file:
            text_file.write(text)
            
        

# define function to extract URLs from text
def get_urls(txt_path):

    url_dict = {}
    for txt_path in df['txt_paths']:
        
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
            v[i] = re.sub(r':/A\w\w\w\.', 'https://www.', url)


def main():
    global df 
    print(df.head())
    text_folder = input("Enter folder name where text files will be stored: ")
    
    if os.path.exists(text_folder):

        for img_path in df['img_paths']:
        
            # run function to extract text from image
            image_text_extract(img_path, text_folder)
            print("TEXT EXTRACTED")

           
            # run function to extract URLs from text
            url_dict = get_urls(text_folder)
            print("URLS EXTRACTED")
            
            # viewing the dictionary
            for key, value in url_dict.items():
                print(key, value)
                print("\n")

            # run function to clean extracted URLs
            clean_urls(url_dict)
        
            # viewing them
            for key, value in url_dict.items():
                print(key, value)
                print("\n")

            # append clean urls to data frame
            df['urls'] = url_dict.values()

            # explode list of urls
            df.explode('urls')

            print(df.head())

        


    else:
        print("Please provide valid folder names.")


if __name__ == "__main__":
    main()