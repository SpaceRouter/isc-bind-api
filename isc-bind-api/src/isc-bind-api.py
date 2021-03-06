#!/usr/bin/env python

from bottle import route, run, request, response
import json
import os
from dns.rdatatype import *
import dns.tsigkeyring
import dns.resolver
import dns.update
import dns.query
import dns.zone

ZONE            = os.environ['ZONE']
DNS_SERVER      = os.environ['SERVER']
TSIG_USERNAME   = os.environ['TSIG_KEY']
TSIG_PASSWORD   = os.environ['TSIG_SECRET']
VALID_ZONES     = [i + '.' for i in os.environ['ZONE'].split(',')]
RECORD_TYPES    = ['A', 'AAAA', 'CNAME', 'MX', 'NS', 'TXT', 'SOA']

def enable_cors(fn):
  def _enable_cors(*args, **kwargs):
      response.content_type = 'application/json'
      response.headers['Access-Control-Allow-Origin'] = '*'
      response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS, DELETE'
      response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

      if request.method != 'OPTIONS':
          # actual request; reply with the actual response
          return fn(*args, **kwargs)

  return _enable_cors

@route('/dns/zone')
@enable_cors
def get_zone():
    zone_name = ZONE
    item = dict()
    records = []

    if not zone_name.endswith('.'):
        zone_name = zone_name + '.'

    if zone_name not in VALID_ZONES:
        response.status = 500
        return json.dumps({'error': 'invalid zone'})
    try:
        zone = dns.zone.from_xfr(dns.query.xfr(DNS_SERVER, zone_name))
    except dns.exception.FormError:
        response.status = 500
        return json.dumps({'fail': zone_name})

    for (name, ttl, rdata) in zone.iterate_rdatas():
        if rdata.rdtype != SOA:
            item = dict(Hostname=str(name), Answer=str(rdata), RecordType=rdata.rdtype, TTL=ttl)
            records.append(item)

    response.status = 200
    return json.dumps({zone_name: records})

@route('/dns/add', method=['POST', 'OPTIONS'])
@enable_cors
def add():
    data = request.json
    domain = data['Hostname']
    ttl = data['TTL']
    record_type = data['RecordType']
    answer = data['Answer']

    zone = '.'.join(dns.name.from_text(domain).labels[1:])

    if record_type not in RECORD_TYPES:
        response.status = 500
        return json.dumps({'error': 'not a valid record type'})

    if zone not in VALID_ZONES:
        response.status = 500
        return json.dumps({'error': 'not a valid zone'})

    tsig = dns.tsigkeyring.from_text({TSIG_USERNAME: TSIG_PASSWORD})
    action = dns.update.Update(zone, keyring=tsig)
    action.add(dns.name.from_text(domain).labels[0], ttl, str(record_type), str(answer))

    try:
        query = dns.query.tcp(action, DNS_SERVER)
    except:
        response.status = 500
        return json.dumps({'error': 'DNS transaction failed'})

    if query.rcode() == 0:
        response.status = 200
        return json.dumps({domain: 'DNS request successful'})
    else:
        response.status = 500
        return json.dumps({domain: 'DNS request failed'})

@route('/dns/update', method=['PUT', 'OPTIONS'])
@enable_cors
def update():
    data = request.json
    domain = data['Hostname']
    ttl = data['TTL']
    record_type = data['RecordType']
    answer = data['Answer']

    zone = '.'.join(dns.name.from_text(domain).labels[1:])

    if record_type not in RECORD_TYPES:
        response.status = 500
        return json.dumps({'error': 'not a valid record type'})

    if zone not in VALID_ZONES:
        response.status = 500
        return json.dumps({'error': 'not a valid zone'})

    resolver = dns.resolver.Resolver()
    resolver.nameservers = [DNS_SERVER]

    try:
        query = resolver.query(domain, record_type)
    except dns.resolver.NXDOMAIN:
        response.status = 500
        return json.dumps({'error': 'domain does not exist'})

    tsig = dns.tsigkeyring.from_text({TSIG_USERNAME: TSIG_PASSWORD})
    action = dns.update.Update(zone, keyring=tsig)
    action.replace(dns.name.from_text(domain).labels[0], ttl, str(record_type), str(answer))
    try:
        query = dns.query.tcp(action, DNS_SERVER)
    except:
        response.status = 500
        return json.dumps({'error': 'DNS transaction failed'})

    if query.rcode() == 0:
        response.status = 200
        return json.dumps({domain: 'DNS request successful'})
    else:
        response.status = 500
        return json.dumps({domain: 'DNS request failed'})

@route('/dns/delete', method=['DELETE', 'OPTIONS'])
@enable_cors
def delete():
    data = request.json
    domain = data['Hostname']
    record_type = data['RecordType']

    zone = '.'.join(dns.name.from_text(domain).labels[1:])

    if record_type not in RECORD_TYPES:
        response.status = 500
        return json.dumps({'error': 'not a valid record type'})

    if zone not in VALID_ZONES:
        response.status = 500
        return json.dumps({'error': 'not a valid zone'})

    resolver = dns.resolver.Resolver()
    resolver.nameservers = [DNS_SERVER]

    try:
        query = resolver.query(domain, record_type)
    except dns.resolver.NXDOMAIN:
        response.status = 500
        return json.dumps({'error': 'domain does not exist'})

    tsig = dns.tsigkeyring.from_text({TSIG_USERNAME: TSIG_PASSWORD})
    action = dns.update.Update(zone, keyring=tsig)
    action.delete(dns.name.from_text(domain).labels[0])

    try:
        query = dns.query.tcp(action, DNS_SERVER)
    except:
        response.status = 500
        return json.dumps({'error': 'DNS transaction failed'})

    if query.rcode() == 0:
        response.status = 200
        return json.dumps({domain: 'DNS request successful'})
    else:
        response.status = 500
        return json.dumps({domain: 'DNS request failed'})

run(host='0.0.0.0', port=8090, debug=False)
