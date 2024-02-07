from typing import List
from PyQt5.QtWidgets import QWidget, QApplication, QHBoxLayout, QPushButton, QTabWidget, QVBoxLayout, QFrame, QTabBar, QFormLayout, QLabel, QLineEdit, QTextEdit, QMessageBox, QGroupBox, QRadioButton, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import QSize

from db.db import db, Clinica, config, Database

class ClinicaPage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.initUI()
        self.load_data()
    
    def initUI(self):
        self.setWindowTitle("Clinica")

        # Center the window on the screen
        width = 500
        height = 500

        screen_geometry = QApplication.desktop().screenGeometry() # type: ignore
        x = (screen_geometry.width() - width) / 2
        y = (screen_geometry.height() - height) / 2

        self.setGeometry(int(x), int(y), width, height)

        # Main layout
        self.layout = QVBoxLayout() # type: ignore

        self.top_frame = QFrame()
        self.top_frame_layout = QHBoxLayout()

        self.top_frame.setLayout(self.top_frame_layout)
        self.layout.addWidget(self.top_frame)
        self.setLayout(self.layout)

        # Create a groupbox 
        self.orden_groupbox = QGroupBox("Orden")
        self.orden_groupbox_layout = QVBoxLayout()
        self.orden_groupbox.setLayout(self.orden_groupbox_layout)
        self.top_frame_layout.addWidget(self.orden_groupbox)

        # Add the order selector
        # Create two radio buttons 'codigo' and 'nombre'
        self.inicial_radio = QRadioButton("Inicial")
        self.inicial_radio.setChecked(True)
        self.nombre_radio = QRadioButton("Nombre")
        self.orden_groupbox_layout.addWidget(self.inicial_radio)
        self.orden_groupbox_layout.addWidget(self.nombre_radio)


        # Create two buttons 'Edicion' and 'Salir'
        self.edit_button = QPushButton("Editar")
        self.save_button = QPushButton("Guardar")
        self.salir_button = QPushButton("Salir")
        self.top_frame_layout.addStretch(1)
        self.top_frame_layout.addWidget(self.edit_button)
        self.top_frame_layout.addWidget(self.save_button)
        self.top_frame_layout.addWidget(self.salir_button)

        # Add actions
        self.save_button.clicked.connect(self.save_data)
        self.salir_button.clicked.connect(self.close) # type: ignore
        self.edit_button.clicked.connect(self.edit_clinica)

        # Create a table
        self.bottom_table = QTableWidget()
        self.layout.addWidget(self.bottom_table)

        self.bottom_frame = QFrame()
        self.bottom_frame_layout = QHBoxLayout()
        self.bottom_frame.setLayout(self.bottom_frame_layout)

        self.add_button = QPushButton("Añadir")
        self.bottom_frame_layout.addWidget(self.add_button)
        self.add_button.clicked.connect(self.add_clinica)

        self.delete_button = QPushButton("Eliminar")
        self.bottom_frame_layout.addWidget(self.delete_button)
        self.delete_button.clicked.connect(self.delete_clinica)

        self.layout.addWidget(self.bottom_frame)
    
    def close(self):
        return super().close()

    def save_data(self):

        to_insert_data = self.clinicas_data[self.bottom_table.currentRow()]

        import toml
        config['config']['clinica_id'] = to_insert_data.id # type: ignore

        # Save the config file
        with open('config.toml', 'w') as f:
            toml.dump(config, f)
        
    def order_data(self):
        if self.inicial_radio.isChecked():
            self.clinicas_data = sorted(self.clinicas_data, key=lambda x: x.letra) # type: ignore
        elif self.nombre_radio.isChecked():
            self.clinicas_data = sorted(self.clinicas_data, key=lambda x: x.nombre) # type: ignore
        
        self.bottom_table.clearContents()
        self.bottom_table.setRowCount(len(self.clinicas_data))
        self.bottom_table.setColumnCount(2)

        self.bottom_table.setHorizontalHeaderLabels(["Inicial", "Nombre"])

        for i, clinica in enumerate(self.clinicas_data):
            self.bottom_table.setItem(i, 0, QTableWidgetItem(clinica.letra)) # type: ignore
            self.bottom_table.setItem(i, 1, QTableWidgetItem(clinica.nombre)) # type: ignore




    def load_data(self):
        self.clinicas_data = db.session.query(Clinica).order_by(Clinica.letra).all()
        

        self.bottom_table.setRowCount(len(self.clinicas_data))
        self.bottom_table.setColumnCount(2)

        self.bottom_table.setHorizontalHeaderLabels(["Inicial", "Nombre"])

        for i, clinica in enumerate(self.clinicas_data):
            self.bottom_table.setItem(i, 0, QTableWidgetItem(clinica.letra)) # type: ignore
            self.bottom_table.setItem(i, 1, QTableWidgetItem(clinica.nombre)) # type: ignore
    
    def edit_clinica(self):
        clinica = self.clinicas_data[self.bottom_table.currentRow()]

        self.edit_clinica = EditClinica(clinica, self)
        self.edit_clinica.show()
    
    def add_clinica(self):
        self.add_clinica = AddClinica(self)
        self.add_clinica.show()

    def delete_clinica(self):
        # Create a confirm dialog
        confirm = QMessageBox()
        confirm.setWindowTitle("Eliminar")
        confirm.setText(f"¿Estás seguro de que quieres eliminar la clínica {self.clinicas_data[self.bottom_table.currentRow()].nombre}?")

        confirm.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        confirm.setDefaultButton(QMessageBox.No)

        # If the user confirms, delete the clinica
        if confirm.exec_() == QMessageBox.No:
            return


        clinica = self.clinicas_data[self.bottom_table.currentRow()]

        thread_safe_db = Database()

        # Query the database for the clinica
        clinica = thread_safe_db.session.query(Clinica).filter_by(id=clinica.id).first()

        # Delete the clinica
        try:
            thread_safe_db.session.delete(clinica)
            thread_safe_db.session.flush()
            thread_safe_db.session.commit()
            thread_safe_db.session.close()
        except Exception as e:
            print("Commit failed: ", e)
            thread_safe_db.session.rollback()
        self.load_data()
        self.order_data()

        
