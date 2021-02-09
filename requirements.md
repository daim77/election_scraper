# ELECTION SCRAPER - CHAMBER OF DEPUTIES of CZECH REPUBLIC

## moduls:
  - CSV
  - REQUESTS
  - OS
  - BeautifullSoup (BS4)

## How to install BS4:
  https://pypi.org/project/bs4/

## clone repo from GitHub:

```
$ git clone git@github.com:daim77/election_scraper.git'
```

## prepare args:
  open https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ \
  for chosen district open ** X ** in "vyber obce"column \
  copy this link as *url arg*

## run script:
  arg1 = url\
  arg2 = file name \

  **election_scraper_2017(url, file_name)**

## result in file_name.csv in "table" subfolder:

```
city_number,city_name,registered,envelope,valid,ODS,ŘN - VU,CESTA,ČSSD,PB,RČ,STAN,KSČM,Zelení,Rozumní,SPDV,Svobodní,BPI,ODA,Piráti,OBČANÉ 2011,Unie H.A.V.E.L.,ČNF,Referendum o EU,TOP 09,ANO,DV 2016,SPRRSČ M.Sládka,KDU-ČSL,ČSNS,REAL,SPORTOVCI,DSSS,SPD,SPO,NáS
562726,Báňovice,90,71,71,9,0,0,2,0,0,1,0,0,1,0,0,0,0,4,0,0,0,0,5,11,0,0,33,0,0,0,0,5,0,0
562548,Bednárec,87,47,47,8,0,0,8,0,0,3,0,1,0,0,0,0,0,9,0,0,0,0,0,14,0,0,3,0,0,0,1,0,0,0
561053,Bednáreček,156,101,99,9,0,0,8,0,0,1,13,2,3,0,2,0,0,4,0,0,0,0,5,34,0,0,4,0,0,1,1,12,0,0
```
