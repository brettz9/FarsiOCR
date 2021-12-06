import os
import re

import pytesseract
from pdf2image import convert_from_path

from preprocess import process_image

langs = "fas"  # Languages for OCR eng+fas
dirname = os.path.dirname(os.path.dirname(__file__))
input_dir = os.path.join(dirname, "data2")  # Directory of pdf/image files
output_dir = os.path.join(dirname, "output")  # Directory of ocr'ed images
if not os.path.exists(output_dir):
    os.makedirs(output_dir)


def main():
    for filename in os.listdir(input_dir):
        # Convert pdf to image files
        if filename.endswith('.pdf'):
            print(os.path.join(input_dir, filename))
            fullName = os.path.join(input_dir, filename)
            pages = convert_from_path(fullName, 500)
            image_counter = 1
            for page in pages:
                image_name = os.path.splitext(fullName)[0] + '_' + str(image_counter) + '.tiff'
                page.save(image_name, format='TIFF')
                image_counter += 1

    for filename in os.listdir(input_dir):
        img_ext = ['.png', '.jpg', '.jpeg', '.tiff']
        if filename.endswith(tuple(img_ext)):
            print(filename)
            fileAddress = os.path.join(input_dir, filename)
            img = process_image(fileAddress)

            # Recognize the text as string in image using pytesserct
            config = ''
            text = str(pytesseract.image_to_string(img, lang=langs, config=config))

            # Remove empty lines of text - s.strip() removes lines with spaces
            text = os.linesep.join([s for s in text.splitlines() if s.strip()])

            # Creating a text file to write the output
            write_output(filename, text)

            # Evaluate the result based on Levenshtein distance
            # evaluate_result(text)


def write_output(filename, text):
    outfile = os.path.join(output_dir, f'out_{os.path.splitext(filename)[0]}.txt')
    with open(outfile, 'w', encoding='utf-8') as text_file:
        text_file.write(text)


def evaluate_result(text):
    import docx2txt
    import Levenshtein
    original_text = docx2txt.process(os.path.join(input_dir, "original.docx"))
    original_text = os.linesep.join([s for s in original_text.splitlines() if s.strip()])

    text = re.sub(r'[|]', '', text)

    distance = Levenshtein.distance(original_text, text)
    print(distance)


if __name__ == "__main__":
    main()
