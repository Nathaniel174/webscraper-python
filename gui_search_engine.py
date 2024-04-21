import sys
from PyQt6.QtWidgets import QApplication, QDialog
from ui_gui_app import Ui_gui_app
# make changes from Qt Designer: pyuic6 ui_gui_app.ui -o ui_gui_app.py

app = QApplication(sys.argv)
window = QDialog()
ui = Ui_gui_app()
ui.setupUi(window)

window.show()
sys.exit(app.exec())

# import json

# def search_compound_by_mass(compounds, mass):
#     found_compounds = []
#     for compound in compounds:
#         # Check base molecular weight +- 0.5
#         if "base_molecular_weight" in compound and (compound["base_molecular_weight"] >= (mass-0.5) and compound["base_molecular_weight"] <= (mass+0.5)):
#             found_compounds.append(compound)
#         # Check HCl molecular weight +- 0.5
#         elif "HCl_molecular_weight" in compound and isinstance(compound["HCl_molecular_weight"], (int, float)):
#             if (compound["HCl_molecular_weight"] >= (mass-0.5) and compound["HCl_molecular_weight"] <= (mass+0.5)):
#                 found_compounds.append(compound)
#     return found_compounds

# def main():
#     # Open the JSON file
#     with open('test_data.json', encoding='utf-8') as f:
#         compounds = json.load(f)

#     while True:
#         try:
#             # Ask the user for mass input
#             mass = float(input("Geben Sie die Masse ein: "))
#             break  # Exit the loop if input is valid
#         except ValueError:
#             print("Ungültige Eingabe. Masse sollte eine Zahl sein.")

#     # Search for compounds with the given mass
#     found_compounds = search_compound_by_mass(compounds, mass)

#     # Display the results on the screen
#     if found_compounds:
#         print(f"{len(found_compounds)} Substanz(en) mit Masse {mass} +-0.5 gefunden:")
#         for compound in found_compounds:
#             print("Name:", compound["names"])
#             print("IUPAC name:", compound["iupac_name"])
#             print("CAS:", compound["CAS"])
#             print("Appearance:", compound["appearance"])
#             print("Base formula:", compound["base_formular"])
#             print("Base molecular weight:", compound["base_molecular_weight"])
#             print("Base melting point:", compound["base_melting_point"])
#             print("HCl formula:", compound["HCl_formular"])
#             print("HCl molecular weight:", compound["HCl_molecular_weight"])
#             print("HCl melting point:", compound["HCl_melting_point"])
#             print("URL:", compound["url"])
#             print("-------------------------------------------")
#     else:
#         print(f"Keine Substanzen mit {mass} +-0.5 gefunden.")

# if __name__ == "__main__":
#     main()
