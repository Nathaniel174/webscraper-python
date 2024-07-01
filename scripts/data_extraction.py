import json
import os
from datetime import datetime
from pdfminer.high_level import extract_pages, extract_text
import logging

# Setup logging:
logger = logging.getLogger("extraction_logger")
hdlr = logging.FileHandler(os.path.join("logging", "extraction.log"))
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)

# Init json file path and path for pdf_folder with existing pdfs:
json_file_path = os.path.join("data", "output", "data.json")
pdf_folder_path = os.path.join("data", "pdf-files")
source_website = "swgdrugs"

# Ensure PDF folder exists
if not os.path.exists(pdf_folder_path):
    logger.error(f"PDF folder does not exist: {pdf_folder_path}")
    raise FileNotFoundError(f"PDF folder does not exist: {pdf_folder_path}")

# Array with paths in string type 
pdf_file_paths = []

# Array with existing data
already_existing_pdfs = []

# get all existing pdf file names from pdf_folder
def get_all_pdf_names() -> None:
    logger.info("Get all pdf names from pdf-folder")

    # load content
    with open(json_file_path, "r") as js:
        content = json.load(js)

    for chemical in content:
        already_existing_pdfs.append(chemical.get("source")[1].split("/")[-1])

    for file in os.listdir(pdf_folder_path):
        if file.lower().endswith('.pdf'):
            if file not in already_existing_pdfs:
                pdf_file_paths.append(os.path.join(pdf_folder_path, file))

    logger.info("Get all pdf names READY")

# create dictionary for inserting data into json-file 
def assign_var_to_dict(pdf: str) -> dict:
    pdf_text = pdf_to_string(pdf)
    # initialise dictionary with found information 
    return_dict = {"version": get_version(),
                   "smiles": get_smiles(),
                   "names": get_names(pdf_text),
                   "iupac_names": get_iupac(pdf_text),
                   "formula": get_formula(pdf_text),
                   "inchi": get_inchi(),
                   "inchi_key": get_inchi_key(),
                   "molecular_mass": get_molecular_mass(pdf_text),
                   "cas_num": get_cas_num(pdf_text),
                   "categories": get_categories(),
                   "source": get_source(pdf),
                   "validated": get_validation(),
                   "deleted": get_deleted_status(),
                   "last_modified": get_last_modified(),
                   "details": {}
                   }

    return return_dict

# extract data from pdf to string 
def pdf_to_string(pdf):
    # read PDF into text as string
    text = extract_text(pdf)
    if 'cid:0' in text:
        text = text.replace('(cid:0)', '')
    splitted_text = text.split('\n')
    counter_blank = 0
    counter_space = 0

    # count spaces and blanks
    for i in range(len(splitted_text)):
        if splitted_text[i] == '':
            counter_blank += 1     
        elif splitted_text[i] == ' ':
            counter_space += 1

    # remove spaces and blanks
    for i in range(counter_blank):
        splitted_text.remove('')
    for i in range(counter_space):
        splitted_text.remove(' ')
    
    return splitted_text
                               
# ------ get functions ------  
def get_version() -> str:
    # Not in document
    return ""

def get_smiles() -> str:
    return ""

def get_names(splitted_text: list) -> list:
    # Erstes Element ist immer der Name als Überschrift
    names = []
    bad_synonyms = ["uvmax", "n/a", "cfr", "available"]

    # Get first name in heading
    # filter for strings found in beginning
    for i in range(3):
        if 'drug' not in splitted_text[i].lower():
            if 'this' not in splitted_text[i].lower():
                names.append(splitted_text[i].replace(" ", ""))
                break

    if 'latest' in names[0].lower():
        string_parts = names[0].lower().split('latest')
        string_parts.pop(1)
        string_in_char_list = []
        for char in string_parts[0]:
            string_in_char_list.append(char)
            
        for i in range(len(string_in_char_list),0,-1):
            if string_in_char_list[i-1] == ' ':
                string_in_char_list.pop(i-1)
            else:
                break
        
        name_length = len(string_in_char_list)
        
        string_in_char_list = []
        for i in range(0,name_length):
            string_in_char_list.append(names[0][i])
            
        names[0] = ''.join(string_in_char_list)

    # get location of names
    for i in range(len(splitted_text)):
        if "synonyms" in splitted_text[i].lower():
            if "cas" in splitted_text[i-1].lower():
                if "source" in splitted_text[i+1].lower():
                    if 'appearance' in splitted_text[i+2].lower():
                        if 'uvmax' in splitted_text[i+3].lower():
                            names.append(splitted_text[i+5].replace(" ", ""))
                        else:
                            names.append(splitted_text[i+4].replace(" ", ""))
                    else:
                        names.append(splitted_text[i+3].replace(" ", ""))
                else:
                    names.append(splitted_text[i+2].replace(" ", ""))
            else:
                if "source" in splitted_text[i+1].lower():
                    names.append(splitted_text[i+2].replace(" ", ""))
                else:
                    names.append(splitted_text[i+1].replace(" ", ""))

    # filter bad synonyms
    if len(names) > 0: 
        for i in range(len(names)):
            for bad_synonym in bad_synonyms:
                if bad_synonym in names[i-1].lower():
                    names.pop(i-1)

    # filter "/" from names
    tmpnames = "/".join(names)
    names = tmpnames.split("/")
    
    return names

