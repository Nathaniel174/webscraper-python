import json
import os
from os import path

jsonFilePath = "data.json"

pdfFolderPath = "./pdf-files"
pdfFilePaths = []


def getAllPdfNames():
    for file in os.listdir(pdfFolderPath):
        pdfFilePaths.append(pdfFolderPath + "/" + file)

# create dictionary to insert into json-file 
def createDict(pdf):
    
    tmpDict = {}
    # all information about the substance
    names = []
    iupacName = ""
    CAS = ""
    appearance = ""
    base_formular = ""
    base_molecular_weight = ""
    base_melting_point = ""
    HCl_formular = ""
    HCl_molecular_weight = ""
    HCl_melting_point = ""
    # id = ""
    # formula = ""
    # molecularWeight = ""
    # categoryTag = ""
    # inchi = ""
    # inchiKey = ""
    smiles = ""
    url = ""
    timestamp = ""


    # initialise information to specific var 
    # 
    # 
    # PLACEHOLDER
    
    
    # initialise dictionary with found information 
    tmpDict = {"names" : names,
               "iupac_name" : iupacName,
               "CAS" : CAS,
               "appearance" : appearance,
               "base_formular" : base_formular,
               "base_molecular_weight" : base_molecular_weight,
               "base_melting_point" : base_melting_point,
               "HCl_formular" : HCl_formular,
               "HCl_molecular_weight" : HCl_molecular_weight,
               "HCl_melting_point" : HCl_melting_point,
               "smiles" : smiles,
               "url" : url,
               "timestamp" : timestamp
               }
    
    return tmpDict

def addSubstance(pdf):
    
    # check for file and create new if no json file in directory
    # insert array "[]"
    if path.isfile(jsonFilePath) == False:
        with open(jsonFilePath, "w") as js: 
            json.dump([], js) 
    
    # load content
    with open(jsonFilePath, "r") as js: 
        content = json.load(js)
    
    # append content 
    content.append(createDict(pdf))
    
    # dump content 
    with open(jsonFilePath, "w") as outfile: 
        json.dump(content, outfile,  indent = 4, separators = (',',': '))
    
    print('Successfully appended to the JSON file')
    
# --------- main ----------
def add_all_to_json():
    # get all PDF-file names 
    getAllPdfNames()
    for pdf in pdfFilePaths: 
        addSubstance(pdf)