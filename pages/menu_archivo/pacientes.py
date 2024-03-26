from PyQt5.QtWidgets import QWidget, QApplication, QHBoxLayout, QPushButton, QVBoxLayout, QFrame, QLabel, QLineEdit, QMessageBox, QGroupBox, QRadioButton, QTableWidget, QTableWidgetItem

from db.db import db, Paciente, Database
from utils.utils import open_file, draw_pdf_header

class PacientePage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.initUI()
        self.load_data()
    
    def initUI(self):
        self.setWindowTitle("Pacientes")

        # Center the window on the screen
        width = 700
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
        self.codigo_radio = QRadioButton("Codigo")
        self.codigo_radio.setChecked(True)
        self.nombre_radio = QRadioButton("Nombre")
        self.orden_groupbox_layout.addWidget(self.codigo_radio)
        self.orden_groupbox_layout.addWidget(self.nombre_radio)
        
        # If the user clicks on the 'codigo' radio button, order the data by 'codigo'
        # If the user clicks on the 'nombre' radio button, order the data by 'nombre'
        self.codigo_radio.clicked.connect(self.order_data)
        self.nombre_radio.clicked.connect(self.order_data)


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
        self.edit_button.clicked.connect(self.edit_paciente)

        # Create a table
        self.bottom_table = QTableWidget()
        self.layout.addWidget(self.bottom_table)

        self.bottom_frame = QFrame()
        self.bottom_frame_layout = QHBoxLayout()
        self.bottom_frame.setLayout(self.bottom_frame_layout)

        self.add_button = QPushButton("Añadir")
        self.bottom_frame_layout.addWidget(self.add_button)
        self.add_button.clicked.connect(self.add_paciente)

        self.delete_button = QPushButton("Eliminar")
        self.bottom_frame_layout.addWidget(self.delete_button)
        self.delete_button.clicked.connect(self.delete_paciente)

        self.layout.addWidget(self.bottom_frame)
    
    def close(self):
        return super().close()

    def listar_data(self):
        from fpdf import FPDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Arial', 'B', 11)
        draw_pdf_header(pdf)
        pdf.set_xy(30, 25)
        pdf.cell(10, 10, 'Codigo')
        pdf.line(30, 33, 86, 33)
        pdf.set_xy(60, 25)
        pdf.cell(10, 10, 'Nombre')
        pdf.line(60, 33, 117, 33)
        pdf.set_xy(90, 25)
        pdf.cell(10, 10, 'Domicilio')
        pdf.line(90, 33, 146, 33)
        pdf.set_xy(120, 25)
        pdf.cell(10, 10, 'C. Postal')
        pdf.line(120, 33, 176, 33)
        pdf.set_xy(150, 25)
        pdf.cell(10, 10, 'Poblacion')
        pdf.line(150, 33, 200, 33)
        for i, paciente in enumerate(self.pacientes_data):
            pdf.set_xy(30, 30 + (i * 4))
            pdf.cell(10, 13, f'{paciente.codigo}')
            pdf.set_xy(60, 30 + (i * 4))
            pdf.cell(10, 13, f'{paciente.nombre}')
            pdf.set_xy(90, 30 + (i * 4))
            pdf.cell(10, 13, f'{paciente.domicilio}')
            pdf.set_xy(120, 30 + (i * 4))
            pdf.cell(10, 13, f'{paciente.cp}')
            pdf.set_xy(150, 30 + (i * 4))
            pdf.cell(10, 13, f'{paciente.poblacion}')

        pdf.line(10, 30 + (len(self.pacientes_data) * 4) + 10, 200, 30 + (len(self.pacientes_data) * 4) + 10)

        pdf.set_xy(10, 30 + (len(self.pacientes_data) * 4) + 10)
        pdf.cell(10, 10, f'Total: {len(self.pacientes_data)}')

        pdf.line(10, 30 + (len(self.pacientes_data) * 4) + 20, 200, 30 + (len(self.pacientes_data) * 4) + 20)

        try:
            pdf.output('pacientes.pdf', 'F')
            QMessageBox.information(self, "Listado", "Listado generado correctamente")
            open_file('pacientes.pdf')
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al generar el listado: {e}")
        
    def order_data(self):
        if self.codigo_radio.isChecked():
            self.pacientes_data = sorted(self.pacientes_data, key=lambda x: x.codigo) # type: ignore
        elif self.nombre_radio.isChecked():
            self.pacientes_data = sorted(self.pacientes_data, key=lambda x: x.nombre) # type: ignore
        else:
            print("Error: No radio button is checked")
        
        self.bottom_table.clearContents()
        self.bottom_table.setRowCount(len(self.pacientes_data))
        self.bottom_table.setColumnCount(5)

        self.bottom_table.setHorizontalHeaderLabels(["Codigo", "Nombre"])

        for i, paciente in enumerate(self.pacientes_data):
            self.bottom_table.setItem(i, 0, QTableWidgetItem(paciente.codigo)) # type: ignore
            self.bottom_table.setItem(i, 1, QTableWidgetItem(paciente.nombre)) # type: ignore
            self.bottom_table.setItem(i, 2, QTableWidgetItem(paciente.domicilio)) # type: ignore
            self.bottom_table.setItem(i, 3, QTableWidgetItem(paciente.cp)) # type: ignore
            self.bottom_table.setItem(i, 4, QTableWidgetItem(paciente.poblacion)) # type: ignore




    def load_data(self):
        self.pacientes_data = db.session.query(Paciente).order_by(Paciente.codigo).all()

        self.bottom_table.setRowCount(len(self.pacientes_data))
        self.bottom_table.setColumnCount(5)

        self.bottom_table.setHorizontalHeaderLabels(["Código", "Nombre", "Domicilio", "C. Postal", "Poblacion"])

        for i, paciente in enumerate(self.pacientes_data):
            self.bottom_table.setItem(i, 0, QTableWidgetItem(paciente.codigo)) # type: ignore
            self.bottom_table.setItem(i, 1, QTableWidgetItem(paciente.nombre)) # type: ignore
            self.bottom_table.setItem(i, 2, QTableWidgetItem(paciente.domicilio)) # type: ignore
            self.bottom_table.setItem(i, 3, QTableWidgetItem(paciente.cp)) # type: ignore
            self.bottom_table.setItem(i, 4, QTableWidgetItem(paciente.poblacion)) # type: ignore
    
    def edit_paciente(self):
        paciente = self.pacientes_data[self.bottom_table.currentRow()]

        self.edit_paciente = EditPaciente(paciente, self)
        self.edit_paciente.show()
    
    def add_paciente(self):
        self.add_paciente = AddPaciente(self)
        self.add_paciente.show()

    def delete_paciente(self):

        # Create a confirm dialog
        confirm = QMessageBox()
        confirm.setWindowTitle("Eliminar")
        confirm.setText(f"¿Estás seguro de que quieres eliminar el paciente {self.pacientes_data[self.bottom_table.currentRow()].nombre}?")

        confirm.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        confirm.setDefaultButton(QMessageBox.No)

        # If the user confirms, delete the clinica
        if confirm.exec_() == QMessageBox.No:
            return

        paciente = self.pacientes_data[self.bottom_table.currentRow()]

        thread_safe_db = Database()

        # Query the database for the clinica
        paciente = thread_safe_db.session.query(Paciente).filter_by(id=paciente.id).first()

        # Delete the clinica
        try:
            thread_safe_db.session.delete(paciente)
            thread_safe_db.session.flush()
            thread_safe_db.session.commit()
            thread_safe_db.session.close()
        except Exception as e:
            print("Commit failed: ", e)
            thread_safe_db.session.rollback()
        self.load_data()
        self.order_data()

        
