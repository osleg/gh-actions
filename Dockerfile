FROM python:3.9.5

COPY . /app
WORKDIR /app

RUN pip install -r /app/requirements.txt

ENTRYPOINT ["/app/entrypoint.sh"]
