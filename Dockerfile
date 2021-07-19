FROM python:3.10-rc-slim-buster

COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt
COPY fetch.py .
CMD python3 fetch.py
