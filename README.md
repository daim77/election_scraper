# election_scrapper
https://github.com/daim77/election_scraper.git

###DATA STRUCTURE
for one municipality - dict:
{region, district, city_number, city_name, links,
registered, envelopes, valid, *all_parties}

===========================================  
Elections to the Chamber of Deputies of the Parliament of the Czech Republic
1996 - 2007

Available for **CZ** and **EN** version

_EN version available from 2002_

===========================================

### Possibilities
1. one big script `election_scraper.py`  
   control function is `chamber_of_deputies()`
2. main script `chamber_of_deputies.py`  
   you can run this in terminal
   check example below
   
3. `election_scraper_2017`  
    ENGETO project  
   check requirements.md
   
### INSTALL

modules csv, os, string, requests and BeautifullSoup

### How to install BS4:
  https://pypi.org/project/bs4/

## clone repo from GitHub:

```
$ git clone git@github.com:daim77/election_scraper.git'
```

### prepare args:
  open https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ \
  for chosen district open ** X ** in "vyber obce"column\
  copy this link as *url arg*

### how to run 2nd possibility
open terminal
write:  
```
$ python chamber_of_deputies.py 'https://volby.cz/pls/ps2002/ps45?xjazyk=CZ&xkraj=5&xokres=4103', 'results_2002'
```

### result is available as results_2002.csv table in TABLE subfolder
```
city_number,city_name,registered,envelope,valid,ODS,ŘN - VU,CESTA,ČSSD,PB,RČ,STAN,KSČM,Zelení,Rozumní,SPDV,Svobodní,BPI,ODA,Piráti,OBČANÉ 2011,Unie H.A.V.E.L.,ČNF,Referendum o EU,TOP 09,ANO,DV 2016,SPRRSČ M.Sládka,KDU-ČSL,ČSNS,REAL,SPORTOVCI,DSSS,SPD,SPO,NáS
562726,Báňovice,90,71,71,9,0,0,2,0,0,1,0,0,1,0,0,0,0,4,0,0,0,0,5,11,0,0,33,0,0,0,0,5,0,0
562548,Bednárec,87,47,47,8,0,0,8,0,0,3,0,1,0,0,0,0,0,9,0,0,0,0,0,14,0,0,3,0,0,0,1,0,0,0
561053,Bednáreček,156,101,99,9,0,0,8,0,0,1,13,2,3,0,2,0,0,4,0,0,0,0,5,34,0,0,4,0,0,1,1,12,0,0
```