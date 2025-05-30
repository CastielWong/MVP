#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Customization on PDF."""
from pathlib import Path
from typing import List
import copy
import os

from PyPDF2 import PdfFileReader, PdfFileWriter
from PyPDF2.pdf import DocumentInformation
from reportlab.lib import colors, units
from reportlab.pdfgen.canvas import Canvas

_CWD = Path(__file__).parent.absolute()
_DIR_OUTPUT = "output"


def extract_information(pdf_path: str) -> DocumentInformation:
    """Extract meta of the PDF file.

    Args:
        pdf_path: path to the pdf file

    Returns:
        The meta information
    """
    with open(pdf_path, "rb") as f_r:
        pdf = PdfFileReader(f_r)
        information = pdf.documentInfo

    txt = f"""
        Information about {pdf_path}:

        Author: {information.author}
        Creator: {information.creator}
        Producer: {information.producer}
        Subject: {information.subject}
        Title: {information.title}
        Number of pages: {pdf.pages}
    """

    print(txt)
    return information


def rotate_pages(pdf_old: str, pdf_new: str) -> None:
    """Rotate pages in a pdf and output a new one.

    Args:
        pdf_old: original pdf file
        pdf_new: pdf file after rotated
    """
    pdf_writer = PdfFileWriter()
    pdf_reader = PdfFileReader(pdf_old)

    for page in pdf_reader.pages:
        if "/Rotate" not in page or page["/Rotate"] == 0:
            continue
        # rotate a page back to normal
        page.rotateClockwise(-page["/Rotate"])

    # rotate page 90 degrees to the right
    page_1 = pdf_reader.getPage(0).rotateClockwise(90)
    pdf_writer.addPage(page_1)
    # rotate page 90 degrees to the left
    page_2 = pdf_reader.getPage(1).rotateCounterClockwise(90)
    pdf_writer.addPage(page_2)
    # # add a page in normal orientation
    # pdf_writer.addPage(pdf_reader.getPage(2))

    with open(pdf_new, "wb") as fh:
        pdf_writer.write(fh)

    return


def merge_pdfs(dir_input: List[str], dir_output: str) -> None:
    """Merge a list of pdf files into one.

    Args:
        dir_input: a list of pdf files to merge, note that name of files are expected
            to be in order so as to keep the the merged PDF aligned
        dir_output: pdf file after merged
    """
    files = os.listdir(dir_input)  # type: ignore

    # the merged page order is determined by the order of pdf files
    pdf_files = [a_file for a_file in files if a_file.endswith(".pdf")]

    pdf_writer = PdfFileWriter()

    for file_name in pdf_files:
        file_path = f"{dir_input}/{file_name}"
        pdf_reader = PdfFileReader(file_path)
        for page in range(pdf_reader.getNumPages()):
            # add each page to the writer object
            pdf_writer.addPage(pdf_reader.getPage(page))

    # write out the merged PDF
    with open(f"{dir_output}/merged.pdf", "wb") as out:
        pdf_writer.write(out)

    return


def split_pdf(pdf_path: str, dir_output: str, prefix: str) -> None:
    """Split a PDF file into individual pages.

    Args:
        pdf_path: pdf file to split
        dir_output: directory to output
        prefixes: prefix used in generated pdf pages
    """
    pdf = PdfFileReader(pdf_path)
    pages = pdf.getNumPages()

    for index in range(pages):
        page = index + 1

        pdf_writer = PdfFileWriter()
        pdf_writer.addPage(pdf.getPage(index))

        output = f"{dir_output}/{prefix}_{page}.pdf"
        with open(output, "wb") as output_pdf:
            pdf_writer.write(output_pdf)

    return


def create_watermark(pdf_path: str, watermark_pdf: str, output: str) -> None:
    """Embedded watermark to the PDF.

    Args:
        pdf_path: pdf file to embed watermark
        watermark_pdf: watermark to embed, which is expected to be a PDF file
        output: pdf file after watermark embedded
    """
    watermark_obj = PdfFileReader(watermark_pdf)
    watermark_page = watermark_obj.getPage(0)

    pdf_reader = PdfFileReader(pdf_path)
    pdf_writer = PdfFileWriter()

    # watermark all the pages
    for page in pdf_reader.pages:
        page.mergePage(watermark_page)
        pdf_writer.addPage(page)

    with open(output, "wb") as out:
        pdf_writer.write(out)

    return


