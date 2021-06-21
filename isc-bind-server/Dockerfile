FROM alpine:latest

LABEL "space.opengate.vendor"="SpaceRouter"
LABEL org.opencontainers.image.source https://github.com/SpaceRouter/isc-bind-api
LABEL space.opengate.image.authors="theo.lefevre@edu.esiee.fr"

RUN apk add --no-cache --purge -uU tzdata bind
RUN rm -rf /var/cache/apk/* /tmp/*

RUN mkdir -p /etc/bind && chown root:root /etc/bind/ && chmod 755 /etc/bind
RUN mkdir -p /var/cache/bind && chown root:root /var/cache/bind && chmod 755 /var/cache/bind
RUN mkdir -p /var/lib/bind && chown root:root /var/lib/bind && chmod 755 /var/lib/bind
RUN mkdir -p /var/log/bind && chown root:root /var/log/bind && chmod 755 /var/log/bind
RUN mkdir -p /run/named && chown root:root /run/named && chmod 755 /run/named

RUN mkdir -p bind
COPY entrypoint.sh /bind/entrypoint.sh
RUN chmod +x /bind/entrypoint.sh

EXPOSE 53/udp 53/tcp 953/tcp

ENTRYPOINT ["sh", "/bind/entrypoint.sh"]
