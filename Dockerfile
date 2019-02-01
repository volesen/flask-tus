FROM python:3.7-alpine

WORKDIR /app

COPY requirements.txt /

RUN pip install -r /requirements.txt

COPY . /app

RUN python setup.py install

CMD ["python", "example/app.py"]
