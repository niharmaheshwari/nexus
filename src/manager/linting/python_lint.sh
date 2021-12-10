#!/bin/bash
url=$1
filename=$(basename "$url")
wget "$url" &> /dev/null
pylint "$filename"
rm "$filename"