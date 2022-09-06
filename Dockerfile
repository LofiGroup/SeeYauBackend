FROM python:3.10

ENV PYTHONUNBUFFERED=1
ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .

COPY wait-for-it.sh ./
ENTRYPOINT ["sh", "./entrypoint.sh"]
