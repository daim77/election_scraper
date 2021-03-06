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
        item.text.split(' ')[1:]
        for item in soup.find_all('b')[1:]
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

    url_part = url.split('/')[2:][:-1]

    soup_candidates = soup_boiling(
        'https:' + '/' * 2
        + '/'.join(url_part) + '/'
        + 'u32?xpl=0&xtr=2'
    )

    parties = [str(100 + int(index / 12))[1:] + ':' + item.text
               for index, item in
               enumerate(soup_candidates.table.find_all('td'))
               if index % 12 == 0][1:]

    order = [str(number + 100)[1:]
             for number in range(1, len(parties) + 1)]

    translate = dict(zip(order, parties))

    for member in parties:
        result_election_frame[member] = 0
        header_names.append(member)


def link_municipality_scraper(soup, url):
    sub_links = []
    links = []
    url_part = url.split('/')[2:][:-1]

    for index, item in enumerate(
            [field for field in soup.find_all('td') if field.text != '']):
        if (index + 1) % 4 == 0:
            try:
                sub_links.append(
                    item.a.attrs['href'][:5]
                    + '2'
                    + item.a.attrs['href'][6:]
                )
            except AttributeError:
                continue
            sub_links.remove(' X ')
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
        sub_soup = soup_boiling(item['links'][0])
        figures = [
            figure.text.replace(' ', '')
            for figure in sub_soup.find_all('td')
            if figure.text != ''
        ]

        item['registered'] = int(figures[3].replace(' ', ''))
        item['envelope'] = int(figures[4].replace(' ', ''))
        item['valid'] = int(figures[7].replace(' ', ''))

        figures = figures[9:]
        for index, item_ in enumerate(figures):
            if (index + 1) % 4 == 0:
                value = figures[index - 1]
                key = figures[index - 3]
                item[translate[key]] += int(value)

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
        'https://volby.cz/pls/ps1996/u5311?xkraj=32&xokres=4',
        'vysledky_96'
    )
