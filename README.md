# iudx-python-sdk

```
from iudx import *

# get data
iudx.get_latest_data("rbccps.org/aa9d66a000d94a78895de8d4c0b3a67f3450e531/rs.varanasi.iudx.org.in/varanasi-aqm/EM_01_0102_01")

test_ids = [
	"rbccps.org/aa9d66a000d94a78895de8d4c0b3a67f3450e531/rs.varanasi.iudx.org.in/varanasi-aqm/EM_01_0102_01",
	"rbccps.org/aa9d66a000d94a78895de8d4c0b3a67f3450e531/rs.varanasi.iudx.org.in/varanasi-aqm/EM_01_0101_01",
]

print (iudx.get_latest_data(test_ids))

# search for all ids in the catalog 
all_ids = iudx.search()

# search and get count of for data sets with options
print("Number of pollution sensors",iudx.search_count({"tags": ["aqi", "aqm"]}))

# get an access token
auth = iudx.auth("certificate.pem","private-key.pem")
auth.get_token(test_ids)

```
