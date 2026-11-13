FROM python:3.14-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

RUN apt-get update && apt-get install curl -y

COPY . .

RUN groupadd -g 10001 user && \
    useradd -g 10001 user && \
    chown -R user:user /app

USER user

ENTRYPOINT ["uvicorn"]

CMD ["main:app","--port","8000","--host","0.0.0.0" ]