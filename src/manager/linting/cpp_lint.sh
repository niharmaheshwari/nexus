#!/bin/bash
url=$1
filename=$(basename "$url")
wget "$url" &> /dev/null
cpplint "$filename"
rm "$filename"
