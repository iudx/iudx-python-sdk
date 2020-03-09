from iudx import *

test_items = [
	"rbccps.org/aa9d66a000d94a78895de8d4c0b3a67f3450e531/rs.varanasi.iudx.org.in/varanasi-aqm/EM_01_0102_01",
	"rbccps.org/aa9d66a000d94a78895de8d4c0b3a67f3450e531/rs.varanasi.iudx.org.in/varanasi-aqm/EM_01_0101_01",
]

r = iudx.get_latest_data (test_items)

print(r)

entries = iudx.search()
length = iudx.search_count({"tags": ["aqi", "aqm"]})

assert len(entries) >= length

r = iudx.get_latest_data([
	entries[0]["id"],
	entries[1]["id"],
])

auth = iudx.auth("certificate.pem","private-key.pem")

