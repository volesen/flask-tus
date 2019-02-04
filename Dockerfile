FROM python:3.7-alpine

WORKDIR /app

COPY . /app

RUN pip install -e .[testing]

CMD ["python", "example/app.py"]
