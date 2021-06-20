FROM python:3.9.5
COPY requirements.txt /github/workspace/requirements.txt
COPY update_fixV.py /github/workspace/update_fixV.py
COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
