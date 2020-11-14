#!/usr/bin/env bash

# remove distribution folders in current directory
rm -rf "${PWD}/build/"
rm -rf "${PWD}/dist/"
# do not know how to match egg directory name properly
rm -rf *.egg-info/
