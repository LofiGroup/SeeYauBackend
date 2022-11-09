FROM python:3.10.7-bullseye

ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .

ENTRYPOINT ["bash", "./entrypoint.sh"]
