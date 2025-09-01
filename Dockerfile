FROM python:3.13-slim-bookworm
WORKDIR /livent_bot
RUN pip install --upgrade pip wheel poetry
RUN poetry config virtualenvs.create false
COPY ./poetry.lock ./poetry.lock
COPY ./pyproject.toml ./pyproject.toml
RUN poetry install --no-interaction
COPY . .
RUN chmod +x ./prestart.sh
RUN chmod +x ./start.sh
ENTRYPOINT ["./prestart.sh"]
CMD ["./start.sh"]