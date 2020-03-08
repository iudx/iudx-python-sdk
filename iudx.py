import sys
import json
import requests

catalog_of_catalogs = "varanasi.iudx.org.in" # should be "catalogue.iudx.org.in"

class iudx:
#{
	def __init__(self,certificate,key):
		if certificate and key:
			self.credentials = (certificate,key)
		else:
			self.credentials = None

	@staticmethod
	def search(options =  {}, catalog = catalog_of_catalogs):
		catalog = "https://" + catalog + "/catalogue/v1/search"
		response = requests.get(catalog)
		return json.loads(response.text)

	@staticmethod
	def get_metadata(items, catalog = catalog_of_catalogs):

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

	@staticmethod
	def get_latest_data(items, token = None, server_token = None):

		if type(items) == type("string"):
			items = [items]
		else:
			items = items

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

			if token:
				body["token"]		= token
				body["server-token"]	= server_token[rs] 

			body = json.dumps(body)
			response = requests.post(url=url,verify=True,data=body)

			if response.status_code == 200:
				result[i] = json.loads(response.text)[0]
			else:
				sys.stderr.write (
					"WARNING: resource-server API failure  | " +
					url + "/" + " | " +
					response.reason + " | " +
					response.text
				)

				result[i] = None
		return result

	class auth:
	#{
		def __init__(self, certificate, key, auth_server="auth.iudx.org.in", version=1):
			self.url = "https://" + auth_server + "/auth/v" + str(version)
			self.credentials = (certificate, key)

		def call(self, api, body=None):
			ret = True # success
			body = json.dumps(body)
			response = requests.post (
				url=self.url + "/" + api,
				verify=True,
				cert=self.credentials,
				data=body,
				headers={"content-type": "application/json"}
        		)

			if response.status_code != 200:
				sys.stderr.write(
					"WARNING: auth API failure  | " +
					self.url + "/" + api + " | " +
					response.reason + " | " +
					response.text
            			)

				ret = False # failed

				if response.headers['content-type'] == 'application/json':
					return {'success':ret, 'response':json.loads(response.text)}
				else:
					sys.stderr.write(
						"WARNING: auth did not send 'application/json'"
            				)
					return {'success':False, 'response':None}

		def get_token(self, request, token_time=None, existing_token=None):
			body = {'request': request}

			if token_time:
				body['token-time'] = token_time

			if existing_token:
				body['existing-token'] = existing_token

			return self.call("token", body)

		def get_certificate_info(self):
			return self.call("certificate-info")

		def get_policy(self):
			return self.call("acl")

		def set_policy(self, policy):
			body = {'policy': policy}
			return self.call("acl/set", body)

		def append_policy(self, policy):
			body = {'policy': policy}
			return self.call("acl/append", body)

		def introspect_token(self, token, server_token=None):
			body = {'token': token}

			if server_token:
            			body['server-token'] = server_token

			return self.call("token/introspect", body)

		def revoke_tokens(self, tokens):
			if type(tokens) is type([]):
				body = {'tokens': tokens}
			else:
				body = {'tokens': [tokens]}

			return self.call("token/revoke", body)

		def revoke_token_hashes(self, token_hashes):
			if type(token_hashes) is type([]):
				body = {'token-hashes': token_hashes}
			else:
				body = {'token-hashes': [token_hashes]}

			return self.call("token/revoke", body)

		def revoke_all(self, serial, fingerprint):
			body = {'serial':serial, 'fingerprint': fingerprint}
			return self.call("token/revoke-all", body)

		def audit_tokens(self, hours):
			body = {'hours': hours}
			return self.call("audit/tokens", body)

		def add_consumer_to_group(self, consumer, group, valid_till):
			body = {'consumer': consumer, 'group': group, 'valid-till': valid_till}
			return self.call("group/add", body)

		def delete_consumer_from_group(self, consumer, group):
			body = {'consumer': consumer, 'group': group}
			return self.call("group/delete", body)

		def list_group(self, consumer, group=None):
			body = {'consumer': consumer}

			if group:
				body['group'] = group

			return self.call("group/list", body)
	#}
#}
