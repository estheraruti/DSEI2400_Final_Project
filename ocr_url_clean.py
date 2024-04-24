import cv2
import pytesseract
import os
import re



# need tesseract as environment variable in path before running this
def image_text_extract():

    for pic_name in pic_names:
        image_path = os.path.join(pic_folder, pic_name)
        # read in image
        image = cv2.imread(image_path)

        # turning image into grayscale
        #gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        '''
        # Apply thresholding
        _, thresh_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        '''
        # extract text from image
        text = pytesseract.image_to_string(image)
        txt_path = os.path.join(text_folder, pic_name.split('.')[0] + '.txt')
        
        # adding text files
        with open(txt_path, 'w') as text_file:
            text_file.write(text)
    

def get_urls(text_names):
    url_dict = {}

    for text_name in text_names:
        txt_path = os.path.join(text_folder, text_name.split('.')[0] + '.txt')
        
        with open(txt_path, 'r') as text_file:
            file_contents = text_file.read()

            if 'yahoo' in text_name:
                urls = re.findall(r'www.[a-zA-Z]*[^\s]*', file_contents)

            else:
                urls = re.findall(r'h[a-zA-Z]*:/[^\s]*', file_contents)
            #print(urls)

        url_dict[text_name] = urls
    



def clean_urls(url_dict):
    # cleaning up the URLs
    for k, v in url_dict.items():
        for i in range(len(v)):
            v[i] = re.sub(r'^h[a-z]*:', 'https:', v[i])
            v[i] = re.sub(r':/A\w\w\w\.', '://www.', v[i])



def main():
    # specify folder where photos are
    pic_folder = input("Enter folder name where pictures are stored: ")

    # list all files in the folder
    pic_names = os.listdir(pic_folder)

    # specify folder for text
    text_folder = input("Enter folder name where text files will be stored: ")

    if pic_folder & text_folder:
        image_text_extract(pic_names)

        if image_text_extract(pic_names)
        print("Text successfully extracted from images.")


    else:
        print("Please provide both the name of the Picture Folder and Text Folder.")


if __name__ == "__main__":
    main()