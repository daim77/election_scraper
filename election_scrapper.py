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
            print('link is not complete', item)
            continue
        sub_soup = soup_boilling(item[2])
        figures = [figure.text for figure in sub_soup.table.find_all('td')]
        item.append([figures[3], figures[4], figures[7]])
        data_municipality.append(item)
    print(data_municipality)
        # for item in sub_soup:
        #     print(item)
        # exit()




# def ward_municipality_scrapper


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


def region_name(soup):
    return [item.text.strip('\n') for item in soup.find_all('h3')]


# def csv_writer(region_name: str, data_villages: list, file_name: str):
#     with open(f'{file_name}.csv', 'w') as csv_file:
#         csv_writer = csv_writer(csv_file, delimiter=',')
#         csv_writer.writerows(data_villages)


def scrap_elect(url, file_name):
    soup = soup_boilling(url)
    name = region_name(soup)
    # print(name)

    links = link_municipality_scrapper(soup, url)
    # print(links)

    data_municipality_scrapper(links)
    # csv_writer(name, data_villages, file_name)


if __name__ == '__main__':
    scrap_elect('https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2111', 'election_data')  # odkaz na seznam obci, nazev souboru
