#!/usr/bin bash

echo "Removing previous/cached compiled files..."
rm -rf build
rm *.c
rm *.so

echo "-------------------------------------------"

# compile cython file
python setup.py build_ext --inplace

echo "-------------------------------------------"

# run the demo
python demo_cython.py
