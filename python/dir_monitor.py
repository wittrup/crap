import os
from time import sleep
from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:/tesseract-ocr/tesseract'


path_to_watch = "ignore/"
before = dict ([(f, None) for f in os.listdir (path_to_watch)])
print(before)

while 1:
    sleep (1)
    after = dict ([(f, None) for f in os.listdir(path_to_watch)])
    added = [f for f in after if not f in before]
    removed = [f for f in before if not f in after]
    if added:
        print("Added: ", ", ".join(added))
        for add in added:
            filename, file_extension = os.path.splitext(add)
            if file_extension.lower() == '.png':
                try:
                    print(pytesseract.image_to_string(Image.open(path_to_watch + add), lang='nor'))
                except:
                    print('OCR of', path_to_watch + add, 'failed')
            else:
                print(file_extension, 'is not .png')
    if removed:
        print("Removed: ", ", ".join (removed))
    before = after
