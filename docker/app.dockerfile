FROM python:3.10-slim

WORKDIR /work

COPY . /work

RUN pip install poetry
RUN poetry install --without doc --without dev

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "asgi:application", "--host", "0.0.0.0", "--port", "8000"]

