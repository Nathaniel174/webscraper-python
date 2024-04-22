import json
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton, QLineEdit, QFormLayout, QMessageBox, QTextEdit
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Suchmaschine für Designerdrogen') # Set window title
        self.setMinimumSize(350, 200) # Set minimum window size
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.result_label = QLabel()

        # Creating a label widget with text 'Ich suche...'
        title_label = QLabel('Ich suche...', central_widget)

        layout = QFormLayout(central_widget)
        layout.addRow(title_label)
        # Add a line edit widget for SMILES
        self.smiles_field = QLineEdit()
        layout.addRow('SMILES', self.smiles_field)
        # Add a line edit widget for Formel
        self.formel_field = QLineEdit()
        layout.addRow('Formel', self.formel_field)
        # Add a line edit widget for Masse
        self.masse_field = QLineEdit()
        layout.addRow('Masse', self.masse_field)

        search_button = QPushButton('Suchen', central_widget)
        clear_button = QPushButton('Löschen', central_widget)
        # Connect search button to on_button_click method
        search_button.clicked.connect(self.on_button_click)
        # Connect clear button to clear_fields method
        clear_button.clicked.connect(self.clear_fields)
        layout.addRow(search_button, clear_button)
        layout.addWidget(self.result_label)
        self.result_text = QTextEdit()  # Create a QTextEdit widget to display search results
        layout.addWidget(self.result_text)
   
    #Function to handle the click event of the 'Suchen' button.
    #It retrieves the text from the input fields, constructs a message, and sets it as the text of the result label.
    def on_button_click(self):
        smiles = self.smiles_field.text()
        formel = self.formel_field.text()
        masse = self.masse_field.text()

        # Validate if masse input is a float
        try:
            masse = float(masse)
        except ValueError:
            # If not a float, display an error message
            QMessageBox.critical(self, 'Fehler', 'Masse sollte eine Zahl sein.')
            return  # Exit the function

        self.result_label.setText(f'Ich suche Substanzen mit SMILES {smiles}, Formel {formel} und Masse {masse}')
    
        result = self.search_compound(masse)
        self.result_text.clear()  # Clear previous results

        if result:
            self.result_text.append(f"{len(result)} Substanz(en) mit Masse {masse} +-0.5 gefunden:\n")
            for compound in result:
                self.result_text.append(f"Name: {compound['names']}")
                self.result_text.append(f"IUPAC name: {compound['iupac_name']}")
                self.result_text.append(f"CAS: {compound['CAS']}")
                self.result_text.append(f"Appearance: {compound['appearance']}")
                self.result_text.append(f"Base formula: {compound['base_formular']}")
                self.result_text.append(f"Base molecular weight: {compound['base_molecular_weight']}")
                self.result_text.append(f"Base melting point: {compound['base_melting_point']}")
                self.result_text.append(f"HCl formula: {compound['HCl_formular']}")
                self.result_text.append(f"HCl molecular weight: {compound['HCl_molecular_weight']}")
                self.result_text.append(f"HCl melting point: {compound['HCl_melting_point']}")
                self.result_text.append(f"URL: {compound['url']}")
                self.result_text.append("-------------------------------------------")
        else:
            self.result_text.append(f"Keine Substanzen mit {masse} +-0.5 gefunden.")


    # Function to handle the click event of the 'Löschen' button.
    # It clears the text from all input fields and the result label.
    def clear_fields(self):
        self.smiles_field.clear()
        self.formel_field.clear()
        self.masse_field.clear()
        self.result_label.clear()
        self.result_text.clear()

    def search_compound(self, mass):
        # Open the JSON file
        with open('test_data.json', encoding='utf-8') as f:
            compounds = json.load(f)

        # Search for compounds with the given mass
        found_compounds = self.search_compound_by_mass(compounds, mass)

        return found_compounds
        
    def search_compound_by_mass(self, compounds, mass):
        found_compounds = []
        for compound in compounds:
            # Check base molecular weight +- 0.5
            if "base_molecular_weight" in compound and (compound["base_molecular_weight"] >= (mass-0.5) and compound["base_molecular_weight"] <= (mass+0.5)):
                found_compounds.append(compound)
            # Check HCl molecular weight +- 0.5
            elif "HCl_molecular_weight" in compound and isinstance(compound["HCl_molecular_weight"], (int, float)):
                if (compound["HCl_molecular_weight"] >= (mass-0.5) and compound["HCl_molecular_weight"] <= (mass+0.5)):
                    found_compounds.append(compound)
        return found_compounds


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
