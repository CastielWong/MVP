#!/usr/bin/env/ python
# -*- coding: utf-8 -*-
"""Perform OCR to extract text."""

import os

from PIL import Image
import pytesseract

_DIR_IMAGE = "images"

if __name__ == "__main__":
    # image_name = "alphabet.jpg"
    image_name = "question.png"

    image_to_scan = os.path.join(_DIR_IMAGE, image_name)
    text = pytesseract.image_to_string(Image.open(image_to_scan))

    output = []

    for line in text.split("\n"):
        processed = line.strip().replace("", "").replace("© ", "").replace("@ ", "")
        if not processed:
            continue

        output.append(f"{processed}\n")

    with open(os.path.join(_DIR_IMAGE, "output.txt"), "w") as f_w:
        f_w.writelines(output)
