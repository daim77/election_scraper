import csv
import requests
import os

from bs4 import BeautifulSoup


result_election_frame = {}
result_election = []
header_names = []
translate = {}



def soup_boiling(url):
    html_data = requests.get(url)
    soup = BeautifulSoup(html_data.text, "html.parser")
    return soup


# region name, district name
def region_name(soup):

    region = [
        item.text.replace(' ', '').split(':')[1:]
        for item in soup.find_all('b')
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


def list_of_candidates(url):
    global translate

    if 'jazyk=EN' in url:
        mutation = 'EN'
    else:
        mutation = 'CZ'

    url_part = url.split('/')[2:][:-1]

    soup_candidates = soup_boiling(
        'https:' + '/' * 2
        + '/'.join(url_part) + '/'
        + 'ps72?xjazyk=' + mutation
    )
    parties = [item.text
               for index, item in
               enumerate(soup_candidates.table.find_all('th')[15:])
               if (index + 1) % 2 == 0]

    for member in parties:
        result_election_frame[member] = 0
        header_names.append(member)


def link_municipality_scraper(soup, url):
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


def data_municipality_scraper():

    for item in result_election:
        if '&xokrsek=' not in item['links'][0]:
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

            item['registered'] += int(figures[3].replace(' ', ''))
            item['envelope'] += int(figures[4].replace(' ', ''))
            item['valid'] += int(figures[7].replace(' ', ''))

            figures = figures[9:]
            for index, item_ in enumerate(figures):
                if (index + 1) % 4 == 0:
                    value = int(figures[index - 1].replace(' ', ''))
                    key = figures[index - 2]
                    item[key] += value

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


def main(url, file_name):
    try:
        soup = soup_boiling(url)
        region_name(soup)
        list_of_candidates(url)
        link_municipality_scraper(soup, url)
        data_municipality_scraper()
        csv_writer(file_name)

    except (ValueError, IndexError, TypeError, AttributeError):
        print('Sorry - wrong link')


if __name__ == '__main__':
    main(
        'https://volby.cz/pls/ps2002/ps45?xjazyk=CZ&xkraj=5&xokres=4103',
        'vysledky_2002'
    )
