name = "PwnedPy"

import requests
import json

headers = {
	'User-Agent': 'PwnedPy v1.0-May-2019'
}

def getBreaches(account, Truncated=False, Unverified=False):
	params = (("truncateResponse", Truncated),("includeUnverified",Unverified))
	account = str(account)
	baseURL = "https://haveibeenpwned.com/api/v2/breachedaccount/"
	url = baseURL + account
	response = requests.get(url, headers=headers, params=params)
	return response.json()

def getBreachesByDomain(account, domain, Truncated=False, Unverified=False):
	params = (("domain", domain),("truncateResponse", Truncated),("includeUnverified",Unverified))
	account = str(account)
	domain = str(domain)
	baseURL = "https://haveibeenpwned.com/api/v2/breachedaccount/"
	url = baseURL + account
	try:
		response = requests.get(url, headers=headers, params=params)
	except:
		print("Are you sure your inputs were valid?")
	return response.json()

def getAllBreaches(domain=""):
	params = (("domain",domain),)
	url = "https://haveibeenpwned.com/api/v2/breaches"
	response = requests.get(url, headers=headers, params=params)
	return response.json()

def getPastes(account):
	account = str(account)
	baseURL = "https://haveibeenpwned.com/api/v2/pasteaccount/"
	url = baseURL + account
	print(account + "\n" + url)
	response = requests.get(url, headers=headers)
	return response.json()

