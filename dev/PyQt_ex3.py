import sys
from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QShortcut
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import Qt

class TableWidgetDemo(QWidget):
    def __init__(self):
        super().__init__()

        # Création d'une table avec 5 lignes et 3 colonnes
        self.table_widget = QTableWidget(5, 3, self)
        self.table_widget.setHorizontalHeaderLabels(['Colonne 1', 'Colonne 2', 'Colonne 3'])

        # Remplissage de quelques cellules de la table
        for i in range(5):
            for j in range(3):
                item = QTableWidgetItem(f'Item {i+1},{j+1}')
                self.table_widget.setItem(i, j, item)

        # Mise en page
        layout = QVBoxLayout()
        layout.addWidget(self.table_widget)
        self.setLayout(layout)

        self.setWindowTitle("PyQt5 - Copier/Coller avec Ctrl+C et Ctrl+V")

        # Définir les raccourcis Ctrl+C et Ctrl+V
        self.copy_shortcut = QShortcut(QKeySequence("Ctrl+C"), self)
        self.copy_shortcut.activated.connect(self.copy_selection)

        self.paste_shortcut = QShortcut(QKeySequence("Ctrl+V"), self)
        self.paste_shortcut.activated.connect(self.paste_selection)

    def copy_selection(self):
        """Copie la sélection de la table dans le presse-papiers au format texte (tableur compatible)"""
        selection = self.table_widget.selectedRanges()

        if selection:
            copied_text = ""

            for selected_range in selection:
                for row in range(selected_range.topRow(), selected_range.bottomRow() + 1):
                    row_data = []
                    for col in range(selected_range.leftColumn(), selected_range.rightColumn() + 1):
                        item = self.table_widget.item(row, col)
                        if item:
                            row_data.append(item.text())
                        else:
                            row_data.append('')  # Pour les cellules vides
                    copied_text += "\t".join(row_data) + "\n"

            # Envoi du texte au presse-papiers du système
            clipboard = QApplication.clipboard()
            clipboard.setText(copied_text.strip())

            print("Données copiées dans le presse-papiers :")
            print(copied_text)
        else:
            print("Aucune cellule sélectionnée.")

    def paste_selection(self):
        """Colle les données du presse-papiers dans la table"""
        clipboard = QApplication.clipboard()
        pasted_text = clipboard.text()

        if pasted_text:
            # Sépare les lignes et colonnes en fonction du format tabulaire
            rows = pasted_text.split("\n")
            current_row = self.table_widget.currentRow()
            current_column = self.table_widget.currentColumn()

            for i, row_data in enumerate(rows):
                columns = row_data.split("\t")
                for j, col_data in enumerate(columns):
                    row = current_row + i
                    col = current_column + j

                    if row < self.table_widget.rowCount() and col < self.table_widget.columnCount():
                        item = QTableWidgetItem(col_data)
                        self.table_widget.setItem(row, col, item)

            print("Données collées depuis le presse-papiers :")
            print(pasted_text)
        else:
            print("Le presse-papiers est vide.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = TableWidgetDemo()
    demo.show()
    sys.exit(app.exec_())

