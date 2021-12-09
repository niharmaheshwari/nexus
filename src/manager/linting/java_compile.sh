#!/bin/bash
url=$1
filename=$(basename "$url")
wget "$url" &> /dev/null
javac "$filename"
rm "$filename"
