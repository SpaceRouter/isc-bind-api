FROM python:2.7-slim

LABEL "space.opengate.vendor"="SpaceRouter"
LABEL org.opencontainers.image.source https://github.com/SpaceRouter/isc-bind-api
LABEL space.opengate.image.authors="theo.lefevre@edu.esiee.fr"

RUN mkdir /usr/src/app/
COPY src /usr/src/app/

WORKDIR /usr/src/app/
RUN pip install -r requirements.txt

EXPOSE 8090

CMD ["python", "isc-bind-api.py"]

