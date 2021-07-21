#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Any, List

from PyPDF2 import PdfFileReader
from PyPDF2 import PdfFileWriter


def extract_information(pdf_path: str) -> Any:
    """Extract meta of the PDF file.

    Args:
        pdf_path: path to the pdf file

    Returns:
        The meta information
    """
    with open(pdf_path, "rb") as f:
        pdf = PdfFileReader(f)
        information = pdf.getDocumentInfo()
        number_of_pages = pdf.getNumPages()

    txt = f"""
        Information about {pdf_path}:

        Author: {information.author}
        Creator: {information.creator}
        Producer: {information.producer}
        Subject: {information.subject}
        Title: {information.title}
        Number of pages: {number_of_pages}
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
    # rotate page 90 degrees to the right
    page_1 = pdf_reader.getPage(0).rotateClockwise(90)
    pdf_writer.addPage(page_1)
    # rotate page 90 degrees to the left
    page_2 = pdf_reader.getPage(1).rotateCounterClockwise(90)
    pdf_writer.addPage(page_2)
    # add a page in normal orientation
    pdf_writer.addPage(pdf_reader.getPage(2))

    with open(pdf_new, "wb") as fh:
        pdf_writer.write(fh)

    return


def merge_pdfs(pdf_paths: List[str], output: str) -> None:
    """Merge a list of pdf files into one.

    Args:
        pdf_paths: a list of pdf files to merge
        output: pdf file after merged
    """
    pdf_writer = PdfFileWriter()

    for path in pdf_paths:
        pdf_reader = PdfFileReader(path)
        for page in range(pdf_reader.getNumPages()):
            # add each page to the writer object
            pdf_writer.addPage(pdf_reader.getPage(page))

    # write out the merged PDF
    with open(output, "wb") as out:
        pdf_writer.write(out)

    return


def split_pdf(pdf_path: str, prefix: str) -> None:
    """Split a PDF file into individual pages.

    Args:
        pdf_path: pdf file to split
        prefixes: prefix used in generated pdf pages
    """
    pdf = PdfFileReader(pdf_path)
    pages = pdf.getNumPages()

    for index in range(pages):
        page = index + 1

        pdf_writer = PdfFileWriter()
        pdf_writer.addPage(pdf.getPage(index))

        output = f"{prefix}_{page}.pdf"
        with open(output, "wb") as output_pdf:
            pdf_writer.write(output_pdf)

    return


def create_watermark(pdf_path: str, watermark_pdf: str, output: str) -> None:
    """Embeded watermark to the PDF.

    Args:
        pdf_path: pdf file to embed watermark
        watermark_pdf: watermark to embed, which is expected to be a PDF file
        output: pdf file after watermark embedded
    """
    watermark_obj = PdfFileReader(watermark_pdf)
    watermark_page = watermark_obj.getPage(0)

    pdf_reader = PdfFileReader(pdf_path)
    pdf_writer = PdfFileWriter()

    pages = pdf_reader.getNumPages()
    # watermark all the pages
    for page in range(pages):
        single_page = pdf_reader.getPage(page)
        single_page.mergePage(watermark_page)
        pdf_writer.addPage(single_page)

    with open(output, "wb") as out:
        pdf_writer.write(out)


if __name__ == "__main__":
    path = "sample.pdf"

    # extract_information(pdf_old=path)

    # rotate_pages(pdf_old=path, pdf_new='rotate_pages.pdf')

    # merge_pdfs(pdf_paths=[path, path], output='merged.pdf')

    # split_pdf(pdf_path=path, prefix="a")

    # create_watermark(
    #     pdf_path=path,
    #     watermark_pdf="icon.pdf",
    #     output="output.pdf",
    # )
