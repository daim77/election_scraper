import sys

import election_scraper_1996
import election_scrape_2002
import election_scraper_2006


def main(url, file_name):
    year = int(url.split('/')[4][2:].replace('nss', ''))

    if year <= 1998:
        election_scraper_1996.main(url, file_name)
    elif year == 2002:
        election_scrape_2002.main(url, file_name)
    else:
        election_scraper_2006.main(url, file_name)


if __name__ == '__main__':
    try:
        main(sys.argv[1], sys.argv[2])
    except IndexError:
        print('wrong arguments')
