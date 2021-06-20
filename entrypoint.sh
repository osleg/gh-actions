#!/bin/sh
pip install -r /requirements.txt &> /dev/null || return 0
python /update_fixV.py
