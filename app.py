from bs4 import BeautifulSoup
import requests
from time import time
from os.path import join, exists
import userurlopener

# GLOBALS
ROOT_DIR = "./images/"
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
HEADERS = {'User-Agent': USER_AGENT}

DIAGNOSES = {"dermatitis", "eczema", "acne", "rosacea", "urticaria", "psoriasis", "herpesvirus", "dermatophytosis", "tinea", "scabies", "impetigo", "cellulitis", "lupus"}

def read_subdirectory(url, subfolder="./"):
    source = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(source.text, "html.parser")
    imgs = soup.find_all("img", class_="image")
    download_images_from_url_list(imgs, subfolder) 


def download_images_from_url_list(url_list, subfolder):
    myOpener = userurlopener.URLOpener()
    for img in url_list:
        imgurl = img['src']
        filename = imgurl.split('/')[-1]
        save_folder = join(ROOT_DIR, subfolder)
        myOpener.retrieve(imgurl, join(save_folder, filename))

# GET URLS
diag_root_dir = "https://globalskinatlas.com/public/diagnosis"
root_src = requests.get(diag_root_dir, headers=HEADERS)
root_soup = BeautifulSoup(root_src.text, "html.parser")
url_list = root_soup.find_all("ul")
for list_ in url_list:
    for li in list_.findAll('li'):
        diag = li.text
        for diagnosis in DIAGNOSES:
            if diagnosis in diag.lower():
                print(diag)
                diag_url = li.find('a')['href']
                print(diag_url)
                read_subdirectory(diag_url, subfolder=diagnosis);