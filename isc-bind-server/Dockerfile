FROM alpine

LABEL "space.opengate"="SAFEROUTER"
LABEL space.opengate.image.authors="theo.lefevre@edu.esiee.fr"

RUN apk add --no-cache bind

VOLUME ["/etc/bind", "/var/cache/bind", "/var/lib/bind", "/var/log", "/usr/share/dns/"]

RUN mkdir -p /etc/bind && chown root:root /etc/bind/ && chmod 755 /etc/bind
RUN mkdir -p /var/cache/bind && chown root:root /var/cache/bind && chmod 755 /var/cache/bind
RUN mkdir -p /var/lib/bind && chown root:root /var/lib/bind && chmod 755 /var/lib/bind
RUN mkdir -p /var/log/bind && chown root:root /var/log/bind && chmod 755 /var/log/bind
RUN mkdir -p /run/named && chown root:root /run/named && chmod 755 /run/named

EXPOSE 53/udp 53/tcp 953/tcp

CMD ["/usr/sbin/named", "-g", "-u", "root"]