#!/bin/bash
url=$1
wget -O file.cpp "$url" &> /dev/null
cpplint file.cpp
rm file.cpp