class EditClinica(QWidget):
    def __init__(self, clinica: Clinica, upper) -> None:
        super().__init__()
        self.clinica = clinica
        self.upper = upper
        self.initUI()
    
    def initUI(self):
        self.layout = QHBoxLayout() # type: ignore
        self.setLayout(self.layout)

        self.setWindowTitle("Editar Clinica")

        # Center the window on the screen
        width = 800
        height = 50

        screen_geometry = QApplication.desktop().screenGeometry() # type: ignore
        x = (screen_geometry.width() - width) / 2
        y = (screen_geometry.height() - height) / 2

        self.setGeometry(int(x), int(y), width, height)

        # Create a label and a line edit for 'letra; and 'nombre'
        self.letra_label = QLabel("Letra")
        self.letra_lineedit = QLineEdit()
        
        self.nombre_label = QLabel("Nombre")
        self.nombre_lineedit = QLineEdit()

        self.letra_lineedit.setText(self.clinica.letra) # type: ignore
        self.nombre_lineedit.setText(self.clinica.nombre) # type: ignore

        self.layout.addWidget(self.letra_label)
        self.layout.addWidget(self.letra_lineedit)
        self.layout.addWidget(self.nombre_label)
        self.layout.addWidget(self.nombre_lineedit)

        # Create a button 'Guardar'
        self.save_button = QPushButton("Guardar")
        self.layout.addWidget(self.save_button)

        # Add actions
        self.save_button.clicked.connect(self.save_data)
    
    def save_data(self):
        thread_safe_db = Database()

        clinica_from_db = thread_safe_db.session.query(Clinica).filter_by(id=self.clinica.id).first() # type: ignore

        if clinica_from_db is None:
            QMessageBox.critical(self, "Error", "No se ha encontrado la clinica")
            return

        clinica_from_db.letra = self.letra_lineedit.text() # type: ignore
        clinica_from_db.nombre = self.nombre_lineedit.text() # type: ignore

        try:
            thread_safe_db.session.flush()
            thread_safe_db.session.commit()
            thread_safe_db.session.close()
            self.upper.load_data()
            self.upper.order_data()
            self.close()
        except Exception as e:
            print("Commit failed: ", e)
            thread_safe_db.session.rollback()
            



class AddClinica(QWidget):
    def __init__(self,  upper) -> None:
        super().__init__()
        self.upper = upper
        self.initUI()
    
    def initUI(self):
        self.layout = QHBoxLayout() # type: ignore
        self.setLayout(self.layout)

        self.setWindowTitle("Añadir Clinica")

        # Center the window on the screen
        width = 800
        height = 50

        screen_geometry = QApplication.desktop().screenGeometry() # type: ignore
        x = (screen_geometry.width() - width) / 2
        y = (screen_geometry.height() - height) / 2

        self.setGeometry(int(x), int(y), width, height)

        # Create a label and a line edit for 'letra; and 'nombre'
        self.letra_label = QLabel("Letra")
        self.letra_lineedit = QLineEdit()
        
        self.nombre_label = QLabel("Nombre")
        self.nombre_lineedit = QLineEdit()

        self.layout.addWidget(self.letra_label)
        self.layout.addWidget(self.letra_lineedit)
        self.layout.addWidget(self.nombre_label)
        self.layout.addWidget(self.nombre_lineedit)

        # Create a button 'Guardar'
        self.save_button = QPushButton("Guardar")
        self.layout.addWidget(self.save_button)

        # Add actions
        self.save_button.clicked.connect(self.save_data)
    
    def save_data(self):
        thread_safe_db = Database()

        # Save a new 'clinica' to the database
        clinica = Clinica(
            letra=self.letra_lineedit.text(),
            nombre=self.nombre_lineedit.text()
        )

        try:
            thread_safe_db.session.add(clinica)
            thread_safe_db.session.flush()
            thread_safe_db.session.commit()
            thread_safe_db.session.close()
            self.upper.load_data()
            self.upper.order_data()
            self.close()
        except Exception as e:
            print("Commit failed: ", e)
            thread_safe_db.session.rollback()

