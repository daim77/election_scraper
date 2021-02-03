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
import requests
import bs4


result_election_frame = {}
result_election = []
header_names = []


def election_year(url):
    year = int(url.split('/')[4][2:])
    return year


def soup_boiling(url):
    html_data = requests.get(url)
    soup = bs4.BeautifulSoup(html_data.text, "html.parser")
    return soup


# region name, district name
def region_name(soup, year):
    if year >= 2006:
        region = [
            item.text.strip('\n').split(':')[1]
            for item in soup.find_all('h3')
        ]
    elif year == 2002:
        region = [
            item.text.replace(' ', '').split(':')[1]
            for item in soup.find_all('b')
        ]
    else:
        region = [
            item.text.split(' ')[1]
            for item in soup.find_all('b')[1:]
        ]

    result_election_frame['region'] = region[0]
    result_election_frame['district'] = region[1]

    header_names.append('region')
    header_names.append('district')


def data_municipality_scrapper():

    for item in result_election:
        if len(item['links'][0]) < 80:
            ward_links = ward_link_scrapper(item['links'][0])
            item['links'] = ward_links
            # continue

        item['registered'] = 0
        item['envelope'] = 0
        item['valid'] = 0

        for link in item['links']:
            sub_soup = soup_boiling(link)

            figures = [
                figure.text.replace(' ', '')
                for figure in sub_soup.table.find_all('td')
            ]
            if len(figures) == 6:
                corr = 3
            else:
                corr = 0

            item['registered'] += int(figures[3 - corr])
            item['envelope'] += int(figures[4 - corr])
            item['valid'] += int(figures[7 - corr])

    header_names.insert(4, 'registered')
    header_names.insert(5, 'envelope')
    header_names.insert(6, 'valid')


# wards in some municipalities
def ward_link_scrapper(url_for_wards):
    ward_soup = soup_boiling(url_for_wards)
    url_part = url_for_wards.split('/')[2:][:-1]
    ward_links = []
    for item in ward_soup.table.find_all('td'):
        try:
            ward_links.append(
                'https://' + '/'.join(url_part) + '/' + item.a.attrs['href']
            )
        except AttributeError:
            continue
    return ward_links
    # extrahovat total data a ty pak suma secist
    # vse vratit do data_municipality scrapper


def link_municipality_scrapper(soup, url):
    sub_links = []
    links = []
    url_part = url.split('/')[2:][:-1]

    for index, item in enumerate(soup.find_all('td')):
        if (index + 1) % 3 == 0:
            try:
                sub_links.append(item.a.attrs['href'])
            except AttributeError:
                continue
            links.append(sub_links)
            sub_links = []
            continue

        sub_links.append(item.text)

    for index, item in enumerate(links):
        # result_election.append(result_election_frame)
        result_election.append({})
        result_election[index]['city_number'] = item[0]
        result_election[index]['city_name'] = item[1]

        url = 'https://' + '/'.join(url_part) + '/' + item[2]
        result_election[index]['links'] = [url]
        result_election[index].update(result_election_frame)

    header_names.insert(2, 'city_number')
    header_names.insert(3, 'city_name')


def list_of_candidates(url):
    url_part = url.split('/')[2:][:-1]

    soup_candidates = \
        soup_boiling(
            'https://' + '/'.join(url_part) + '/' + 'ps82?xjazyk=CZ'
        )

    parties = [item.text
               for index, item in
               enumerate(soup_candidates.table.find_all('td'))
               if (index + 1) % 3 == 0]

    for member in parties:
        result_election_frame[member] = 0
        header_names.append(member)


def csv_writer(file_name):
    file_name += '.csv'
    try:
        with open(file_name, mode='w', encoding='utf-8') as csv_file:

            writer = csv.DictWriter(
                csv_file,
                delimiter=',',
                fieldnames=header_names,
                extrasaction='ignore'
            )

            writer.writeheader()
            for row in result_election:
                writer.writerow(row)
    except IOError:
        print("I/O error")


# main()
def scrap_elect(url, file_name):
    year = election_year(url)
    soup = soup_boiling(url)
    region_name(soup, year)
    list_of_candidates(url)

    link_municipality_scrapper(soup, url)
    data_municipality_scrapper()

    csv_writer(file_name)


if __name__ == '__main__':
    scrap_elect(
        'https://volby.cz/pls/ps1996/u5311?xkraj=32&xokres=11',
        'election_data_2006'
    )
