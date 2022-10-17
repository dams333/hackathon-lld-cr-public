import json
import urllib.parse
import requests
import time
from datetime import datetime

def extract_data(data, key):
    if data is None:
        return None
    if key in data:
        return data[key]
    else:
        return None

def soliguide_to_rna(soliguide_obj):
    name = soliguide_obj['name']
    zip_code = soliguide_obj['position']['codePostal']
    url = "https://www.data-asso.fr/gw/api-server/associations/search?q=" + urllib.parse.quote(name)
    response = requests.get(url)
    data = response.json()
    found = []
    for association in data:
        identite = extract_data(association, 'identite')
        if str(extract_data(identite, 'sigle')).lower() == name.lower() or str(extract_data(identite, 'name')).lower() == name.lower():
            coordonate = extract_data(association, 'coordonnees')
            if str(extract_data(extract_data(coordonate, "adresse_siege"), "code_postal")) == zip_code:
                found.append(association)
    return found

def rna_to_soliguide_adress(rna_adress, zip_code):
    rna_adress = rna_adress.replace("_ ", "")
    split = rna_adress.split(zip_code)
    return split[0][:-1] + ", " + zip_code + split[1]

def is_rna_updated(rna, soliguide_obj):
    soliguide_update = datetime.strptime(extract_data(soliguide_obj, "updatedAt"), '%Y-%m-%dT%H:%M:%S.%fZ')
    url = "https://entreprise.data.gouv.fr/api/rna/v1/id/" + rna
    response = requests.get(url)
    data = response.json()
    assocaition = extract_data(data, 'association')
    if assocaition is None:
        return False
    rna_update = datetime.strptime(extract_data(assocaition, "updated_at"), '%Y-%m-%dT%H:%M:%S.%fZ')
    return rna_update > soliguide_update

def get_rna_updated(rna, original_obj):
    modif = {}
    url = "https://www.data-asso.fr/gw/api-server/asso?id=" + rna
    response = requests.get(url)
    data = response.json()
    
    #Test if adress changed
    address = extract_data(extract_data(data, 'coordonnees'), 'adresse_siege')
    rna_address_1 = extract_data(address, 'raw')
    rna_address_1 = rna_to_soliguide_adress(rna_address_1, extract_data(address, 'cp'))
    rna_address_2 = extract_data(extract_data(address, 'geo'), 'raw')
    rna_address_2 = rna_to_soliguide_adress(rna_address_2, extract_data(address, 'cp'))
    soliguide_address = extract_data(extract_data(original_obj, "position"), 'adresse')
    if soliguide_address != rna_address_1 and soliguide_address != rna_address_2:
        modif['address'] = rna_address_1

    #Test if email changed
    rna_email = extract_data(extract_data(data, 'coordonnees'), 'courriel')
    soliguide_email = extract_data(extract_data(original_obj, 'entity'), 'mail')
    if soliguide_email != rna_email:
        modif['email'] = rna_email
        
    #Test if phone changed
    rna_phone = extract_data(extract_data(data, 'coordonnees'), 'telephone')
    soliguide_phones = extract_data(extract_data(original_obj, 'entity'), 'phones')
    soliguide_repaired_phones = [str(extract_data(phone, "phoneNumber")).replace(" ", "") for phone in soliguide_phones]
    if rna_phone not in soliguide_repaired_phones:
        modif['phone'] = ' '.join(rna_phone[i:i+2] for i in range(0, len(rna_phone), 2))


    #Set update date
    url = "https://entreprise.data.gouv.fr/api/rna/v1/id/" + rna
    response = requests.get(url)
    data = response.json()
    if is_rna_updated(rna, original_obj):
        modif['update_time'] = extract_data(extract_data(data, "association"), 'updated_at')
    if "update_time" not in modif and len(modif) > 0:
        modif['update_time'] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    if len(modif) > 0:
        modif['rna'] = rna
        modif['zip_code'] = extract_data(address, 'cp')
        modif['data_type'] = 'update'
        modif['original_obj'] = original_obj
    return modif


# get soliguide data
with open('soliguide_obj.json') as f:
    soliguide_data = json.load(f)

associations = soliguide_to_rna(soliguide_data)
print("Found " + str(len(associations)) + " associations")
for association in associations:
    rna = extract_data(association, 'rna')
    print("Found association with RNA: " + rna)
    update = get_rna_updated(rna, soliguide_data)
    if len(update) > 0:
        print("Update needed")
        print(json.dumps(update))
    time.sleep(0.2)