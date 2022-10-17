from cgitb import reset
import json
from urllib import response
import urllib.parse
from more_itertools import peekable
import requests
import time
from datetime import datetime
from scrapper_joaf import obtain_data
import sys

def extract_data(data, key):
    if data is None:
        return None
    if key in data:
        return data[key]
    else:
        return None
			
#search for a key in a json object recursivily
def search_key(data, key):
	if data is None:
		return None
	if key is None:
		return None
	if type(data) is dict:
		if key in data.keys():
			return data[key]
		else:
			for k in data.keys():
				return(search_key(data[k], key))
	else:
		return None

lld = obtain_data()

def format_data(lld):
	bdd = []
	for key in lld:
		for obj in lld[key]:
			json_obj = {}
			json_obj['data'] = {}
			json_obj['rna'] = extract_data(obj, 'numero_rna')
			json_obj['zip_code'] = extract_data(obj, 'zip_code')
			json_obj['data_type'] = extract_data(obj, 'contenu_request')
			json_obj['data']['name'] = extract_data(obj, 'title')
			json_obj['data']['update_date'] = extract_data(obj, 'update_at')
			json_obj['data']['type'] = key
			json_obj['data']['content'] = extract_data(obj, 'content')
			response = requests.get("https://www.data-asso.fr/gw/api-server/asso?id=" + extract_data(obj, 'numero_rna'))
			if response.status_code == 200:
				data = response.json()
				json_obj['data']['description'] = extract_data(extract_data(data, 'activites'), 'objet')
				if json_obj['data']['name'] is None:
					json_obj['data']['name'] = extract_data(data, 'title')
				if json_obj['zip_code'] is None:
					json_obj['zip_code'] = extract_data(extract_data(extract_data(data, 'coordonnees'), 'adresse_gestion'), 'cp')
				json_obj['tel'] = extract_data(extract_data(data, 'coordonnees'), 'telephone')
				json_obj['address'] = extract_data(extract_data(extract_data(data, 'coordonnees'), 'adresse_gestion'), 'raw')
			bdd.append(json_obj)
	return bdd

def export_bdd(bdd):
	with open('new_dataset.json', 'w') as outfile:
		json.dump(bdd, outfile)


bdd = format_data(lld)
export_bdd(bdd)