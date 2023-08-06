import requests

def check(url):
	endpoint = 'https://isitup.org/' + url + '.json'
	response = requests.get(endpoint, verify = True)

	data = response.json()

	if data['status_code'] == 3:
		return 'Invalid domain'

	if data['status_code'] == 1: # Up
		return False

	if data['status_code'] == 2: # Down
		return True
