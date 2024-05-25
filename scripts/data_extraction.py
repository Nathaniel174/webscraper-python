import json
import os
from os import path
from pypdf import PdfReader
from datetime import datetime

jsonFilePath = "data.json"

pdfFolderPath = "./pdf-files"
pdfFilePaths = []


def get_all_pdf_names():
    for file in os.listdir(pdfFolderPath):
        pdfFilePaths.append(pdfFolderPath + "/" + file)
    

# create dictionary to insert into json-file 
def create_dict(pdf):
    
    tmp_pdf_name = pdf.split("/")
    current_dt = str(datetime.now())
    
    tmpDict = {}
    # all information about the substance
    name = "" # IUPAC Name
    synonyms = [] # Synonyms 
    formula = "" # Chemical Formula 
    smiles = "" 
    inchi = ""
    inchi_key = ""
    molecular_mass = ""
    cas_num = ""
    source_name = "swgdrugs"
    source_url = "https://swgdrug.org/Monographs/" + tmp_pdf_name[-1]
    status = ""
    last_changed_at = current_dt
    special_data = []
    
    # ------------
    # initialise information to specific var:
    
    # read PDF into text as string
    reader = PdfReader(pdf)
    text = reader.pages[0].extract_text()
    splittedText = text.split("\n")
    
    # Text extract for one line phrases 
    for phrase in splittedText:
        # IUPAC Name
        if "iupac" in phrase.casefold():
            tmp = phrase.split(": ")
            tmpNoSpaces = []
            for char in tmp[-1]: 
                if " " != char: 
                    tmpNoSpaces.append(char)
            name = "".join(tmpNoSpaces)
            
        # CAS 
        if "cas" in phrase.casefold():
            tmp = phrase.split(": ")
            tmpNoSpaces = []
            for char in tmp[-1]: 
                if " " != char: 
                    tmpNoSpaces.append(char)
            cas_num = "".join(tmpNoSpaces)
            
        # Source 
        # if "source" in phrase.casefold():
        #     tmp = phrase.split(": ")
        #     source_name = tmp[-1]
            
        # Chemical Formula and Molecular Weight
        
        
        if "base" in phrase.casefold():
            tmp =  phrase.split(" ")
            tmpNoSpaces = []
            for element in tmp:
                if "" != element:
                    tmpNoSpaces.append(element)
            if len(tmpNoSpaces) >= 2:
                formula = tmpNoSpaces[1]
                if len(tmpNoSpaces) >= 3:
                    molecular_mass = tmpNoSpaces[2]
        
    # # Synonyms: 
    # splittedText = text.split("Synonyms: ") 
    # tmpText = splittedText[1].split("Source: ")
    # splittedText = tmpText[0]
    # tmpText = splittedText.split(", ")
    # tmpText

    # for sub in tmpText:
    #     name.append(sub.replace("\n", ""))
    
    # initialise dictionary with found information 
    tmpDict = {"name" : name,
               "synoyms" : synonyms,
               "formula" : formula,
               "smiles" : smiles,
               "inchi" : inchi,
               "inchi_key" : inchi_key,
               "molecular_mass" : molecular_mass,
               "cas-num" : cas_num,
               "source_name" : source_name,
               "source_url" : source_url,
               "status" : status,
               "last_changed_at" : last_changed_at,
               "special_data" : special_data
               }
    
    return tmpDict

def add_substance(pdf):
    
    tmp_pdf_name = pdf.split("/")
    
    # check for file and create new if no json file in directory
    # insert array "[]"
    if path.isfile(jsonFilePath) == False:
        with open(jsonFilePath, "w") as js: 
            json.dump([], js) 
    
    # load content
    with open(jsonFilePath, "r") as js: 
        content = json.load(js)
    
    # append content 
    content.append(create_dict(pdf))
    
    # dump content 
    with open(jsonFilePath, "w") as outfile: 
        json.dump(content, outfile,  indent = 4, separators = (',',': '))
    
    print('Successfully appended to JSON: ', tmp_pdf_name[-1])
    
# --------- main ----------
def add_all_to_json():
    # get all PDF-file names 
    get_all_pdf_names()
    for pdf in pdfFilePaths: 
        add_substance(pdf)