class EditPaciente(QWidget):
    def __init__(self, paciente: Paciente, upper) -> None:
        super().__init__()
        self.paciente = paciente
        self.upper = upper
        self.initUI()
    
    def initUI(self):
        self.layout = QHBoxLayout() # type: ignore
        self.setLayout(self.layout)

        self.setWindowTitle("Editar Referidor")

        # Center the window on the screen
        width = 800
        height = 50

        screen_geometry = QApplication.desktop().screenGeometry() # type: ignore
        x = (screen_geometry.width() - width) / 2
        y = (screen_geometry.height() - height) / 2

        self.setGeometry(int(x), int(y), width, height)

        # Create a label and a line edit for 'letra; and 'nombre'
        self.codigo_label = QLabel("Código")
        self.codigo_lineedit = QLineEdit()
        
        self.nombre_label = QLabel("Nombre")
        self.nombre_lineedit = QLineEdit()

        self.domicilio_label = QLabel("Domicilio")
        self.domicilio_lineedit = QLineEdit()

        self.cp_label = QLabel("Código Postal")
        self.cp_lineedit = QLineEdit()

        self.poblacion_label = QLabel("Población")
        self.poblacion_lineedit = QLineEdit()

        self.codigo_lineedit.setText(self.paciente.codigo) # type: ignore
        self.nombre_lineedit.setText(self.paciente.nombre) # type: ignore
        self.domicilio_lineedit.setText(self.paciente.domicilio) # type: ignore
        self.cp_lineedit.setText(self.paciente.cp) # type: ignore
        self.poblacion_lineedit.setText(self.paciente.poblacion) # type: ignore

        self.layout.addWidget(self.codigo_label)
        self.layout.addWidget(self.codigo_lineedit)
        self.layout.addWidget(self.nombre_label)
        self.layout.addWidget(self.nombre_lineedit)
        self.layout.addWidget(self.domicilio_label)
        self.layout.addWidget(self.domicilio_lineedit)
        self.layout.addWidget(self.cp_label)
        self.layout.addWidget(self.cp_lineedit)
        self.layout.addWidget(self.poblacion_label)
        self.layout.addWidget(self.poblacion_lineedit)

        # Create a button 'Guardar'
        self.save_button = QPushButton("Guardar")
        self.layout.addWidget(self.save_button)

        # Add actions
        self.save_button.clicked.connect(self.save_data)
    
    def save_data(self):
        thread_safe_db = Database()

        referidor_from_db = thread_safe_db.session.query(Paciente).filter_by(id=self.paciente.id).first() # type: ignore

        if referidor_from_db is None:
            QMessageBox.critical(self, "Error", "No se ha encontrado el referidor")
            return

        referidor_from_db.codigo = self.codigo_lineedit.text() # type: ignore
        referidor_from_db.nombre = self.nombre_lineedit.text() # type: ignore
        referidor_from_db.domicilio = self.domicilio_lineedit.text() # type: ignore
        referidor_from_db.cp = self.cp_lineedit.text() # type: ignore
        referidor_from_db.poblacion = self.poblacion_lineedit.text() # type: ignore

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
            



