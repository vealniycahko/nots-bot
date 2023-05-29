FROM python:3.11.3

WORKDIR /notes_bot

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY aiobot/ ./aiobot
COPY logs/ ./logs
COPY migrations/ ./migrations
