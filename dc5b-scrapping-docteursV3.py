import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# Créer une session requests et effectuer une première requête GET pour récupérer les cookies
session = requests.Session()
url = 'http://annuairesante.ameli.fr/'
response = session.get(url)
if response.status_code != 200:
    raise Exception("La requête GET n'a pas abouti")
print("Cookies récupérés")

# Récupérer les cookies de la session
cookies = session.cookies.get_dict()

# Définir les données à envoyer pour la recherche
data = {
    'ps_profession': '34',
    'ps_profession_label': 'Médecin généraliste',
    'ps_localisation': 'HERAULT (34)',
    'localisation_category': 'departements',
    'ps_proximite': 'on',
    'submit_final': 'Rechercher'
}

# Lancer une instance de Chrome avec Selenium et ouvrir l'URL de recherche
driver = webdriver.Chrome()
driver.get(url)

# Chercher le formulaire de recherche en utilisant BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')
form = soup.find('form', {'action': '/recherche.html'})
if not form:
    raise Exception("Le formulaire de recherche est introuvable")
response = session.post(url + form['action'], data=data, cookies=cookies)

# Remplir les données de recherche et cliquer sur le bouton "Rechercher"
input_element = driver.execute_script("document.getElementById('formProId').value = '34'; document.getElementById('formPro').title = 'Médecin généraliste'; document.getElementById('formOu').title = 'HERAULT (34)';")
button_element = driver.find_element(By.XPATH, '//input[@type="submit" and @value="Rechercher" and @title="Rechercher"]')
button_element.click()

# Attendre que la page de résultats soit chargée
time.sleep(5)

# Récupérer l'URL actuelle
current_url = driver.current_url
response = session.get(current_url)

# Parser le HTML de la réponse à l'aide de Beautiful Soup pour extraire les informations des médecins
soup = BeautifulSoup(response.text, 'html.parser')

# Extraire les informations des médecins
items = soup.find_all()

# Créer une liste pour stocker les informations des médecins
doctors_info = []

for item in items[:50]: 
    # Extraire le nom et prénom du médecin # ne récupérer que les 50 premiers éléments
    name_tag = item.find('div', {'class': 'nom_pictos'})
    if name_tag:
        full_name = name_tag.find('strong').string.strip()
        first_name, last_name = full_name.split(' ', 1)
    else:
        first_name, last_name = 'Nom', 'inconnu'
        
    # Extraire le numéro de téléphone du médecin
    tel_tag = item.find('div', {'class': 'elements'}).find('div', {'class': 'tel'})
    if tel_tag:
        tel = tel_tag.text.strip().replace('\xa0', '')
    else:
        tel = 'Numéro de téléphone inconnu'

    # Extraire l'adresse du médecin
    adresse_tag = item.find('div', {'class': 'elements'}).find('div', {'class': 'adresse'})
    if adresse_tag:
        adresse = adresse_tag.text.strip().replace('<br>', ', ')
    else:
        adresse = 'Adresse inconnue'

    # Stocker les informations dans un dictionnaire
    doctor_info = {
        'Prénom': first_name,
        'Nom': last_name,
        'Téléphone': tel,
        'Adresse': adresse
    }
    doctors_info.append(doctor_info)

# Créer un DataFrame pandas avec les informations des médecins et écrire le CSV
doctors_df = pd.DataFrame(doctors_info, columns=['Nom', 'Téléphone', 'Adresse'])
doctors_df.to_csv('medecins-generalistes-herault.csv', index=False, encoding='utf-8-sig')

# Fermer le driver Selenium
driver.quit()