class AddPaciente(QWidget):
    def __init__(self,  upper) -> None:
        super().__init__()
        self.upper = upper
        self.initUI()
    
    def initUI(self):
        self.layout = QHBoxLayout() # type: ignore
        self.setLayout(self.layout)

        self.setWindowTitle("Añadir referidor")

        # Center the window on the screen
        width = 800
        height = 50

        screen_geometry = QApplication.desktop().screenGeometry() # type: ignore
        x = (screen_geometry.width() - width) / 2
        y = (screen_geometry.height() - height) / 2

        self.setGeometry(int(x), int(y), width, height)

        # Create a label and a line edit for 'letra; and 'nombre'
        self.letra_label = QLabel("Código")
        self.letra_lineedit = QLineEdit()
        
        self.nombre_label = QLabel("Nombre")
        self.nombre_lineedit = QLineEdit()

        self.domicilio_label = QLabel("Domicilio")
        self.domicilio_lineedit = QLineEdit()

        self.cp_label = QLabel("Código Postal")
        self.cp_lineedit = QLineEdit()

        self.poblacion_label = QLabel("Población")
        self.poblacion_lineedit = QLineEdit()

        self.layout.addWidget(self.letra_label)
        self.layout.addWidget(self.letra_lineedit)
        self.layout.addWidget(self.nombre_label)
        self.layout.addWidget(self.nombre_lineedit)
        self.layout.addWidget(self.domicilio_label)
        self.layout.addWidget(self.domicilio_lineedit)
        self.layout.addWidget(self.cp_label)
        self.layout.addWidget(self.cp_lineedit)
        self.layout.addWidget(self.poblacion_label)
        self.layout.addWidget(self.poblacion_lineedit)

        # Create a button 'Guardar'
        self.save_button = QPushButton("Guardar")
        self.layout.addWidget(self.save_button)

        # Add actions
        self.save_button.clicked.connect(self.save_data)
    
    def save_data(self):
        thread_safe_db = Database()

        # Save a new 'sociedad' to the database
        paciente = Paciente(
            codigo=self.letra_lineedit.text(),
            nombre=self.nombre_lineedit.text(),
            domicilio=self.domicilio_lineedit.text(),
            cp=self.cp_lineedit.text(),
            poblacion=self.poblacion_lineedit.text()
        )

        try:
            thread_safe_db.session.add(paciente)
            thread_safe_db.session.flush()
            thread_safe_db.session.commit()
            thread_safe_db.session.close()
            self.upper.load_data()
            self.upper.order_data()
            self.close()
        except Exception as e:
            print("Commit failed: ", e)
            thread_safe_db.session.rollback()