def convert_to_txt(pdf_path: str) -> str:
    """Convert a pdf into a text file.

    Args:
        pdf_path: pdf file to be converted

    Returns:
        File path of the output text file
    """
    file_name = Path(pdf_path).name.split(".")[0]
    output = _CWD / _DIR_OUTPUT / f"{file_name}.txt"

    pdf_reader = PdfFileReader(pdf_path)

    with output.open(mode="w") as file_writer:
        title = pdf_reader.documentInfo.title
        num_pages = pdf_reader.getNumPages()
        file_writer.write(f"{title}\\nNumber of pages: {num_pages}\\n\\n")

        for page in pdf_reader.pages:
            text = page.extractText()
            file_writer.write(f"{text}")

    return str(output)


def crop_page(pdf_path: str) -> str:
    """Crop a PDF page with left/right side.

    Args:
        pdf_path: pdf file to crop

    Returns:
        File path of the PDF page after cropped
    """
    pdf_reader = PdfFileReader(pdf_path)

    first_page = pdf_reader.getPage(0)

    left_side = copy.deepcopy(first_page)
    right_side = copy.deepcopy(first_page)

    current_coords = left_side.mediaBox.upperRight
    new_corrds = (current_coords[0] / 2, current_coords[1])

    left_side.mediaBox.upperRight = new_corrds
    right_side.mediaBox.upperLeft = new_corrds

    pdf_writer = PdfFileWriter()
    pdf_writer.addPage(left_side)
    pdf_writer.addPage(right_side)

    output = _CWD / _DIR_OUTPUT / "cropped.pdf"
    with output.open(mode="wb") as fw:
        pdf_writer.write(fw)

    return str(output)


def encrypt(  # nosec
    pdf_path: str, pwd_user: str = "super", pwd_owner: str = "demo"
) -> str:
    """Encrypt a PDF file with password(s).

    Args:
        pdf_path: pdf file to encrypt
        pwd_user: password of read-only
        pwd_owner: password for no restriction

    Returns:
        File path of the encrypted PDF
    """
    output = _CWD / _DIR_OUTPUT / "encrypted.pdf"

    pdf_reader = PdfFileReader(pdf_path)
    pdf_writer = PdfFileWriter()
    pdf_writer.encrypt(user_pwd=pwd_user, owner_pwd=pwd_owner)

    for page in pdf_reader.pages:
        pdf_writer.addPage(page)

    with open(output, "wb") as f_w:
        pdf_writer.write(f_w)

    return str(output)


def decrypt(pdf_encrypted: str, password: str = "demo") -> str:  # nosec
    """Decrypt a PDF file with password.

    Args:
        pdf_encrypted: the encrypted PDF file
        password: password used to decrypt

    Returns:
        File path of the PDF decrypted
    """
    output = _CWD / _DIR_OUTPUT / "decrypted.pdf"

    pdf_reader = PdfFileReader(pdf_encrypted)
    pdf_reader.decrypt(password=password)

    pdf_writer = PdfFileWriter()
    for page in pdf_reader.pages:
        pdf_writer.addPage(page)

    with open(output, "wb") as f_w:
        pdf_writer.write(f_w)

    return str(output)


def draft_blank(pdf_path: str) -> None:
    """Draft a blank PDF file.

    Args:
        pdf_path: file path to the drafted PDF
    """
    canvas = Canvas(pdf_path, pagesize=(8.5 * units.inch, 11 * units.inch))
    canvas.setFont("Times-Roman", 12)

    canvas.drawString(72, 72, "Sample Drawing")

    canvas.setFillColor(colors.blue)

    canvas.drawString(1 * units.inch, 10 * units.inch, "Blue text")

    canvas.save()

    return
