import csv
import requests
import os

from bs4 import BeautifulSoup


result_election_frame = {}
result_election = []
header_names = []
translate = {}


def soup_boiling(url):
    return BeautifulSoup(requests.get(url).text, "html.parser")


def list_of_candidates(url):
    global translate

    url_part = url.split('/')[2:][:-1]

    soup_candidates = soup_boiling(
        'https:' + '/' * 2
        + '/'.join(url_part) + '/'
        + 'ps82?xjazyk=CZ'
    )

    parties = [
        item.text
        for item in
        soup_candidates.find_all('td', {'headers': 'sa1 sb2'})
    ]

    translate = {str(index): value for index, value in enumerate(parties, 1)}

    for member in parties:
        result_election_frame[member] = 0
        header_names.append(member)


def link_municipality_scraper(soup, url):
    sub_links = []
    links = []
    url_part = url.split('/')[2:][:-1]

    for index, item in enumerate(
            [
                field for field in soup.find_all('td') if field.text != ''
            ]
    ):
        if (index + 1) % 3 == 0:
            try:
                sub_links.append(item.a.attrs['href'])
            except AttributeError:
                continue
            links.append(sub_links)
            sub_links = []
            continue
        sub_links.append(item.text)

    id_municipality_scraper(links, url_part)


def id_municipality_scraper(links, url_part):

    for index, item in enumerate(links):
        result_election.append({})
        result_election[index]['city_number'] = item[0]
        result_election[index]['city_name'] = item[1]

        url = 'https:' \
              + '/' \
              + '/' \
              + '/'.join(url_part) \
              + '/' + item[2]

        result_election[index]['links'] = [url]
        result_election[index].update(result_election_frame)

    header_names.insert(0, 'city_number')
    header_names.insert(1, 'city_name')


def data_municipality_scraper():

    for item in result_election:
        if '&xvyber=' not in item['links'][0]:
            ward_links = ward_link_scraper(item['links'][0])
            item['links'] = ward_links

        item['registered'] = 0
        item['envelope'] = 0
        item['valid'] = 0

        for link in item['links']:
            sub_soup = soup_boiling(link)

            figures = [
                figure.text.replace(' ', '')
                for figure in sub_soup.find_all('td')
                if figure.text != ''
            ]

            if '&xokrsek=' in link:
                corr = 3
            else:
                corr = 0

            item['registered'] += int(figures[3 - corr].replace(' ', ''))
            item['envelope'] += int(figures[4 - corr].replace(' ', ''))
            item['valid'] += int(figures[7 - corr].replace(' ', ''))

            if '&xokrsek=' in link:
                figures = figures[6:]
            else:
                figures = figures[9:]

            for index, item_ in enumerate(figures):
                if (index + 1) % 5 == 0:
                    if figures[index - 2].replace(' ', '').isnumeric():
                        value = int(figures[index - 2].replace(' ', ''))
                        key = figures[index - 4]
                        item[translate[key]] += value
                    else:
                        continue

    header_names.insert(2, 'registered')
    header_names.insert(3, 'envelope')
    header_names.insert(4, 'valid')


def ward_link_scraper(url_for_wards):
    ward_soup = soup_boiling(url_for_wards)
    url_part = url_for_wards.split('/')[2:][:-1]
    ward_links = []

    for item in ward_soup.find_all('td'):
        try:
            ward_links.append(
                'https:'
                + '/'
                + '/'
                + '/'.join(url_part)
                + '/' + item.a.attrs['href']
            )
        except AttributeError:
            continue
    return ward_links


def csv_writer(file_name):
    if len(result_election) == 0:
        raise Exception('Wrong link!')

    path = os.getcwd() + os.sep + 'tables'

    if not os.path.exists(path):
        os.mkdir(path)

    file_name += '.csv'

    try:
        with open(path + os.sep + file_name, mode='w', encoding='utf-8') \
                as csv_file:

            writer = csv.DictWriter(
                csv_file,
                delimiter=',',
                fieldnames=header_names,
                extrasaction='ignore'
            )

            writer.writeheader()
            writer.writerows(result_election)

            print('You are lucky! Data available here:')
            print('=' * 100)
            print(path + os.sep + file_name)
            print('=' * 100)
    except IOError:
        print("I/O error")


def chamber_of_deputies(url, file_name):
    try:
        soup = soup_boiling(url)
        list_of_candidates(url)
        link_municipality_scraper(soup, url)
        data_municipality_scraper()
        csv_writer(file_name)

    except (ValueError, IndexError, TypeError, AttributeError):
        print('Sorry - wrong link')


if __name__ == '__main__':
    chamber_of_deputies(
        'https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=3&xnumnuts=3103',
        'vysledek'
    )
