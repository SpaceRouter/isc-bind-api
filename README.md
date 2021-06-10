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

	const response = await fetch("http://localhost:8090/add", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({
        Answer: 192.168.1.70,
        Hostname: "devtest" + ".opengate.lan",
        RecordType: A,
        TTL: 300,
      }),
    });

    curl -H "Content-Type: application/json" -d '{"Hostname":"devtest.opengate.lan","TTL":"300","RecordType":"A","Answer":"192.168.1.70"}' -X POST http://localhost:8090/add

**UPDATE DNS record:**

Update a DNS record

    const response = await fetch("http://localhost:8090/update", {
      method: "PUT",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({
        Answer: 192.168.1.71,
        Hostname: "devtest" + ".opengate.lan",
        RecordType: A,
        TTL: 300,
      }),
    });

    curl -H "Content-Type: application/json" -d '{"Hostname":"devtest.opengate.lan","TTL":"300","RecordType":"A","Answer":"192.168.1.71"}' -X PUT http://localhost:8090/update

**DELETE DNS record:**

Delete a DNS record

    const response = await fetch("http://localhost:8090/delete", {
      method: "DELETE",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({
        Hostname: "devtest" + ".opengate.lan",
        RecordType: A,
      }),
    });

    curl -H "Content-Type: application/json" -d '{"Hostname":"devtest.opengate.lan","RecordType":"A"}' -X DELETE http://localhost:8090/delete

**SHOW Entire Zone:**

Retrieve data regarding the specified zone.

    const response = await fetch("http://localhost:8090/zone");

    curl http://localhost:8090/zone

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
