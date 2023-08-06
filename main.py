import requests
from bs4 import BeautifulSoup as bs
from datetime import datetime

URL_OLX = "https://www.olx.pl/praca/informatyka/warszawa/"
URL_PRACUJ = "https://www.pracuj.pl/praca/data;kw/warszawa;wp/it%20-%20rozw%C3%B3j%20oprogramowania;cc,5016?rd=30&et=1%2C17"


dtime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

def get_data_olx(url, datetime):
    base_url = "https://www.olx.pl"
    response = requests.get(url)
    soup = bs(response.text, 'html.parser')

    container_div = soup.find('div', attrs={'data-testid': 'listing-grid'})
    links = container_div.find_all("a")

    titles = [title.string for title in soup.find_all("h6")]
    hrefs = []

    for i in range(len(links)):
        if(links[i]['href'].startswith('/oferta')):
            hrefs.append(base_url + links[i]['href'])

    if (len(titles) == len(hrefs)):
        with open("olx_oferty.txt", "a") as f:
            f.write(datetime + '\n\n')
            for title, href in zip(titles, hrefs):
                f.write(title + '\n' + href + '\n\n')

def get_data_pracuj(url, datetime):
    response = requests.get(url)
    soup = bs(response.text, 'html.parser')

    container_div = soup.find('div', attrs={'data-test': 'section-offers'})
    offers = container_div.find_all("h2", attrs={'data-test': 'offer-title'})

    titles = []
    hrefs = []

    for offer in offers:
        elem = offer.find("a")
        titles.append(elem.string)
        hrefs.append(elem['href'])

    with open("pracuj_oferty.txt", "a") as f:
        f.write(datetime + '\n\n')
        for title, href in zip(titles, hrefs):
            f.write(title + '\n' + href + '\n\n')

get_data_olx(URL_OLX, dtime)
get_data_pracuj(URL_PRACUJ, dtime)