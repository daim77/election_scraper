import csv
import requests
import os
import string
from bs4 import BeautifulSoup


result_election_frame = {}
result_election = []
header_names = []
translate = {}
translate_six = {}


def welcome_to_scraper():
    line = '*' * 100
    print()
    print(line)
    print('{:^100}'.format(
        'ELECTION SCRAPER - CHAMBER OF DEPUTIES of CZECH REPUBLIC'
    ))
    print('{:^100}'.format('1996 - 2017'))
    print(line)
    print('{:<100}'.format('More years available in czech version'))
    print('{:<100}'.format(
        '1. Open https://volby.cz/index_en.htm and select year'))
    print('{:<100}'.format(
        "2. Click on 'Results for territorial units'"))
    print('{:<100}'.format(
        "3. Click on 'X' in a column 'Choice of municipality'"))
    print('{:<100}'.format(
        '4. Copy this link'))
    print('{:<100}'.format(
        '5. Prepare file name for result saving in csv format'))
    print('{:<100}'.format(
        "6. Result is saved to folder >>tables<<"))
    print(line)

    url = input('Insert link: ')
    file_name = input('Insert file name: ')

    if url.startswith('www'):
        url = 'https:' + os.sep * 2 + url

    not_valid_char = string.punctuation.replace('-', '').replace('_', '')

    for char in not_valid_char:
        if char in file_name:
            print('Illegal characters in file name!')
            exit()
    if file_name == '':
        file_name = 'election'

    print(line)
    print('Loading data...')

    return url, file_name


def election_year(url):
    year = int(url.split('/')[4][2:].replace('nss', ''))
    return year


def soup_boiling(url):
    html_data = requests.get(url)
    soup = BeautifulSoup(html_data.text, "html.parser")
    return soup


# region name, district name
def region_name(soup, year):
    region = [
        item.text.strip('\n').split(':')[1:]
        for item in soup.find_all('h3')
    ]

    result_election_frame['region'] = region[0][0]

    if len(region) > 1:
        if len(region[1]) == 1:
            result_election_frame['district'] = region[1][0]
        else:
            result_election_frame['district'] = ' '.join(region[1])
    else:
        result_election_frame['district'] = region[0][0]

    header_names.append('region')
    header_names.append('district')


def list_of_candidates(url, year):
    global translate, translate_six

    if 'jazyk=EN' in url:
        mutation = 'EN'
    else:
        mutation = 'CZ'

    url_part = url.split('/')[2:][:-1]

    soup_candidates = soup_boiling(
        'https:' + '/' * 2
        + '/'.join(url_part) + '/'
        + 'ps82?xjazyk=' + mutation
    )

    parties = [
        item.text
        for item in
        soup_candidates.table.find_all('td', {'headers': 'sa1 sb2'})
    ]

    order = [str(num) for num in range(1, len(parties) + 1)]

    translate_six = dict(zip(order, parties))

    for member in parties:
        result_election_frame[member] = 0
        header_names.append(member)


def link_municipality_scraper(soup, url, year):
    sub_links = []
    links = []
    url_part = url.split('/')[2:][:-1]

    for index, item in enumerate(
            [field for field in soup.find_all('td') if field.text != '']):
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

        url = 'https:' + '/' + '/' \
              + '/'.join(url_part) \
              + '/' + item[2]

        result_election[index]['links'] = [url]
        result_election[index].update(result_election_frame)

    header_names.insert(2, 'city_number')
    header_names.insert(3, 'city_name')


def data_municipality_scraper(year):
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
                        item[translate_six[key]] += value
                    else:
                        continue

    header_names.insert(4, 'registered')
    header_names.insert(5, 'envelope')
    header_names.insert(6, 'valid')


def ward_link_scraper(url_for_wards):
    ward_soup = soup_boiling(url_for_wards)
    url_part = url_for_wards.split('/')[2:][:-1]
    ward_links = []

    for item in ward_soup.table.find_all('td'):
        try:
            ward_links.append(
                'https:' + '/' + '/'
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
            for row in result_election:
                writer.writerow(row)

            print('You are lucky! Data available here:')
            print('=' * 100)
            print(path + os.sep + file_name)
            print('=' * 100)
    except IOError:
        print("I/O error")
    return


def chamber_of_deputies():
    try:
        url, file_name = welcome_to_scraper()

        year = election_year(url)
        soup = soup_boiling(url)
        region_name(soup, year)
        list_of_candidates(url, year)
        link_municipality_scraper(soup, url, year)
        data_municipality_scraper(year)
        csv_writer(file_name)

    except (ValueError, IndexError, TypeError, AttributeError):
        print('Sorry - wrong link')


if __name__ == '__main__':
    chamber_of_deputies()
