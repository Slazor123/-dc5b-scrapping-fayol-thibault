import requests
from bs4 import BeautifulSoup

# URL
url = 'https://www.scrapethissite.com/pages/simple/'

# HTML
response = requests.get(url)

# BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Etape 1 les pays
countries = soup.find_all('div', {'class': 'country'})

# Pour chaque pays, récupération des informations nécessaires
for country in countries:
    name = country.find('h3').text.strip() if country.find('h3') is not None else ''
    population = country.find('span', {'class': 'country-population'}).text.strip() if country.find('span', {'class': 'country-population'}) is not None else ''
    capital = country.find('span', {'class': 'country-capital'}).text.strip() if country.find('span', {'class': 'country-capital'}) is not None else ''
    area = country.find('span', {'class': 'country-area'}).text.strip() if country.find('span', {'class': 'country-area'}) is not None else ''

    # Nettoyage des données
    population = population.replace(',', '') if ',' in population else population
    area = area.replace(' km²', '') if ' km²' in area else area

    # Affichage des informations
    print('Nom :', name)
    print('Population :', population)
    print('Capitale :', capital)
    print('Aire :', area + " km²")
    print('\n')
