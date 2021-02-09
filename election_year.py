def election_year(url):
    year = int(url.split('/')[4][2:].replace('nss', ''))
    return year
