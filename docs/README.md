# webscraper-python
Webscraper for pdf-data extraction from swgdrugs.com

## Python version: 3.12 

## How to use: 

### Get data from website:
1. execute "cli_interface.py"
2. input "collect" 
3. wait until finished 
4. open "data"-folder 
5. open "output"-folder
6. get "data.json"

### Search in search engine:
0. (put custom .json-file in "data/input"-folder) //// NOT WORKING
1. execute "gui_search_engine.py"
2. type parameter in input-fields 
3. click "search"-button

## Installation: 

### required libraries:

#### Preinstalled:
- logging
- datetime
- os 
- json 
- cmd
- sys


#### required to install
- requests 
- bs4
- urllib3
- PyPDF2
- pdfminer.six 
- pyqt6


## Aufteilung: 
- PDF in json (Teil 1) (Nathaniel)
- Json prüfen der Daten (Teil 2: validation) (Tatiana)
- Regelmäßig (Teil 3: Website Neuerungen überprüfen) (Nathaniel)
- Logging (Nathaniel)
- GUI / Suchmaschine (Teil 4) CLI und GUI (Tatiana)
- Import aus anderen Gruppen