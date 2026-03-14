import cv2
import numpy as np
from pdf2image import convert_from_path
import easyocr
import re


def load_images(path):
    if path.lower().endswith(".pdf"):
        pages = convert_from_path(path)
        return [np.array(p.convert("RGB")) for p in pages]

    img = cv2.imread(path)
    if img is None:
        return []
    return [cv2.cvtColor(img, cv2.COLOR_BGR2RGB)]


def run_easyocr(images):
    reader = easyocr.Reader(["en"], gpu=False)
    output = []
    for img in images:
        text = reader.readtext(img, detail=0)
        output.extend(text)
    return output


def fix_price_confusions(text):
    text = re.sub(r"S(?=\d)", "$", text)

    text = re.sub(r"(?<=\d)[oO](?=\d)", "0", text)

    return text


def apply_corrections(lines):
    corrected = []
    for line in lines:
        fixed = fix_price_confusions(line)
        corrected.append(fixed)
    return corrected
