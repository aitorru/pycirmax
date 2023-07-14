from typing import List
from PyQt5.QtWidgets import QWidget, QApplication, QHBoxLayout, QPushButton, QTabWidget, QVBoxLayout, QFrame, QTabBar, QFormLayout, QLabel, QLineEdit, QTextEdit, QMessageBox, QGroupBox, QRadioButton, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import QSize

from db.db import db, Sociedad, config, Database
from utils.utils import open_file

class SociedadPage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.initUI()
        self.load_data()
    
    def initUI(self):
        self.setWindowTitle("Sociedades")

        # Center the window on the screen
        width = 500
        height = 500

        screen_geometry = QApplication.desktop().screenGeometry()
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
        self.codigo_radio = QRadioButton("Codigo")
        self.codigo_radio.setChecked(True)
        self.nombre_radio = QRadioButton("Nombre")
        self.orden_groupbox_layout.addWidget(self.codigo_radio)
        self.orden_groupbox_layout.addWidget(self.nombre_radio)


        # Create two buttons 'Edicion' and 'Salir'
        self.edit_button = QPushButton("Editar")
        self.listar_button = QPushButton("Listar")
        self.salir_button = QPushButton("Salir")
        self.top_frame_layout.addStretch(1)
        self.top_frame_layout.addWidget(self.edit_button)
        self.top_frame_layout.addWidget(self.listar_button)
        self.top_frame_layout.addWidget(self.salir_button)



        # Add actions
        self.listar_button.clicked.connect(self.listar_data)
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

    def listar_data(self):
        from fpdf import FPDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Arial', 'B', 11)
        pdf.line(10, 10, 200, 10)
        pdf.line(10, 11, 200, 11)
        pdf.cell(10, 10, 'Listado de sociades')
        import datetime
        current_date = datetime.datetime.now()
        pdf.set_xy(150, 10)
        pdf.cell(10, 10, f'Fecha: {current_date.day}/{current_date.month}/{current_date.year}')
        pdf.line(10, 18, 200, 18)
        pdf.set_xy(70, 25)
        pdf.cell(10, 10, 'Codigo')
        pdf.line(70, 33, 86, 33)
        pdf.set_xy(100, 25)
        pdf.cell(10, 10, 'Nombre')
        pdf.line(100, 33, 117, 33)
        for i, sociedad in enumerate(self.sociedades_data):
            pdf.set_xy(70, 30 + (i * 4))
            pdf.cell(10, 13, f'{sociedad.codigo}')
            pdf.set_xy(100, 30 + (i * 4))
            pdf.cell(10, 13, f'{sociedad.nombre}')

        pdf.line(10, 30 + (len(self.sociedades_data) * 4) + 10, 200, 30 + (len(self.sociedades_data) * 4) + 10)

        pdf.set_xy(10, 30 + (len(self.sociedades_data) * 4) + 10)
        pdf.cell(10, 10, f'Total: {len(self.sociedades_data)}')

        pdf.line(10, 30 + (len(self.sociedades_data) * 4) + 20, 200, 30 + (len(self.sociedades_data) * 4) + 20)

        try:
            pdf.output('sociedades.pdf', 'F')
            QMessageBox.information(self, "Listado", "Listado generado correctamente")
            open_file('sociedades.pdf')
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al generar el listado: {e}")
        
    def order_data(self):
        if self.codigo_radio.isChecked():
            self.sociedades_data = sorted(self.sociedades_data, key=lambda x: x.codigo) # type: ignore
        elif self.nombre_radio.isChecked():
            self.sociedades_data = sorted(self.sociedades_data, key=lambda x: x.nombre) # type: ignore
        
        self.bottom_table.clearContents()
        self.bottom_table.setRowCount(len(self.sociedades_data))
        self.bottom_table.setColumnCount(2)

        self.bottom_table.setHorizontalHeaderLabels(["Codigo", "Nombre"])

        for i, sociedad in enumerate(self.sociedades_data):
            self.bottom_table.setItem(i, 0, QTableWidgetItem(sociedad.codigo)) # type: ignore
            self.bottom_table.setItem(i, 1, QTableWidgetItem(sociedad.nombre)) # type: ignore




    def load_data(self):
        self.sociedades_data = db.session.query(Sociedad).order_by(Sociedad.codigo).all()

        self.bottom_table.setRowCount(len(self.sociedades_data))
        self.bottom_table.setColumnCount(2)

        self.bottom_table.setHorizontalHeaderLabels(["Código", "Nombre"])

        for i, sociedad in enumerate(self.sociedades_data):
            self.bottom_table.setItem(i, 0, QTableWidgetItem(sociedad.codigo)) # type: ignore
            self.bottom_table.setItem(i, 1, QTableWidgetItem(sociedad.nombre)) # type: ignore
    
    def edit_clinica(self):
        clinica = self.sociedades_data[self.bottom_table.currentRow()]

        self.edit_clinica = EditClinica(clinica, self)
        self.edit_clinica.show()
    
    def add_clinica(self):
        self.add_clinica = AddClinica(self)
        self.add_clinica.show()

    def delete_clinica(self):

        # Create a confirm dialog
        confirm = QMessageBox()
        confirm.setWindowTitle("Eliminar")
        confirm.setText(f"¿Estás seguro de que quieres eliminar la sociedad {self.sociedades_data[self.bottom_table.currentRow()].nombre}?")

        confirm.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        confirm.setDefaultButton(QMessageBox.No)

        # If the user confirms, delete the clinica
        if confirm.exec_() == QMessageBox.No:
            return

        sociedad = self.sociedades_data[self.bottom_table.currentRow()]

        thread_safe_db = Database()

        # Query the database for the clinica
        sociedad = thread_safe_db.session.query(Sociedad).filter_by(id=sociedad.id).first()

        # Delete the clinica
        try:
            thread_safe_db.session.delete(sociedad)
            thread_safe_db.session.flush()
            thread_safe_db.session.commit()
            thread_safe_db.session.close()
        except Exception as e:
            print("Commit failed: ", e)
            thread_safe_db.session.rollback()
        self.load_data()
        self.order_data()

        
