#!/usr/bin/env/ python
# -*- coding: utf-8 -*-
"""Perform OCR to extract text."""
import os

from PIL import Image
import pytesseract

_DIR_IMAGE = "images"

if __name__ == "__main__":
    # image_name = "alphabet.jpg"
    image_name = "sample.jpg"

    image_to_scan = os.path.join(_DIR_IMAGE, image_name)
    print(pytesseract.image_to_string(Image.open(image_to_scan)))
