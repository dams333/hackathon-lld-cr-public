
import requests
from datetime import datetime

now = datetime.now()

SEC_IN_WEEK = 604800

def extract_data(data, key):
	if data is None:
		return None
	if key in data:
		return data[key]
	else:
		return None

def update_from(timestamp):
	time = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ')
	return (now - time).total_seconds()

# Adresse API : https://journal-officiel-datadila.opendatasoft.com/explore/dataset/jo_associations/api/

def deepSearchZIP(content):
	if content is None:
		return None
	zip = "codePostal"
	if zip in content:
		beg = content.find(zip) + len(zip) + 4
		end = beg + 5
		return(str(content[beg:end]))

def get_joaf_asso(category, rows):
	url = "https://journal-officiel-datadila.opendatasoft.com/api/records/1.0/search/?dataset=jo_associations&facet=domaine_activite_categorise&facet=domaine_activite_libelle_categorise&refine.domaine_activite_libelle_categorise=" + category + "&sort=dateparution&rows=" + str(rows)
	response = requests.get(url)
	data = response.json()
	found = []
	obj = {}
	for info in data['records']:
		obj = {}
		obj["numero_rna"] = extract_data(info['fields'], 'numero_rna')
		obj['title'] = extract_data(info['fields'], 'titre')
		obj['update_at'] = extract_data(info, 'record_timestamp')
		obj['update_from'] = update_from(obj['update_at'])
		obj["contenu_request"] = "remove" if extract_data(info['fields'], 'internal_contenu_subnode') else "add"
		obj["zip_code"] = extract_data(info['fields'], 'dca_codepostal')
		obj["content"] = extract_data(info['fields'], 'contenu')
		if obj['zip_code'] is None:
			obj['zip_code'] = deepSearchZIP(obj['content'])
			# print(obj['zip_code'])
		if obj['update_from'] > SEC_IN_WEEK:
			return found
		elif obj['numero_rna'] is not None and obj['contenu_request'] != "modification":
			# print(obj)
			found.append(obj)
	if obj['update_from'] > SEC_IN_WEEK:
		return found
	else:
		return get_joaf_asso(category, rows + 100)

def aff_bdd(category):
	for key in category:
		print("\n=== ", key, ": ", len(category[key]), " ===\n")
		# for obj in category[key]:
		# 	print(obj['content'])


def	obtain_data():
	category = {}
	category['Caritative_humanitaire_sociale'] = get_joaf_asso("associations+caritatives%2C+humanitaires%2C+aide+au+d%C3%A9veloppement%2C+d%C3%A9veloppement+du+b%C3%A9n%C3%A9volat", 100)
	category['Entraide'] = get_joaf_asso("amicales%2C+groupements+affinitaires%2C+groupements+d%27entraide+(hors+défense+de+droits+fondamentaux", 100)
	category['Emploi_solidarite'] = get_joaf_asso("aide+à+l%27emploi%2C+développement+local%2C+promotion+de+solidarités+économiques%2C+vie+locale", 100)
	category['Medico_sociaux'] = get_joaf_asso("services+et+établissements+médico-sociaux", 100)
	category['Sante'] = get_joaf_asso("santé", 100)
	category['Droits'] = get_joaf_asso("défense+de+droits+fondamentaux%2C+activités+civiques", 100)
	# aff_bdd(category)
	return category

#aff_bdd(obtain_data())