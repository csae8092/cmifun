#!/bin/bash

echo "Prepare Data"
python make_stats.py

echo "Build the HTML pages"

python build_website.py