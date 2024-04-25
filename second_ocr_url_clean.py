import cv2
import pytesseract
import os
import re
import third_creating_df

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


def main():
    pic_folder = input("Enter folder name where pictures are stored: ")
    text_folder = input("Enter folder name where text files will be stored: ")
    
    if os.path.exists(pic_folder) and os.path.exists(text_folder):
        
        # run function to extract text from image
        print("------Extracting text from image...------")
        image_text_extract(pic_folder, text_folder)
        print("\nText successfully extracted from images.\n")
        # list all text files in the folder
        text_names = os.listdir(text_folder)
        print(text_names)

        # run function to extract URLs from text
        print("\n------Extracting URLs from text...------")
        url_dict = get_urls(text_folder)
        print("\nURLs extracted.\n")
        # viewing the dictionary
        for key, value in url_dict.items():
            print(key, value)
            print("\n")

        # run function to clean extracted URLs
        print("\n------Cleaning extracted URLs...------")
        clean_urls(url_dict)
        print("\nURLs have been cleaned.\n")
        # viewing them
        for key, value in url_dict.items():
            print(key, value)
            print("\n")


    else:
        print("Please provide valid folder names.")


if __name__ == "__main__":
    main()