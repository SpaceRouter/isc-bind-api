# isc-bind-api

PYTHON REST API for isc-bind-server (soon using jwt authentication)

Run:
----
    python isc-bind-api.py

Record Types :
---------
RECORD_TYPES  = ['A', 'AAAA', 'CNAME', 'MX', 'NS', 'TXT', 'SOA']

API List :
---------

**ADD DNS record:**

Create a DNS record

    curl -i -H "Content-Type: application/json" -X POST http://localhost:8090/dns/record/test.safe.lan/604800/A/192.168.1.60

**DELETE DNS record:**

Delete a DNS record

    curl -i -H "Content-Type: application/json" -X DELETE http://localhost:8090/dns/record/test.safe.lan/604800/A/192.168.1.60

**UPDATE DNS record:**

Update a DNS record

    curl -i -H "Content-Type: application/json" -X PUT http://localhost:8090/dns/record/test.safe.lan/604800/A/192.168.1.61

**SHOW Entire Zone:**

Retrieve data regarding the specified zone.

    curl http://localhost:8090/dns/zone/safe.lan

Return example:

```
{
	"safe.lan.": {
		"test": [{
			"Answer": "192.168.1.50",
			"RecordType": 1,
			"TTL": 604800
		}],
		"@": [{
			"Answer": "ns",
			"RecordType": 2,
			"TTL": 604800
		}],
		"ns": [{
			"Answer": "192.168.1.1",
			"RecordType": 1,
			"TTL": 604800
		}],
		"test1": [{
			"Answer": "192.168.1.51",
			"RecordType": 1,
			"TTL": 604800
		}]
	}
}
```
