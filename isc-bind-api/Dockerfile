FROM python

LABEL "fr.esieespace.saferouter"="SAFEROUTER"
LABEL fr.esieespace.saferouter.image.authors="theo.lefevre@edu.esiee.fr"

RUN mkdir /usr/src/app/
COPY src /usr/src/app/

WORKDIR /usr/src/app/
RUN pip install -r requirements.txt

EXPOSE 8090

CMD ["python", "isc-bind-api.py"]

