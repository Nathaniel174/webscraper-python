import json
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton, QLineEdit, QFormLayout, QMessageBox, QTextEdit
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Suchmaschine für Designerdrogen') # Set window title
        self.setMinimumSize(500, 400) # Set minimum window size
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
        self.result_number = QTextEdit() # Create a QTextEdit widget to display the number of search results
        self.result_text = QTextEdit()  # Create a QTextEdit widget to display a list of search results
        layout.addWidget(self.result_number)
        layout.addWidget(self.result_text)

        # Connect returnPressed signal of QLineEdit fields to on_button_click method
        self.smiles_field.returnPressed.connect(self.on_button_click)
        self.formel_field.returnPressed.connect(self.on_button_click)
        self.masse_field.returnPressed.connect(self.on_button_click)
   
    #Function to handle the click event of the 'Suchen' button.
    #It retrieves the text from the input fields, constructs a message, and sets it as the text of the result label.
    def on_button_click(self):
        smiles = self.smiles_field.text()
        formel = self.formel_field.text()
        masse = self.masse_field.text()

        # Validate if masse input is a float
        # Convert masse to float if not empty
        if masse:
            try:
                masse = float(masse)
            except ValueError:
                # If not a float, display an error message and return
                QMessageBox.critical(self, 'Fehler', 'Masse sollte eine Zahl sein.')
                return  # Exit the function
        else:
            masse = None  # Set masse to None if field is empty

        self.result_label.setText(f'Ich suche Substanzen mit SMILES {smiles}, Formel {formel} und Masse {masse}')
        
        result = self.search_compound(masse)
        # Clear previous results
        self.result_number.clear()
        self.result_text.clear()

        if result:
            # Display the number of found compounds and their details
            self.result_number.append(f"{len(result)} Substanz(en) mit Masse {masse} +-0.5 gefunden:\n")
            for compound in result:
                self.result_text.append(f"Name: {compound['name']}")
                self.result_text.append(f"Synoyms: {compound['synoyms']}")
                self.result_text.append(f"Formula: {compound['formula']}")
                self.result_text.append(f"Smiles: {compound['smiles']}")
                self.result_text.append(f"inchi: {compound['inchi']}")
                self.result_text.append(f"inchi_key: {compound['inchi_key']}")
                self.result_text.append(f"molecular_mass: {compound['molecular_mass']}")
                self.result_text.append(f"cas-num: {compound['cas-num']}")
                self.result_text.append(f"source_name: {compound['source_name']}")
                self.result_text.append(f"source_url: {compound['source_url']}")
                self.result_text.append(f"status: {compound['status']}")
                self.result_text.append(f"last_changed_at: {compound['last_changed_at']}")
                self.result_text.append(f"special_data: {compound['special_data']}")
                self.result_text.append("-------------------------------------------")
        else:
            # Display a message if no compounds were found
            self.result_number.append(f"Keine Substanzen mit Masse {masse} +-0.5 gefunden.")


    # Function to handle the click event of the 'Löschen' button.
    # It clears the text from all input fields and the result label.
    def clear_fields(self):
        self.smiles_field.clear()
        self.formel_field.clear()
        self.masse_field.clear()
        self.result_label.clear()
        self.result_number.clear()
        self.result_text.clear()

    # Searches for compounds in the JSON file with the given mass.
    # Args: mass (float): The mass to search for.
    # Returns: list: A list of compounds with mass within +-0.5 of the given mass.
    def search_compound(self, mass):
        # Open the JSON file
        with open('test_data.json', encoding='utf-8') as f:
            compounds = json.load(f)

        # Search for compounds with the given mass
        found_compounds = self.search_compound_by_mass(compounds, mass)

        return found_compounds
    
    # Searches for compounds with the given mass within +-0.5 range.
    # Args: compounds (list): A list of compounds to search within. mass (float): The mass to search for.
    # Returns: list: A list of compounds with mass within +-0.5 of the given mass.
    def search_compound_by_mass(self, compounds, mass):
        found_compounds = []
        for compound in compounds:
            # Check if compound has molecular_mass key
            if "molecular_mass" in compound:
                # Check if mass is not None
                if (compound["molecular_mass"] is not None) and (mass is not None):
                    # Check molecular_mass +- 0.5
                    if (compound["molecular_mass"] >= (mass-0.5) and compound["molecular_mass"] <= (mass+0.5)):
                        found_compounds.append(compound)
        return found_compounds


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
