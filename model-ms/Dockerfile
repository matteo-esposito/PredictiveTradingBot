FROM python:3.6-alpine

MAINTAINER Matteo Esposito 

RUN \
 apk add --update --no-cache g++ gcc libxslt-dev && \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev

COPY ./requirements.txt /app/requirements.txt
WORKDIR /app

RUN \
 python3 -m pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps

COPY .  /app

ENTRYPOINT ["python3"]
CMD ["/app/app/model.py"]
