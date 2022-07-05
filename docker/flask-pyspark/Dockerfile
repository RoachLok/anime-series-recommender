FROM python:3.10.5

WORKDIR /app
COPY . .

RUN apt-get update && \
apt-get install -y openjdk-11-jdk && \
rm -rf /var/lib/apt/lists/*

RUN pip install -r requirements.txt

ENTRYPOINT ["python"]
CMD ["app.py"]