FROM python:3.10

WORKDIR /nots_bot

ENV PYTHONDONTWRITEBYTECODE 1 \
    PYTHONUNBUFFERED 1

ENV POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

COPY . .

RUN apt-get update \
    && apt-get install -y curl \
    && curl -sSL https://install.python-poetry.org | python3.10 -

RUN poetry install