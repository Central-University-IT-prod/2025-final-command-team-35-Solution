FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update
RUN apt-get -y install curl

COPY . /app

EXPOSE 443
CMD ["uvicorn", "api.main:app", "--port", "443", "--host=0.0.0.0", "--ssl-certfile", "/api/ssl/chain.pem", "--ssl-keyfile", "/api/ssl/privkey.pem"]