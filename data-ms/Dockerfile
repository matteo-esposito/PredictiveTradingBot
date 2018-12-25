FROM python:3.6-alpine

MAINTAINER Kevin Tan 

COPY requirements.txt /

RUN pip install -r requirements.txt

COPY src/ /app
WORKDIR /app

EXPOSE 80
ENTRYPOINT ["python"]
CMD ["app.py"]
