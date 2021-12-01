#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Optimize PDF file."""
from PDFNetPython3 import (
    PDFNet,
    PDFDoc,
    Optimizer,
    SDFDoc,
    ImageSettings,
    OptimizerSettings,
)

LICENSE_KEY = (
    "demo:1637609990859:789041bb0300000000ef1e5d101d796ab23fe11159b58361391ad4e108"
)


def main():
    """Execute as the entry point."""
    input_path = "./input/"
    output_path = "./output/"
    input_filename = ""

    PDFNet.Initialize(LICENSE_KEY)

    doc = PDFDoc(input_path + input_filename + ".pdf")
    doc.InitSecurityHandler()

    image_settings = ImageSettings()

    # low quality jpeg compression
    image_settings.SetCompressionMode(ImageSettings.e_jpeg)
    image_settings.SetQuality(8)

    # Set the output dpi to be standard screen resolution
    image_settings.SetImageDPI(144, 96)

    # this option will recompress images not compressed with
    # jpeg compression and use the result if the new image
    # is smaller.
    image_settings.ForceRecompression(True)

    # this option is not commonly used since it can
    # potentially lead to larger files.  It should be enabled
    # only if the output compression specified should be applied
    # to every image of a given type regardless of the output image size
    # image_settings.ForceChanges(True)

    opt_settings = OptimizerSettings()
    opt_settings.SetColorImageSettings(image_settings)
    opt_settings.SetGrayscaleImageSettings(image_settings)

    # use the same settings for both color and grayscale images
    Optimizer.Optimize(doc, opt_settings)

    doc.Save(output_path + input_filename + "_opt2.pdf", SDFDoc.e_linearized)
    doc.Close()

    return


if __name__ == "__main__":
    print("Starting...")

    main()

    print("Finished.")
