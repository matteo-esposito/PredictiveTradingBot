FROM python:3.6-alpine

MAINTAINER Kevin Tan 

COPY requirements.txt /

RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
 python3 -m pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps

COPY src/ /app
WORKDIR /app

EXPOSE 80
ENTRYPOINT ["python"]
CMD ["app.py"]
