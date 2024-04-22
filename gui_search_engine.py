import json
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton, QLineEdit, QFormLayout

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Suchmaschine für Designerdrogen')
        self.setMinimumSize(350, 200)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        title_label = QLabel('Ich suche...', central_widget)

        layout = QFormLayout(central_widget)
        layout.addRow(title_label) 
        layout.addRow('SMILES', QLineEdit())
        layout.addRow('Formel', QLineEdit())
        layout.addRow('Masse', QLineEdit())

        search_button = QPushButton('Suchen', central_widget)
        clear_button = QPushButton('Löschen', central_widget)
        layout.addRow(search_button, clear_button)


        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()


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
