FROM python:3.11.9-slim

WORKDIR /FazBot
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "-m", "fazbot"]

