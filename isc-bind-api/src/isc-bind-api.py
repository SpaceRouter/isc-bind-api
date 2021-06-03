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

os.environ['ZONES'] = 'safe.lan'
os.environ['SERVER'] = '192.168.1.1'
os.environ['TSIG_USERNAME'] = 'TSIG'
os.environ['TSIG_PASSWORD'] = 'ze4byKPhDoxIfD2rAiWFsg=='

DNS_SERVER    = os.environ['SERVER']
TSIG_USERNAME = os.environ['TSIG_USERNAME']
TSIG_PASSWORD = os.environ['TSIG_PASSWORD']
VALID_ZONES   = [i + '.' for i in os.environ['ZONES'].split(',')]
RECORD_TYPES  = ['A', 'AAAA', 'CNAME', 'MX', 'NS', 'TXT', 'SOA']

def enable_cors(fn):
  def _enable_cors(*args, **kwargs):
      response.status = 200
      response.content_type = 'application/json'
      response.headers['Access-Control-Allow-Origin'] = '*'
      response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS, DELETE'
      response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

      if request.method != 'OPTIONS':
          # actual request; reply with the actual response
          return fn(*args, **kwargs)

  return _enable_cors

@route('/dns/zone/<zone_name>', method=['GET'])
@enable_cors
def get_zone(zone_name):
    item = dict()
    records = []

    if not zone_name.endswith('.'):
        zone_name = zone_name + '.'

    if zone_name not in VALID_ZONES:
        return json.dumps({'error': 'invalid zone'})

    try:
        zone = dns.zone.from_xfr(dns.query.xfr(DNS_SERVER, zone_name))
    except dns.exception.FormError:
        return json.dumps({'fail': zone_name})

    for (name, ttl, rdata) in zone.iterate_rdatas():
        if rdata.rdtype != SOA:
            item = dict(Hostname= str(name), Answer= str(rdata), RecordType= rdata.rdtype, TTL= ttl)
            records.append(item)
    return json.dumps({zone_name: records})

@route('/dns/record/<domain>/<ttl>/<record_type>/<response>', method=['PUT', 'POST', 'DELETE', 'OPTIONS'])
@enable_cors
def dns_mgmt(domain, ttl, record_type, response):
        zone = '.'.join(dns.name.from_text(domain).labels[1:])

        if record_type not in RECORD_TYPES:
            return json.dumps({'error': 'not a valid record type'})

        if zone not in VALID_ZONES:
            return json.dumps({'error': 'not a valid zone'})

        if request.method == 'PUT' or request.method == 'DELETE':
            resolver = dns.resolver.Resolver()
            resolver.nameservers = [DNS_SERVER]
            try:
                answer = resolver.query(domain, record_type)
            except dns.resolver.NXDOMAIN:
                return json.dumps({'error': 'domain does not exist'})

        tsig = dns.tsigkeyring.from_text({TSIG_USERNAME: TSIG_PASSWORD})
        action = dns.update.Update(zone, keyring=tsig)

        if request.method == 'DELETE':
            action.delete(dns.name.from_text(domain).labels[0])
        elif request.method == 'PUT':
            action.replace(dns.name.from_text(domain).labels[0], ttl, str(record_type), str(response))
        elif request.method == 'POST':
            action.add(dns.name.from_text(domain).labels[0], ttl, str(record_type), str(response))
        try:
            response = dns.query.tcp(action, DNS_SERVER)
        except:
            return json.dumps({'error': 'DNS transaction failed'})

        if response.rcode() == 0:
            return json.dumps({domain: 'DNS request successful'})
        else:
            return json.dumps({domain: 'DNS request failed'})

run(host='0.0.0.0', port=8090, debug=False)