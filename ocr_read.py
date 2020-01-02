
"""
libraries needed:
pip install pytesseract 0.3.0
pip install opencv-python 4.1.2.30
pip install pdf2image 1.10.0
pip install numpy 1.17.4

virtualenv -p python3 ocr_env
sudo apt install tesseract-ocr
usr/share/tesseract-ocr/4.00/tessdata# cp -R /home/rafael/Documents/gits/tecessaract_ocr/por.traineddata .
"""
import pytesseract as ocr
from PIL import Image
import cv2
from pdf2image import convert_from_path
import os
import numpy as np

def convert_img(pdf_file):
    print("Converting files...")
    pdf_pages = convert_from_path(pdf_file, 200)
    files = []
    for page_num, page in enumerate(pdf_pages, start=1):
        file_name = f"{pdf_file.replace('.pdf','')}-{page_num}.png"
        files.append(file_name)
        page.save(file_name,"PNG")
    return files

def treat_img(files):
    print("Treating files...")
    treated_files = []
    for file in files:
        img = cv2.cvtColor(cv2.imread(file), cv2.COLOR_BGR2GRAY)
        kernel = np.ones((1, 1), np.uint8)
        img = cv2.dilate(img, kernel, iterations=1)
        img = cv2.erode(img, kernel, iterations=1)
        file_name = file[:4]+"gray_"+file[4:]
        cv2.imwrite(file_name, img)
        treated_files.append(file_name)
    remove_tmp_files(files)
    return treated_files

def remove_tmp_files(files_names):
    print("Removing tmp files...")
    for file in files_names:
        os.remove(file)

def read_img(treated_files):
    print("Reading files...")
    result = ""
    print(treated_files)
    for file in treated_files:
        result += ocr.image_to_string(Image.open(file), lang='por')
    remove_tmp_files(treated_files)
    return result

def create_text_file(text,file_name):
    try:
        f = open(f"{file_name}.txt","w+")
        f.write(text)
        f.close()
        return True
    except Exception as e:
        print("Error: \n"+str(e))
        return

#if not os.path.exists("tmp/"):
#   os.makedirs("tmp/")
files = convert_img("tmp/alvara.pdf")
treated_files = treat_img(files)
create_text_file(read_img(treated_files),"texto_teste2")
#print(read_img(treated_files))

#treated_files = treat_img(["/tmp"])
#print(read_img(["tmp/gray_test_ocr-1.png"]))