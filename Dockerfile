FROM python:3.9.5
COPY requirements.txt /requirements.txt
COPY update_fixV.py /update_fixV.py
COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
