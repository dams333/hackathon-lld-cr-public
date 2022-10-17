# import libraries
from bs4 import BeautifulSoup
import urllib.request
import csv

# Find the contact page in specific website
# return link to contact page
def find_contact_page(url):
    # query the website and return the html to the variable 'page'
    page = urllib.request.urlopen(url)
    # parse the html using beautiful soup and store in variable 'soup'
    soup = BeautifulSoup(page, 'html.parser')
    # Find all links in the page
    links = soup.find_all('a') + soup.find_all('li') + soup.find_all('div') + soup.find_all('span') + soup.find_all('tr') + soup.find_all('p')
    # Find the link that contains "contact" and print it
    for link in links:
        if "contact" in link.text.lower() or "contacts" in link.get('href', '').lower():
            return url + link.get('href')
    return None

# Find the opening times in specific url
# return text with schedule or none if not found 
def goto_schedule(url):
    url_contact = find_contact_page(url)
    if url_contact is None:
        return None
    # query the website and return the html to the variable 'page'
    page = urllib.request.urlopen(url_contact)
    # parse the html using beautiful soup and store in variable 'soup'
    soup = BeautifulSoup(page, 'html.parser')
    # Find all links in the page
    links = soup.find_all('tr') + soup.find_all('p') + soup.find_all('li') + soup.find_all('div') + soup.find_all('span')
    # Find the link that contains "contact" and print it
    for link in links:
        open = ["horaires", "ouverture", "fermeture", "fermé",
                "ouvertures", "fermetures", "heure", "permanences"]
        for match in open:
            if match in link.text.lower():
                return link.text
    return None

urlpage = []
urlpage.append("https://cantal.cidff.info/")
urlpage.append("https://www.armeedusalut.fr")
urlpage.append("https://soliguide.fr")
urlpage.append("https://www.croix-rouge.fr")
for url in urlpage:
    print(goto_schedule(url))