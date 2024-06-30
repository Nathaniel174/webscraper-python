import requests
import json
import os
import logging

# Setup logging:
logger = logging.getLogger("validation_logger")
hdlr = logging.FileHandler(os.path.join("logging", "validation.log"))
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)

json_file_path = os.path.join("data", "output", "data.json")

def validate_data():
    try:
        logger.info("Starting validation of data")
        print("Starting validation...")
        with open(json_file_path) as file:
            content = json.load(file)

        updated_content = get_data_from_api(content)

        with open(json_file_path, 'w') as file:
            json.dump(updated_content, file, ensure_ascii=False, indent=4)
        logger.info("Finished validation of data")
        print("Finished validation")
    except:
        logger.error("VALIDATION ERROR, cannot start validating")

def get_data_from_api(content):
    # properties = "MolecularFormula,MolecularWeight,CanonicalSMILES,InChI,InChIKey,IUPACName"
    not_validated_counter = 0
    validated_counter = 0

    for chemical in content:
        # Validate only if it isnt validated already
        if chemical.get("validated") == False:

            logger.info(f"Starting validation for {chemical.get("source")[1]}")
            print(f"Starting validation for {chemical.get("source")[1]}")

            if (len(chemical.get("iupac_names")) > 0) and (chemical.get("validated") == False):
                # Creating API URL:
                api_url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"
                api_input_domain = "compound"
                api_input_namespace = "name"
                api_input_identifier = chemical.get("iupac_names")[0]
                properties = "MolecularFormula,MolecularWeight,CanonicalSMILES,InChI,InChIKey,IUPACName"
                url = f"{api_url}/{api_input_domain}/{api_input_namespace}/{api_input_identifier}/property/{properties}/JSON"

                # Get Response from API
                response = requests.get(url)

                # Check for correct Status code
                if response.status_code == 200:
                    # Extract data from response
                    data = response.json()

                    # Write data to json file content
                    chemical["smiles"] = data.get("PropertyTable").get("Properties")[0].get("CanonicalSMILES")
                    chemical["molecular_mass"] = float(data.get("PropertyTable").get("Properties")[0].get("MolecularWeight"))
                    chemical["formula"] = data.get("PropertyTable").get("Properties")[0].get("MolecularFormula")
                    chemical["inchi"] = data.get("PropertyTable").get("Properties")[0].get("InChI")
                    chemical["inchi_key"] = data.get("PropertyTable").get("Properties")[0].get("InChIKey")
                    chemical["validated"] = True

                else:
                    logger.error(f"Cannot access API, response code: {response.status_code}")

            if (len(chemical.get("names")) > 0) and (chemical.get("validated") == False):
                # Creating API URL:
                api_url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"
                api_input_domain = "compound"
                api_input_namespace = "name"
                api_input_identifier = chemical.get("names")[0]
                properties = "MolecularFormula,MolecularWeight,CanonicalSMILES,InChI,InChIKey,IUPACName"
                url = f"{api_url}/{api_input_domain}/{api_input_namespace}/{api_input_identifier}/property/{properties}/JSON"

                # Get Response from API
                response = requests.get(url)

                # Check for correct Status code
                if response.status_code == 200:
                    # Extract data from response
                    data = response.json()
                    # Write data to json file content
                    chemical["smiles"] = data.get("PropertyTable").get("Properties")[0].get("CanonicalSMILES")
                    chemical["molecular_mass"] = float(data.get("PropertyTable").get("Properties")[0].get("MolecularWeight"))
                    chemical["formula"] = data.get("PropertyTable").get("Properties")[0].get("MolecularFormula")
                    chemical["inchi"] = data.get("PropertyTable").get("Properties")[0].get("InChI")
                    chemical["inchi_key"] = data.get("PropertyTable").get("Properties")[0].get("InChIKey")

                    iupac_exist = False
                    for iupac in chemical["iupac_names"]:
                        if iupac == data.get("PropertyTable").get("Properties")[0].get("IUPACName"):
                            iupac_exist = True

                    if iupac_exist == False:
                        chemical["iupac_names"].append(data.get("PropertyTable").get("Properties")[0].get("IUPACName"))
                    chemical["validated"] = True

                else:
                    logger.error(f"Cannot access API, response code: {response.status_code}")

            if (chemical.get("cas_num") != "") and (chemical.get("validated") == False):
                # Creating API URL:
                api_url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"
                api_input_domain = "compound"
                api_input_namespace = "name"
                api_input_identifier = chemical.get("cas_num")
                properties = "MolecularFormula,MolecularWeight,CanonicalSMILES,InChI,InChIKey,IUPACName"
                url = f"{api_url}/{api_input_domain}/{api_input_namespace}/{api_input_identifier}/property/{properties}/JSON"

                # Get Response from API
                response = requests.get(url)

                # Check for correct Status code
                if response.status_code == 200:
                    # Extract data from response
                    data = response.json()

                    # Write data to json file content
                    chemical["smiles"] = data.get("PropertyTable").get("Properties")[0].get("CanonicalSMILES")
                    chemical["molecular_mass"] = float(data.get("PropertyTable").get("Properties")[0].get("MolecularWeight"))
                    chemical["formula"] = data.get("PropertyTable").get("Properties")[0].get("MolecularFormula")
                    chemical["inchi"] = data.get("PropertyTable").get("Properties")[0].get("InChI")
                    chemical["inchi_key"] = data.get("PropertyTable").get("Properties")[0].get("InChIKey")

                    iupac_exist = False
                    for iupac in chemical["iupac_names"]:
                        if iupac == data.get("PropertyTable").get("Properties")[0].get("IUPACName"):
                            iupac_exist = True

                    if iupac_exist == False:
                        chemical["iupac_names"].append(data.get("PropertyTable").get("Properties")[0].get("IUPACName"))
                    chemical["validated"] = True

                else:
                    logger.error(f"Cannot access API, response code: {response.status_code}")

            if (chemical.get("formula") != "") and (chemical.get("validated") == False):
                # Creating API URL:
                api_url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"
                api_input_domain = "compound"
                api_input_namespace = "formula"
                api_input_identifier = chemical.get("formula")
                properties = "CanonicalSMILES,MolecularWeight,InChI,InChIKey,IUPACName"
                url = f"{api_url}/{api_input_domain}/{api_input_namespace}/{api_input_identifier}/property/{properties}/JSON"

                # Get Response from API
                response = requests.get(url)

                # Check for correct Status code
                if response.status_code == 200:
                    # Extract data from response
                    data = response.json()

                    # Write data to json file content
                    chemical["smiles"] = data.get("PropertyTable").get("Properties")[0].get("CanonicalSMILES")
                    chemical["molecular_mass"] = float(data.get("PropertyTable").get("Properties")[0].get("MolecularWeight"))
                    chemical["inchi"] = data.get("PropertyTable").get("Properties")[0].get("InChI")
                    chemical["inchi_key"] = data.get("PropertyTable").get("Properties")[0].get("InChIKey")

                    iupac_exist = False
                    for iupac in chemical["iupac_names"]:
                        if iupac == data.get("PropertyTable").get("Properties")[0].get("IUPACName"):
                            iupac_exist = True

                    if iupac_exist == False:
                        chemical["iupac_names"].append(data.get("PropertyTable").get("Properties")[0].get("IUPACName"))
                    chemical["validated"] = True

                else:
                    logger.error(f"Cannot access API, response code: {response.status_code}")

            if (chemical.get("smiles") != "") and (chemical.get("validated") == False):
                # Creating API URL:
                api_url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"
                api_input_domain = "compound"
                api_input_namespace = "smiles"
                api_input_identifier = chemical.get("smiles")
                properties = "MolecularFormula,MolecularWeight,InChI,InChIKey,IUPACName"
                url = f"{api_url}/{api_input_domain}/{api_input_namespace}/{api_input_identifier}/property/{properties}/JSON"

                # Get Response from API
                response = requests.get(url)

                # Check for correct Status code
                if response.status_code == 200:
                    # Extract data from response
                    data = response.json()

                    # Write data to json file content
                    chemical["formula"] = data.get("PropertyTable").get("Properties")[0].get("MolecularFormula")
                    chemical["molecular_mass"] = float(data.get("PropertyTable").get("Properties")[0].get("MolecularWeight"))
                    chemical["inchi"] = data.get("PropertyTable").get("Properties")[0].get("InChI")
                    chemical["inchi_key"] = data.get("PropertyTable").get("Properties")[0].get("InChIKey")

                    iupac_exist = False
                    for iupac in chemical["iupac_names"]:
                        if iupac == data.get("PropertyTable").get("Properties")[0].get("IUPACName"):
                            iupac_exist = True

                    if iupac_exist == False:
                        chemical["iupac_names"].append(data.get("PropertyTable").get("Properties")[0].get("IUPACName"))
                    chemical["validated"] = True

                else:
                    logger.error(f"Cannot access API, response code: {response.status_code}")

            if (chemical.get("inchi") != "") and (chemical.get("validated") == False):
                # Creating API URL:
                api_url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"
                api_input_domain = "compound"
                api_input_namespace = "inchi"
                api_input_identifier = chemical.get("inchi")
                properties = "MolecularFormula,MolecularWeight,CanonicalSMILES,InChIKey,IUPACName"
                url = f"{api_url}/{api_input_domain}/{api_input_namespace}/{api_input_identifier}/property/{properties}/JSON"

                # Get Response from API
                response = requests.get(url)

                # Check for correct Status code
                if response.status_code == 200:
                    # Extract data from response
                    data = response.json()

                    # Write data to json file content
                    chemical["smiles"] = data.get("PropertyTable").get("Properties")[0].get("CanonicalSMILES")
                    chemical["molecular_mass"] = float(data.get("PropertyTable").get("Properties")[0].get("MolecularWeight"))
                    chemical["formula"] = data.get("PropertyTable").get("Properties")[0].get("MolecularFormula")
                    chemical["inchi_key"] = data.get("PropertyTable").get("Properties")[0].get("InChIKey")

                    iupac_exist = False
                    for iupac in chemical["iupac_names"]:
                        if iupac == data.get("PropertyTable").get("Properties")[0].get("IUPACName"):
                            iupac_exist = True

                    if iupac_exist == False:
                        chemical["iupac_names"].append(data.get("PropertyTable").get("Properties")[0].get("IUPACName"))
                    chemical["validated"] = True

                else:
                    logger.error(f"Cannot access API, response code: {response.status_code}")

            if (chemical.get("inchi_key") != "") and (chemical.get("validated") == False):
                # Creating API URL:
                api_url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"
                api_input_domain = "compound"
                api_input_namespace = "inchikey"
                api_input_identifier = chemical.get("inchi_key")
                properties = "MolecularFormula,MolecularWeight,CanonicalSMILES,InChI,IUPACName"
                url = f"{api_url}/{api_input_domain}/{api_input_namespace}/{api_input_identifier}/property/{properties}/JSON"

                # Get Response from API
                response = requests.get(url)

                # Check for correct Status code
                if response.status_code == 200:
                    # Extract data from response
                    data = response.json()

                    # Write data to json file content
                    chemical["smiles"] = data.get("PropertyTable").get("Properties")[0].get("CanonicalSMILES")
                    chemical["molecular_mass"] = float(data.get("PropertyTable").get("Properties")[0].get("MolecularWeight"))
                    chemical["formula"] = data.get("PropertyTable").get("Properties")[0].get("MolecularFormula")
                    chemical["inchi"] = data.get("PropertyTable").get("Properties")[0].get("InChI")

                    iupac_exist = False
                    for iupac in chemical["iupac_names"]:
                        if iupac == data.get("PropertyTable").get("Properties")[0].get("IUPACName"):
                            iupac_exist = True

                    if iupac_exist == False:
                        chemical["iupac_names"].append(data.get("PropertyTable").get("Properties")[0].get("IUPACName"))
                    chemical["validated"] = True

                else:
                    logger.error(f"Cannot access API, response code: {response.status_code}")

            #cas Number search with offical CAS API
            #if (chemical.get("cas_num") != "") and (chemical.get("validated") == False):
            # Die CAS API funktioniert gerade nicht bzw. ist anscheinend neu und muss neu integriert werden indem man sich Registriert bei der Organisation CAS

            # Counter for validated/not validated Chemicals
            if chemical.get("validated") == False:
                not_validated_counter += 1
            else:
                validated_counter += 1

            logger.warning(f"can't validate {chemical.get('names')[0]}")
        else:
            # Counter for validated/not validated Chemicals
            validated_counter += 1

    print(f" Validated: {validated_counter} \n Not Validated: {not_validated_counter}")

    return content
