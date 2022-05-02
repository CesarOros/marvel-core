FROM alpine:3.14

RUN apk add --no-cache python3-dev py3-pip \
    && pip3 install --upgrade pip

WORKDIR /app

COPY . /app

RUN pip3 --no-cache-dir install --ignore-installed -r requirements.txt

CMD ["python3", "app.py"]