FROM python:3.12.3-slim

WORKDIR /usr/fazbot/app

COPY . /usr/fazbot/app

RUN pip3 install --no-cache-dir -r requirements.txt

CMD ["python", "-m", "fazbot"]
