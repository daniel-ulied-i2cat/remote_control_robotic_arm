FROM python:3.11.8-alpine3.19

WORKDIR /app

ADD src/ /app
ADD requirements.txt /
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install -r /requirements.txt
RUN pip install pyniryo2

ENTRYPOINT [ "python", "-u", "latency_test.py"]
