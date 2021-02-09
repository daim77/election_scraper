import election_scraper_1996
import election_scrape_2002
import election_scraper_2006
import election_year


def chamber_of_deputies(url, file_name):
    year = election_year.election_year(url)

    if year <= 1998:
        election_scraper_1996.chamber_of_deputies(url, file_name)
    elif year == 2002:
        election_scrape_2002.chamber_of_deputies(url, file_name)
    else:
        election_scraper_2006.chamber_of_deputies(url, file_name)


if __name__ == '__main__':
    chamber_of_deputies(
        'https://volby.cz/pls/ps2002/ps45?xjazyk=CZ&xkraj=2&xokres=2101',
        'vysledky'
    )