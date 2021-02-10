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
region,district,city_number,city_name,registered,envelope,valid,Občané,LIB,JežíšPán,VV,KONS,KSČM,"""KČ""",ČSNS,ČSSD,NP,SPR-RSČ,M,SPOZ,STOP,TOP 09,ES,KDU-ČSL,PB,ČSNS2005,SZ,Suveren.,HS,ČPS,DSSS,Svobodní,ODS,KH
 Plzeňský kraj, Plzeň-sever,566756,Bdeněves,475,310,308,0,0,0,29,0,40,0,0,41,0,0,0,17,0,62,0,7,0,0,4,21,0,1,9,1,76,0
 Plzeňský kraj, Plzeň-sever,558656,Bezvěrov,544,275,274,0,0,0,34,0,69,0,0,56,0,0,0,5,0,20,0,4,1,0,1,20,0,6,5,3,50,0
 Plzeňský kraj, Plzeň-sever,530239,Bílov,64,46,46,0,0,0,3,0,10,0,0,11,0,0,0,1,0,6,0,2,0,0,0,1,0,1,0,1,10,0
 Plzeňský kraj, Plzeň-sever,558672,Blatnice,615,342,341,0,0,0,47,0,49,0,0,94,0,0,0,11,1,40,0,5,2,1,1,8,0,8,6,3,65,0
 Plzeňský kraj, Plzeň-sever,566764,Blažim,46,31,31,0,0,0,2,0,8,0,0,11,0,0,0,1,0,0,0,0,0,0,0,2,0,1,0,0,6,0
```