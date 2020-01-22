"""
    libraries needed:
    pip install wand 0.5.8
    pip install pytesseract 0.3.0
    pip install Pillow 6.2.1

"""

from wand.image import Image
from PIL import Image as PI
import io
import pytesseract as ocr

image_pdf = Image(filename="tmp/alvara.pdf", resolution=300)
image_jpeg = image_pdf.convert('png')

req_image = []
for img in image_jpeg.sequence:
    img_page = Image(image=img)
    req_image.append(img_page.make_blob('png'))

txt = ""
for img in req_image:
    txt += ocr.image_to_string(PI.open(io.BytesIO(img)), lang='por')

print(txt)
