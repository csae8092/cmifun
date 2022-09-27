#!/bin/bash

echo "download cmi files"
python fetch_data.py

echo "extract metadata from single cmi files"
python extract_md.py

echo "enrich (geonames lookup)"
python enrich_md.py

echo "Prepare Data"
python make_stats.py

echo "Build the HTML pages"

python build_website.py