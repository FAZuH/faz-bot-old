FROM python:3.12.3-slim

WORKDIR /FazBot
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "-m", "fazbot"]
