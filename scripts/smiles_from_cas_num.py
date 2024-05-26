# if there is no SMILES in the JSON file, then it is created from the cas_number and saved in the JSON file

import json
import requests

# JSON file
data_json = 'test_data.json'

def fetch_smiles_from_pubchem(cas_number):
    # Construct the PubChem API URL using the given CAS number
    url = f'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{cas_number}/property/CanonicalSMILES/JSON'
    # Make a GET request to the PubChem API
    response = requests.get(url)
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        # Extract the SMILES string from the response data
        smiles = data.get('PropertyTable', {}).get('Properties', [{}])[0].get('CanonicalSMILES', '')
        return smiles
    else:
        # Return None if the request failed
        return None

def smiles_from_cas():
    # Open and load the JSON file containing compounds data
    with open(data_json, encoding='utf-8') as f:
        compounds = json.load(f)

    for compound in compounds:
        # Check if the compound already has a SMILES string
        if not compound.get("smiles"):
            # Get the CAS number and remove any extra whitespace
            cas_num = (compound.get("cas_num")).split()[0]
            smiles = fetch_smiles_from_pubchem(cas_num)
            # If a SMILES string was found, update the compound's data
            if smiles:
                compound["smiles"] = smiles

    # Save the updated compounds data back to the JSON file
    with open(data_json, 'w', encoding='utf-8') as f:
        json.dump(compounds, f, ensure_ascii=False, indent=4)
            

# if __name__ == '__main__':
#     smiles_from_cas()