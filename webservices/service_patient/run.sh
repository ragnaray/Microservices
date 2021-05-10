#!/bin/sh

cd patient
echo "building"
pip install -r requirements.txt
echo "running"
python patient.py