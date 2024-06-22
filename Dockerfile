FROM python:3.12.3-slim

WORKDIR /usr/src/app

COPY . .

RUN pip3 install --no-cache-dir -r requirements.txt

CMD ["python", "-m", "fazbot"]
