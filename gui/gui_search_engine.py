import json
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton, QLineEdit, QFormLayout, QMessageBox, QHBoxLayout, QVBoxLayout, QScrollArea, QSizePolicy
from PyQt6.QtCore import Qt

# JSON file
data_json = 'test_data.json'

class ResultWidget(QWidget):
    def __init__(self, compound):
        super().__init__()
        self.compound = compound
        layout = QVBoxLayout(self)

        self.info_label = QLabel(f"Name: {compound['names']} \nSMILES: {compound['smiles']}\nFormel: {compound['formula']}\nMasse: {compound['molecular_mass']}\n")
        layout.addWidget(self.info_label)

        button_layout = QHBoxLayout()
        self.info_button = QPushButton('Info')
        self.pdf_button = QPushButton('PDF')
        button_layout.addWidget(self.info_button)
        button_layout.addWidget(self.pdf_button)
        layout.addLayout(button_layout)

        # Connect buttons to actions
        self.info_button.clicked.connect(self.show_info)
        self.pdf_button.clicked.connect(self.show_pdf)

    def show_info(self):
        QMessageBox.information(self, 'Info', f"Information about {self.compound['names']}")

    def show_pdf(self):
        QMessageBox.information(self, 'PDF', f"PDF for {self.compound['names']}")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Suchmaschine für Designerdrogen') # Set window title
        self.setMinimumSize(650, 400) # Set minimum window size
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        title_label = QLabel('Ich suche...')
        layout.addWidget(title_label)

        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignLeft) # Align labels to the left
        form_layout.setFormAlignment(Qt.AlignmentFlag.AlignLeft) # Align form items to the left

        # Add a line edit widget for SMILES
        self.smiles_field = QLineEdit()
        self.smiles_field.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        form_layout.addRow('SMILES', self.smiles_field)

        # Add a line edit widget for Formel
        self.formel_field = QLineEdit()
        self.formel_field.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        form_layout.addRow('Formel', self.formel_field)

        # Add a line edit widget for Masse
        self.mass_field = QLineEdit()
        self.mass_field.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        form_layout.addRow('Masse', self.mass_field)

        layout.addLayout(form_layout)

        button_layout = QHBoxLayout()
        search_button = QPushButton('Suchen')
        clear_button = QPushButton('Löschen')
        button_layout.addWidget(search_button)
        button_layout.addWidget(clear_button)
        layout.addLayout(button_layout)

        self.result_number = QLabel()  # QLabel to display the number of search results
        layout.addWidget(self.result_number)

        # Scroll area to hold the search results
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.results_container = QWidget()
        self.results_layout = QVBoxLayout(self.results_container)
        self.scroll_area.setWidget(self.results_container)
        layout.addWidget(self.scroll_area)

        # Connect search button to on_button_click method
        search_button.clicked.connect(self.on_button_click)
        # Connect clear button to clear_fields method
        clear_button.clicked.connect(self.clear_fields)

        # Connect returnPressed signal of QLineEdit fields to on_button_click method
        self.smiles_field.returnPressed.connect(self.on_button_click)
        self.formel_field.returnPressed.connect(self.on_button_click)
        self.mass_field.returnPressed.connect(self.on_button_click)

    def on_button_click(self):
        smiles = self.smiles_field.text()
        formel = (self.formel_field.text()).upper().strip()
        mass = self.mass_field.text()

        if mass:
            try:
                mass = float(mass)
            except ValueError:
                QMessageBox.critical(self, 'Fehler', 'Masse sollte eine Zahl sein.')
                return
        else:
            mass = None

        result = self.search_compound(smiles, formel, mass)
        self.result_number.clear()
        # Clear previous results
        for i in reversed(range(self.results_layout.count())): 
            self.results_layout.itemAt(i).widget().setParent(None)

        if result:
            self.result_number.setText(f"{len(result)} Substanz(en) mit SMILES {smiles}, Formel {formel} und Masse {mass} +-0.5 gefunden:\n")
            for compound in result:
                result_widget = ResultWidget(compound)
                self.results_layout.addWidget(result_widget)
        else:
            self.result_number.setText(f"Keine Substanzen mit SMILES {smiles}, Formel {formel} und Masse {mass} +-0.5 gefunden.")

    def clear_fields(self):
        self.smiles_field.clear()
        self.formel_field.clear()
        self.mass_field.clear()
        self.result_number.clear()
        for i in reversed(range(self.results_layout.count())): 
            self.results_layout.itemAt(i).widget().setParent(None)

    def search_compound(self, smiles, formel, mass):
        with open(data_json, encoding='utf-8') as f:
            compounds = json.load(f)

        if mass is not None:
            if formel:
                if smiles:
                    found_compounds_mass = self.search_compound_by_mass(compounds, mass)
                    found_compounds_formel = self.search_compound_by_formel(found_compounds_mass, formel)
                    found_compounds = self.search_compound_by_smiles(found_compounds_formel, smiles)
                else:
                    found_compounds_mass = self.search_compound_by_mass(compounds, mass)
                    found_compounds = self.search_compound_by_formel(found_compounds_mass, formel)
            elif smiles:
                found_compounds_mass = self.search_compound_by_mass(compounds, mass)
                found_compounds = self.search_compound_by_smiles(found_compounds_mass, smiles)
            else:
                found_compounds = self.search_compound_by_mass(compounds, mass)
            return found_compounds
        elif formel:
            if smiles:
                found_compounds_formel = self.search_compound_by_formel(compounds, formel)
                found_compounds = self.search_compound_by_smiles(found_compounds_formel, smiles)
            else:
                found_compounds = self.search_compound_by_formel(compounds, formel)
            return found_compounds
        elif smiles:
            found_compounds = self.search_compound_by_smiles(compounds, smiles)
            return found_compounds
        else:
            return compounds

    def search_compound_by_mass(self, compounds, mass):
        found_compounds = []
        for compound in compounds:
            if "molecular_mass" in compound:
                if (compound["molecular_mass"] is not None) and (mass is not None):
                    if (compound["molecular_mass"] >= (mass-0.5) and compound["molecular_mass"] <= (mass+0.5)):
                        found_compounds.append(compound)
        return found_compounds
    
    def search_compound_by_formel(self, compounds, formel):
        found_compounds = []
        for compound in compounds:
            if (compound["formula"] is not None) and (formel is not None):
                if ((compound["formula"]).upper() == formel):
                    found_compounds.append(compound)
        return found_compounds
    
    def search_compound_by_smiles(self, compounds, smiles):
        found_compounds = []
        for compound in compounds:
            if (compound["smiles"] is not None) and (smiles is not None):
                if ((compound["smiles"]) == smiles):
                    found_compounds.append(compound)
        return found_compounds

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