def get_iupac(splitted_text: list) -> list:
    iupac = []
    # first "string" after iupac heading is the iupac name
    for i in range(len(splitted_text)):
        if "iupac" in splitted_text[i].lower():
            iupac.append(splitted_text[i+1].replace(" ", ""))
    return iupac

def get_formula(splitted_text: list) -> str:
    formula = ""
    # first "string" after "base" heading is the formula
    for i in range(len(splitted_text)):
        if "base" in splitted_text[i].casefold():
            formula = splitted_text[i+1].replace(" ", "")
    return formula

def get_inchi() -> str:
    # Not in document
    return ""

def get_inchi_key() -> str:
    # Not in document
    return ""

def get_molecular_mass(splitted_text: list) -> float:
    molecular_mass = 0.0
    # second "string" after "base" heading is the molecular mass
    for i in range(len(splitted_text)):
        if "base" in splitted_text[i].casefold():
            tmp = splitted_text[i+2].replace(" ", ".", 1)
            if tmp.isdigit():
                molecular_mass = float(splitted_text[i+2])

    return molecular_mass

def get_cas_num(splitted_text: list) -> str: # READY
    raw_cas = ""
    out_cas = ''
    
    for i in range(len(splitted_text)):
        if "cas" in splitted_text[i].lower():
            if "synonym" in splitted_text[i+1].lower():
                if "source" in splitted_text[i+2].lower():
                    if "appearance" in splitted_text[i+3].lower():
                        if "uvmax" in splitted_text[i+4].lower():
                            raw_cas = splitted_text[i+5]                        
                        else:
                            raw_cas = splitted_text[i+4]
                    else:
                        raw_cas = splitted_text[i+3]  
                else:
                    raw_cas = splitted_text[i+2]
            elif "source" in splitted_text[i+1].lower():
                raw_cas = splitted_text[i+2]
            else:
                raw_cas = splitted_text[i+1]
    
    
    first_num_at = 0
    first_unsc_at = 0
    second_unsc_at = 0 
    last_num_at = 0
    
    for i in range(len(raw_cas)):
        if first_unsc_at == 0:
            if raw_cas[i] == '0' or raw_cas[i] == '1' or raw_cas[i] == '2' or raw_cas[i] == '3' or raw_cas[i] == '4' or raw_cas[i] == '5' or raw_cas[i] == '6' or raw_cas[i] == '7' or raw_cas[i] == '8' or raw_cas[i] == '9':
                continue
            elif raw_cas[i] == '-':
                first_unsc_at = i
                continue
            else:    
                first_num_at = i+1
                
        elif first_unsc_at != 0: 
            if raw_cas[i] == '-':
                second_unsc_at = i
                continue
        
        if second_unsc_at != 0: 
            if raw_cas[i] == '0' or raw_cas[i] == '1' or raw_cas[i] == '2' or raw_cas[i] == '3' or raw_cas[i] == '4' or raw_cas[i] == '5' or raw_cas[i] == '6' or raw_cas[i] == '7' or raw_cas[i] == '8' or raw_cas[i] == '9':
                last_num_at = i+1
                continue
            else: 
                break
    
    for i in range(first_num_at, last_num_at):
        out_cas += raw_cas[i]
    
    return out_cas

def get_categories() -> list:
    # Not in document
    return [] 

def get_source(pdf) -> tuple:
    # Get Source of pdf as tuple
    tmp_pdf_name = pdf.split("/")
    source_url = "https://swgdrug.org/Monographs/" + tmp_pdf_name[-1]
    return (source_website, source_url)

def get_validation() -> bool:
    # Not in document
    # validation starts later
    return False

def get_deleted_status() -> bool:
    # Not in document
    return False

def get_last_modified():
    # Get last modified / created
    current_dt = str(datetime.now())
    return current_dt

# ------ add extracted data to json-file ------
def add_substance(pdf):
    tmp_pdf_name = pdf.split("/")
    
    # check for file and create new if no json file in directory
    # insert array "[]"
    if os.path.isfile(json_file_path) == False:
        with open(json_file_path, "w") as js: 
            json.dump([], js)
    
    # load content
    with open(json_file_path, "r") as js: 
        content = json.load(js)
    
    # append content 
    content.append(assign_var_to_dict(pdf))
    
    # dump content 
    with open(json_file_path, "w") as outfile: 
        json.dump(content, outfile,  indent = 4, separators = (',',': '))

    logger.info(f'Successfully appended to JSON: {tmp_pdf_name[-1]}')


# ------ output function -------
def extract_to_json():
    logger.info("Starting extraction of data")
    # check for file and create new if no json file in directory
    # insert array "[]"
    if not os.path.isfile(json_file_path):
        with open(json_file_path, "w") as js:
            json.dump([], js)

    get_all_pdf_names()

    for pdf in pdf_file_paths:
        try:
            add_substance(pdf)
        except:
            continue

    logger.info("Finished extraction of data")

