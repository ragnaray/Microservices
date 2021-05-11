#!/bin/sh

cd medication
echo "building"
python3 -m pip install -r requirements.txt --no-cache-dir
echo "running"
python medication.py