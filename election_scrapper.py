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

# data structure
# [city number, city name, link, registered, envelope, valid]

import csv
import requests
import bs4


def soup_boilling(url):
    html_data = requests.get(url)
    # print(html_data.text)
    soup = bs4.BeautifulSoup(html_data.text, "html.parser")
    return soup


def data_municipality_scrapper(links):
    data_municipality = []

    for item in links:
        if len(item[2]) < 80:
            print(item)
            ward_municipality_scrapper(item[2])
            continue

        sub_soup = soup_boilling(item[2])
        figures = [figure.text for figure in sub_soup.table.find_all('td')]

        item.append(figures[3])
        item.append(figures[4])
        item.append(figures[7])
        data_municipality.append(item)

    print(data_municipality)
        # for item in sub_soup:
        #     print(item)
        # exit()


# nektere obce maji okrsky...
def ward_municipality_scrapper(url):
    ward_soup = soup_boilling(url)
    ward_links = []
    for item in ward_soup.table.find_all('td'):
        try:
            ward_links.append(item.a.attrs['href'])
        except AttributeError:
            continue
    print(ward_links)
    # vytvorit linky
    # extrahovat total data a ty pak suma secist
    # vse vratit do data_municipality scrapper


def link_municipality_scrapper(soup, url):
    links = []
    sub_links = []
    for index, item in enumerate(soup.find_all('td')):
        if (index + 1) % 3 == 0:
            sub_links.append(item.a.attrs['href'])
            # print(item.a)
            links.append(sub_links)
            sub_links = []
            continue
        sub_links.append(item.text)

    url_part = url.split('/')[2:][:-1]
    for item in links:
        url = 'https://' + '/'.join(url_part) + '/' + item[2]
        item.pop()
        item.append(url)
    return links


# pojmenovani kraje a okresu
def region_name(soup):
    return [item.text.strip('\n') for item in soup.find_all('h3')]


# def csv_writer(region_name: str, data_villages: list, file_name: str):
#     with open(f'{file_name}.csv', 'w') as csv_file:
#         csv_writer = csv_writer(csv_file, delimiter=',')
#         csv_writer.writerows(data_villages)


def list_of_candidates():
    soup_candidates = \
        soup_boilling('https://volby.cz/pls/ps2017nss/ps82?xjazyk=CZ')
    print([item.text
           for index, item in enumerate(soup_candidates.table.find_all('td'))
           if (index + 1) % 3 == 0])


# main()
def scrap_elect(url, file_name):
    soup = soup_boilling(url)
    name = region_name(soup)
    # print(name)
    list_of_candidates = list_of_candidates()

    links = link_municipality_scrapper(soup, url)
    # print(links)

    data_municipality_scrapper(links)
    # csv_writer(name, data_villages, file_name)


if __name__ == '__main__':
    scrap_elect('https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2111', 'election_data')  # odkaz na seznam obci, nazev souboru
