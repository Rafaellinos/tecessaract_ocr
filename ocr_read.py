
"""
libraries needed:
pip install pytesseract 0.3.0
pip install opencv-python 4.1.2.30
pip install pdf2image 1.10.0
pip install numpy 1.17.4
"""
import pytesseract as ocr
from PIL import Image
import cv2
from pdf2image import convert_from_path
import os
import numpy as np

def convert_img(pdf_file):
    print("Converting files...")
    page_num = 1
    pdf_pages = convert_from_path(pdf_file, 200)
    files = []
    for page in pdf_pages:
        file_name = f"{pdf_file.replace('.pdf','')}-{page_num}.png"
        files.append(file_name)
        page.save(file_name,"PNG")
        page_num += 1
    return files

def treat_img(files):
    print("Treating files...")
    treated_files = []
    for file in files:
        img = cv2.imread(file)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        kernel = np.ones((1, 1), np.uint8)
        img = cv2.dilate(gray, kernel, iterations=1)
        img = cv2.erode(gray, kernel, iterations=1)
        cv2.imwrite("gray"+file, gray)
        treated_files.append("gray"+file)
    remove_tmp_files(files)
    return treated_files

def remove_tmp_files(files_names):
    print("Removing tmp files...")
    for file in files_names:
        os.remove(file)

def read_img(treated_files):
    print("Reading files...")
    result = ""
    for file in treated_files:
        result += ocr.image_to_string(Image.open(file), lang='por')
    remove_tmp_files(treated_files)
    return result


#pdf_file = "Alvará.pdf"
files = convert_img("Alvará.pdf")
treated_files = treat_img(files)
print(read_img(treated_files))
