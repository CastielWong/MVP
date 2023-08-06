#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Entry point to PDF toolkit."""
from argparse import ArgumentParser, Namespace
from pathlib import Path

from pdf import operation as op

_CWD = Path(__file__).parent.absolute()
DEFAULT_OUTPUT = _CWD / "output"


def get_cli_args() -> Namespace:
    """Get command line arguments.

    Returns:
        Arguments parsed
    """
    parser = ArgumentParser(description="Used to manipulate PDF file for customization")
    parser.add_argument(
        "--operation",
        help="indicate what operation to perform",
        type=str,
        choices=["split"],
        default="split",
    )
    parser.add_argument(
        "--name",
        help="PDF file name to process",
        required=True,
        type=str,
    )
    parser.add_argument(
        "--output",
        help="directory for output to persist, by default it's 'pdf/output'",
        required=False,
        type=str,
        default=DEFAULT_OUTPUT,
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = get_cli_args()
    file_name = args.name

    if args.operation == "split":
        op.split_pdf(pdf_path=file_name, dir_output=args.output, prefix="o")
    # elif args.operation == "draft":
    #     op.draft_blank(pdf_path=f"{args.output}/blank.pdf")
    # elif args.operation == "extract":
    #     op.extract_information(pdf_path=file_name)
    # elif args.operation == "rotate":
    #     op.rotate_pages(pdf_old=file_name, pdf_new=f"{args.output}/rotated.pdf")
    # elif args.operation == "merge":
    #     op.merge_pdfs(
    #         pdf_paths=["core/output/a_1.pdf", "core/output/a_2.pdf"],
    #         output=f"{args.output}/merged.pdf"
    #     )
    # elif args.operation == "watermark":
    #     op.create_watermark(
    #         pdf_path=file_name,
    #         watermark_pdf="icon.pdf",
    #         output=f"{args.output}/watermarked.pdf",
    #     )
    # elif args.operation == "text":
    #     op.convert_to_txt(pdf_path=file_name)
    # elif args.operation == "crop":
    #     op.crop_page(pdf_path=file_name)
    # elif args.operation == "decrypt":
    #     file_encrypted = op.encrypt(pdf_path=file_name)
    #     op.decrypt(pdf_encrypted=file_encrypted)
