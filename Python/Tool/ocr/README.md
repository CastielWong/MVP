
- [Instruction](#instruction)
- [Reference](#reference)


## Instruction
1. Place the image to "scan" under directory "images"
2. Update the name for variable `image_name` correspondingly
3. Run `make start` to have the Docker container, whose image had already OCR baked inside, up and running
4. Run `make run` to get into the container
5. Run `python src/__main__.py` for the converted text
6. After everything is done, exit the container then `make stop`


## Reference
- Setting up a Simple OCR Server: https://realpython.com/setting-up-a-simple-ocr-server/
- Tesseract documentation: https://tesseract-ocr.github.io/tessdoc
