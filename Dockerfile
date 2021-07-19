FROM python:3.10-rc-slim-buster

WORKDIR /fetch
COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt
COPY fetch.py .
RUN chmod 700 fetch.py
ENTRYPOINT ["bash"]
