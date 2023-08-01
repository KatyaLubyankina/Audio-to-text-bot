FROM python:3.10.10

COPY . .

RUN pip install poetry

RUN poetry config virtualenvs.create false

RUN poetry install --no-root

EXPOSE 80

CMD python -m uvicorn src.main:app --host 0.0.0.0 --port 80