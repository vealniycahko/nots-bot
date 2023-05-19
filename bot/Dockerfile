FROM python:3.11.3

WORKDIR /bot_app

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY main.py .
COPY bot.log .
COPY database.py .
COPY migrations/ ./migrations/
