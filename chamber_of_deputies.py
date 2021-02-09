import election_scraper_1996
import election_scrape_2002
import election_scraper_2006
import election_year


def chamber_of_deputies(url, file_name):
    year = election_year.election_year(url)

    if year <= 1998:
        election_scraper_1996.chamber_of_deputies()
    elif year == 2002:
        election_scrape_2002.chamber_of_deputies()
    else:
        election_scraper_2006.chamber_of_deputies()
