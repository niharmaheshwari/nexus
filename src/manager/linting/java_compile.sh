#!/bin/bash
url=$1
wget -O file.java "$url" &> /dev/null
javac file.java
rm file.java