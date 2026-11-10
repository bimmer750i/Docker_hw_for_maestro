FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN groupadd -g 10001 user && \
    useradd -g 10001 user && \
    chown -R user:user /app

USER user

CMD ["uvicorn","main:app","--port","8000","--host","0.0.0.0"]

