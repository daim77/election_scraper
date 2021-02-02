# https://github.com/daim77/election_scrapper.git
# Elections to the Chamber of Deputies of the Parliament of the Czech Republic
# held on 20 – 21 October 2017

# Uživatelské vstupy
# Skript očekává dva vstupy: odkaz na seznam obcí daného okresu a název csv
# souboru bez přípony .csv.

# Výstup
# Hlavička csv souboru má mít podobu: kód obce, název obce, voliči v seznamu,
# vydané obálky, platné hlasy, kandidující strany.
# Každý řádek csv souboru potom bude speciální pro každou obec.

# data structure for one municipality:
# region, district, city_number, city_name, links,
# registered, envelopes, valid, all_parties

import csv
from pprint import pprint as pp
import requests
import bs4


result_election_frame = {}
result_election = []


def soup_boilling(url):
    html_data = requests.get(url)
    soup = bs4.BeautifulSoup(html_data.text, "html.parser")
    return soup


def data_municipality_scrapper():

    for item in result_election:
        if len(item['links'][0]) < 80:
            ward_municipality_scrapper(item['links'][0])
            continue

        sub_soup = soup_boilling(item['links'][0])
        figures = [figure.text for figure in sub_soup.table.find_all('td')]

        item['registered'] = figures[3]
        item['envelope'] = figures[4]
        item['valid'] = figures[7]


# wards in some municipalities
def ward_municipality_scrapper(url_for_wards):
    ward_soup = soup_boilling(url_for_wards)
    ward_links = []
    for item in ward_soup.table.find_all('td'):
        try:
            ward_links.append(item.a.attrs['href'])
        except AttributeError:
            continue
    # print(ward_links)
    # vytvorit linky
    # extrahovat total data a ty pak suma secist
    # vse vratit do data_municipality scrapper


def link_municipality_scrapper(soup, url):
    sub_links = []
    links = []
    url_part = url.split('/')[2:][:-1]

    for index, item in enumerate(soup.find_all('td')):
        if (index + 1) % 3 == 0:
            sub_links.append(item.a.attrs['href'])
            links.append(sub_links)
            sub_links = []
            continue
        sub_links.append(item.text)

    for item in links:

        result_election_frame['city_number'] = item[0]
        result_election_frame['city_name'] = item[1]

        url = 'https://' + '/'.join(url_part) + '/' + item[2]
        result_election_frame['links'] = [url]

        result_election.append(result_election_frame)


# region name, district name
def region_name(soup):
    region = [
        item.text.strip('\n').split(':')[1]
        for item in soup.find_all('h3')
    ]
    result_election_frame['region'] = region[0]
    result_election_frame['district'] = region[1]


# def csv_writer(data_villages: dict, file_name: str):
#     with open(f'{file_name}.csv', 'w') as csv_file:
#         csv_writer = csv_writer(csv_file, delimiter=',')
#         csv_writer.writerows(data_villages)


def list_of_candidates():
    soup_candidates = \
        soup_boilling('https://volby.cz/pls/ps2017nss/ps82?xjazyk=CZ')

    parties = [item.text
               for index, item in
               enumerate(soup_candidates.table.find_all('td'))
               if (index + 1) % 3 == 0]

    for member in parties:
        result_election_frame[member] = 0


# main()
def scrap_elect(url, file_name):
    soup = soup_boilling(url)
    region_name(soup)
    list_of_candidates()
    link_municipality_scrapper(soup, url)
    data_municipality_scrapper()

    pp(result_election)
    exit()

    # csv_writer(data_villages, file_name)


if __name__ == '__main__':
    scrap_elect('https://www.volby.cz/pls/ps2017nss/'
                'ps32?xjazyk=CZ&xkraj=2&xnumnuts=2111',
                'election_data')
