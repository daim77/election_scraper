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


def soup_boilling(href_link):
    html_data = requests.get(href_link)
    print(html_data.text)
    soup = bs4.BeautifulSoup(html_data.text, "html.parser")
    return soup


# def district_scrapper(href_district):
#
#
# def village_scrapper(href_village):
#
#
#
# def csv_writer(dictrict_name: str, data_villages: list, file_name: str):
#     with open(f'{file_name}.csv', 'w') as csv_file:
#         csv_writer = csv_writer(csv_file, delimiter=',')
#         csv_writer.writerows(data_villages)


def scrap_elect(href_link, file_name):
    soup_boilling(href_link)



if __name__ == '__main__':
    scrap_elect('https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ', 'election_data')  # odkaz na seznam obci, nazev souboru
