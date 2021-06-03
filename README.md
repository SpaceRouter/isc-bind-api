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
	"safe.lan.": [
    	{
		"Answer": "ns",
		"Hostname": "@",
		"RecordType": 2,
		"TTL": 604800
	}, 
    	{
		"Answer": "192.168.1.1",
		"Hostname": "ns",
		"RecordType": 1,
		"TTL": 604800
	}, 
		{
		"Answer": "192.168.1.50",
		"Hostname": "test",
		"RecordType": 1,
		"TTL": 604800
	}, 
		{
		"Answer": "192.168.1.51",
		"Hostname": "test1",
		"RecordType": 1,
		"TTL": 604800
	}]
}
```
