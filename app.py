from bs4 import BeautifulSoup
import requests
from time import time
from os.path import join, exists
import userurlopener
import json

# GLOBALS
ROOT_DIR = "./images/"
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
HEADERS = {'User-Agent': USER_AGENT}

DIAGNOSES = {"dermatitis", "eczema", "acne", "rosacea", "urticaria", "psoriasis", "herpes", "dermatophytosis", "tinea", "scabies", "impetigo", "cellulitis", "lupus"}
METADATA_ROOT = "https://globalskinatlas.com/public/case"
DIAG_ROOT = "https://globalskinatlas.com/public/diagnosis"

METADATA_FILE = join(ROOT_DIR, "meta.json")

def read_subdirectory(url, subfolder="./"):
    source = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(source.text, "html.parser")
    imgs = soup.find_all("img", class_="image")
    atag = soup.find_all("a")
    download_images_from_url_list(imgs, subfolder) 


def download_images_from_url_list(url_list, subfolder):
    myOpener = userurlopener.URLOpener()
    for img in url_list:
        imgurl = img['src']
        casestring = img['id']
        filename = imgurl.split('/')[-1]
        save_file = join(ROOT_DIR, subfolder, filename)

        if not exists(save_file):
            get_metadata(filename, casestring)
            myOpener.retrieve(imgurl, save_file)

def get_metadata(image_name, casestring):
    # get data
    try:
        with (open(METADATA_FILE, "r") as f):
            metadata = json.load(f)
    except:
        metadata = {}
    # image_name: the full image file path (ie. 123_1.jpg)
    image_id = image_name.split("_")[0]
    case_id = casestring.split("_")[-1]
    # find metadata
    meta_url = join(METADATA_ROOT, image_id, case_id)
    meta_src = requests.get(meta_url, headers=HEADERS)
    meta_soup = BeautifulSoup(meta_src.text, "html.parser")
    plain_text = meta_soup.find_all('p')[1:]
    # select metadata
    metatags = {"site", "description", "morphology", "diagnosis", "sex", "age", "type", "submitted by"}
    entry = {}
    for field in plain_text:
        value = field.text
        for metatag in metatags:
            try:
                pair = value.split(":")
                tag = pair[0]
                data = pair[1]
                if metatag in tag.lower():
                    print(metatag, value)
                    data = value.split(":")[1].strip()
                    entry[metatag] = data
            except:
                print("Invalid field")
                pass
    metadata[image_id] = entry
    try:
        with (open(METADATA_FILE, "w") as f):
            json.dump(metadata, f, ensure_ascii=False, indent=4)
    except:
        pass

# GET URLS
root_src = requests.get(DIAG_ROOT, headers=HEADERS)
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
                read_subdirectory(diag_url, subfolder=diagnosis)
# _testurl = "https://globalskinatlas.com/public/diagnosis/23"
# _src = requests.get(_testurl, headers=HEADERS)
# _soup = BeautifulSoup(_src.text, "html.parser")
# _a = _soup.find_all("a")
# _img = _soup.find_all("img", class_="image")
# for img in _img:
#     _id = img['id']
#     print(_id)