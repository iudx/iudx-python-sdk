import sys
import json
import requests

class iudx:
#
	def get_metadata(items, catalog = "varanasi.iudx.org.in"):

		if type(items) == type("string"):
			items = [items]
		else:
			items = items

		catalog = "https://" + catalog + "/catalogue/v1/items/"

		result = {}

		for i in items:
			url = catalog + i 

			response = requests.get(url=url,verify=True)

			if response.status_code == 200:
				result[i] = json.loads(response.text)[0]
			else:
				sys.stderr.write (
					"WARNING: catalogue API failure  | " +
					url + "/" + " | " +
					response.reason + " | " +
					response.text
				)

				result[i] = None 

		return result

	def get_latest_data(items,certificate = None, key = None):

		if type(items) == type("string"):
			items = [items]
		else:
			items = items

		if certificate and key:
			credentials = (certificate, key)

		result = {}

		metadata = iudx.get_metadata(items) 

		for i in items:
			split = i.split("/")
			rs = split[2]
			provider = metadata[i]["providerId"].split(":")[-1]

			url  = "https://" + rs + "/resource-server/" + provider + "/v1/search"

			body = {
				"id" : i,
				"options" : "latest"
			}

			body = json.dumps(body)
			response = requests.post(url=url,verify=True,data=body)

			if response.status_code == 200:
				result[i] = json.loads(response.text)
			else:
				sys.stderr.write (
					"WARNING: resource-server API failure  | " +
					url + "/" + " | " +
					response.reason + " | " +
					response.text
				)

				result[i] = None
		return result
#	
