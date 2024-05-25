import json
import os
from os import path
from datetime import datetime
import re
from pdfminer.high_level import extract_pages, extract_text

# Init json file path and path for pdf_folder with existing pdfs:
json_file_path = "data.json"
pdf_folder_path = "/Users/nathaniel/Development/Programmieren/Python/PrPr/webscraper-python/pdf-files"
source_website = "swgdrugs"

# Array with paths in string type 
pdf_file_paths = []

# get all existing pdf file names from pdf_folder
def get_all_pdf_names() -> None:
    for file in os.listdir(pdf_folder_path):
        pdf_file_paths.append(pdf_folder_path + "/" + file)

# create dictionary for inserting data into json-file 
def assign_var_to_dict(pdf: str) -> dict:
    pdf_text = pdf_to_string(pdf)
    # initialise dictionary with found information 
    return_dict = {"version" : get_version(),
                   "smiles" : get_smiles(),
                   "names" : get_names(pdf_text),
                   "iupac_names" : get_iupac(pdf_text),
                   "formula" : get_formula(pdf_text),
                   "inchi" : get_inchi(),
                   "inchi_key" : get_inchi_key(),
                   "molecular_mass" : get_molecular_mass(pdf_text),
                   "cas_num" : get_cas_num(pdf_text),
                   "categories" : get_categories(),
                   "source" : get_source(pdf),
                   "validated" : get_validation(),
                   "deleted" : get_deleted_status(),
                   "last_modified" : get_last_modified(),
                   "details": {}
               }
    return return_dict

# extract data from pdf to string 
def pdf_to_string(pdf):
    # read PDF into text as string
    text = extract_text(pdf)
    if 'cid:0' in text:
        text = text.replace('(cid:0)','')
    splitted_text = text.split('\n')
    counter_blank = 0
    counter_space = 0
    for i in range(len(splitted_text)):
        if splitted_text[i] == '':
            counter_blank += 1     
        elif splitted_text[i] == ' ':
            counter_space += 1
        
    for i in range(counter_blank):
        splitted_text.remove('')
    for i in range(counter_space):
        splitted_text.remove(' ')
    
    return splitted_text
                               
# ------ get functions ------  
def get_version() -> str:
    return ""

def get_smiles() -> str:
    return ""

def get_names(splitted_text: list) -> list:
    # Erstes Element ist immer der Name als Überschrift
    names = []
    bad_synonyms = ["uvmax", "n/a", "cfr" ]
    
    for i in range(3):
        if 'drug' not in splitted_text[i].lower():
            if 'this' not in splitted_text[i].lower():
                names.append(splitted_text[i])
                break

    for i in range(len(splitted_text)):
        if "synonyms" in splitted_text[i].lower():
            if "cas" in splitted_text[i-1].lower():
                if "source" in splitted_text[i+1].lower():
                    if 'appearance' in splitted_text[i+2].lower():
                        if 'uvmax' in splitted_text[i+3].lower():
                            names.append(splitted_text[i+5])
                        else:
                            names.append(splitted_text[i+4])
                    else:
                        names.append(splitted_text[i+3])
                else:
                    names.append(splitted_text[i+2])
            else:
                if "source" in splitted_text[i+1].lower():
                    names.append(splitted_text[i+2])
                else:
                    names.append(splitted_text[i+1])
    
    if len(names) > 0: 
        for i in range(len(names)):
            for bad_synonym in bad_synonyms:
                if bad_synonym in names[i-1].lower():
                    names.pop(i-1)
    
    return names

def get_iupac(splitted_text: list) -> list:
    iupac = []
    for i in range(len(splitted_text)):
        if "iupac" in splitted_text[i].lower():
            iupac.append(splitted_text[i+1])
    return iupac

def get_formula(splitted_text: list) -> str:
    return ""

def get_inchi() -> str:
    return ""

def get_inchi_key() -> str:
    return ""

def get_molecular_mass(splitted_text: list) -> float:
    molecular_mass = 0.0
    # for phrase in splitted_text: 
    #     if "base" in phrase.casefold():
    #         tmp =  phrase.split(" ")
    #         tmpNoSpaces = []
    #         for element in tmp:
    #             if "" != element:
    #                 tmpNoSpaces.append(element)
    #         if len(tmpNoSpaces) >= 2:
    #             formula = tmpNoSpaces[1]
    #             if len(tmpNoSpaces) >= 3:
    #                 molecular_mass = tmpNoSpaces[2]
    return molecular_mass

def get_cas_num(splitted_text: list) -> str: # READY
    cas = ""
    bad_keywords = ['schedul', '']
    for i in range(len(splitted_text)):
        if "cas" in splitted_text[i].lower():
            if "synonym" in splitted_text[i+1].lower():
                if "source" in splitted_text[i+2].lower():
                    if "appearance" in splitted_text[i+3].lower():
                        if "uvmax" in splitted_text[i+4].lower():
                            cas = splitted_text[i+5]                        
                        else:
                            cas = splitted_text[i+4]
                    else:
                        cas = splitted_text[i+3]  
                else:
                    cas = splitted_text[i+2]
            elif "source" in splitted_text[i+1].lower():
                cas = splitted_text[i+2]
            else:
                cas = splitted_text[i+1]
    return cas

def get_categories() -> list:
    return [] 

def get_source(pdf) -> tuple: # READY
    tmp_pdf_name = pdf.split("/")
    source_url = "https://swgdrug.org/Monographs/" + tmp_pdf_name[-1]
    return  (source_website, source_url)

def get_validation() -> bool:
    return False

def get_deleted_status() -> bool: 
    return False

def get_last_modified(): # CHECK: Website oder in json hinzugefügt?
    current_dt = str(datetime.now())
    return current_dt

# ------ add extracted data to json-file ------

def add_substance(pdf):
    
    tmp_pdf_name = pdf.split("/")
    
    # check for file and create new if no json file in directory
    # insert array "[]"
    if path.isfile(json_file_path) == False:
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
    
    print('Successfully appended to JSON: ', tmp_pdf_name[-1])    


# ------ output function -------

def extract_to_json():
    get_all_pdf_names()
    for pdf in pdf_file_paths:
        add_substance(pdf)
        
if __name__ == "__main__":
    extract_to_json()
    
    # pdf_test_path = '/Users/nathaniel/Development/Programmieren/Python/PrPr/webscraper-python/pdf-files/25D_NBOMe.pdf'
    # print(pdf_to_string(pdf_test_path))
    # get_all_pdf_names()
    # for i in range(len(pdf_file_paths)):
    #     if '25D_NBOMe.pdf' in pdf_file_paths[i]:
    #         add_substance(pdf_test_path)