class EditClinica(QWidget):
    def __init__(self, sociedad: Sociedad, upper) -> None:
        super().__init__()
        self.sociedad = sociedad
        self.upper = upper
        self.initUI()
    
    def initUI(self):
        self.layout = QHBoxLayout() # type: ignore
        self.setLayout(self.layout)

        self.setWindowTitle("Editar Clinica")

        # Center the window on the screen
        width = 800
        height = 50

        screen_geometry = QApplication.desktop().screenGeometry()
        x = (screen_geometry.width() - width) / 2
        y = (screen_geometry.height() - height) / 2

        self.setGeometry(int(x), int(y), width, height)

        # Create a label and a line edit for 'letra; and 'nombre'
        self.codigo_label = QLabel("Código")
        self.codigo_lineedit = QLineEdit()
        
        self.nombre_label = QLabel("Nombre")
        self.nombre_lineedit = QLineEdit()

        self.codigo_lineedit.setText(self.sociedad.codigo) # type: ignore
        self.nombre_lineedit.setText(self.sociedad.nombre) # type: ignore

        self.layout.addWidget(self.codigo_label)
        self.layout.addWidget(self.codigo_lineedit)
        self.layout.addWidget(self.nombre_label)
        self.layout.addWidget(self.nombre_lineedit)

        # Create a button 'Guardar'
        self.save_button = QPushButton("Guardar")
        self.layout.addWidget(self.save_button)

        # Add actions
        self.save_button.clicked.connect(self.save_data)
    
    def save_data(self):
        thread_safe_db = Database()

        sociedad_from_db = thread_safe_db.session.query(Sociedad).filter_by(id=self.sociedad.id).first() # type: ignore

        if sociedad_from_db is None:
            QMessageBox.critical(self, "Error", "No se ha encontrado la sociedad")
            return

        sociedad_from_db.codigo = self.codigo_lineedit.text() # type: ignore
        sociedad_from_db.nombre = self.nombre_lineedit.text() # type: ignore

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

        screen_geometry = QApplication.desktop().screenGeometry()
        x = (screen_geometry.width() - width) / 2
        y = (screen_geometry.height() - height) / 2

        self.setGeometry(int(x), int(y), width, height)

        # Create a label and a line edit for 'letra; and 'nombre'
        self.letra_label = QLabel("Código")
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

        # Save a new 'sociedad' to the database
        sociedad = Sociedad(
            codigo=self.letra_lineedit.text(),
            nombre=self.nombre_lineedit.text()
        )

        try:
            thread_safe_db.session.add(sociedad)
            thread_safe_db.session.flush()
            thread_safe_db.session.commit()
            thread_safe_db.session.close()
            self.upper.load_data()
            self.upper.order_data()
            self.close()
        except Exception as e:
            print("Commit failed: ", e)
            thread_safe_db.session.rollback()

