import json
from sys import stderr
import requests
import smtplib, ssl

registered_data = {}

def import_new_data():
	with open('new_dataset.json') as f:
		data = json.load(f)
		for obj in data:
			register_data(obj)
	return

def add_to_incomplete_dataset(data):
	with open('data_to_complete.json', 'a+') as f:
		for obj in f:
			if data['rna'] in obj:
				return
		json.dump(data, f)

def register_data(data):
	zip_code = data['zip_code']
	if zip_code is None:
		add_to_incomplete_dataset(data)
		return
	zip_code = '0'*(5-len(zip_code)) + zip_code
	departement = zip_code[:2]
	if departement not in registered_data:
		registered_data[departement] = []
	url = "https://geo.api.gouv.fr/departements/" + departement
	response = requests.get(url)
	if response.status_code == 200:
		departement_name = str(response.json()['nom']).lower()
		mail = departement_name + "@sulinum.org"
	else:
		mail = "default@solinum.org"
	obj = {}
	obj['mail'] = mail
	obj['data'] = data
	registered_data[departement].append(obj)

def export_registered_data():
    with open('registered_data.json', 'w') as outfile:
        json.dump(registered_data, outfile)

def send_mail():
    port = 465
    smtp_server = "smtp.gmail.com"
    sender_email = "" #Gmail mail
    sender_password = "" #Gmail password (use an "application password")
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, sender_password)
        for departement in registered_data:
            message = "Here is your today's review !\n"
            for data in registered_data[departement]['data']:
                if data['data_type'] == "add":
                    message += "\nWe found a new association ! + " + data['data']['name'] + "\n\n"
                    message += json.dumps(data['data']) + "\n"
                elif data['data_type'] == "update":
                    message += "\nWe found an update for " + data['original_obj']['name'] + "!\n"
                    if "address" in data:
                        message += "- New address: " + data['address'] + "\n"
                    if "phone" in data:
                        message += "- New phone: " + data['phone'] + "\n"
                    if "email" in data:
                        message += "- New email: " + data['email'] + "\n"
                    message += "\nOriginal data was: " + json.dumps(data['original_obj']) + "\n"
            subject = "You have a review !"
            receiver_email = registered_data[departement]['mail']
            body = "Subject: {}\n\n{}".format(subject, message)
            server.sendmail(sender_email, receiver_email, body)

def clean_data():
    registered_data = {}


import_new_data()
export_registered_data()
#send_mail()
clean_data()