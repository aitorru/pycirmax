from calendar import c
from PyQt5.QtWidgets import QWidget, QApplication, QHBoxLayout, QPushButton, QVBoxLayout, QFrame, QLabel, QLineEdit, QMessageBox, QGroupBox, QRadioButton, QTableWidget, QTableWidgetItem

from db.db import db, Concepto, Database
from utils.utils import open_file

class ConceptoPage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.initUI()
        self.load_data()
    
    def initUI(self):
        self.setWindowTitle("Conceptos")

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
        self.edit_button.clicked.connect(self.edit_concepto)

        # Create a table
        self.bottom_table = QTableWidget()
        self.layout.addWidget(self.bottom_table)

        self.bottom_frame = QFrame()
        self.bottom_frame_layout = QHBoxLayout()
        self.bottom_frame.setLayout(self.bottom_frame_layout)

        self.add_button = QPushButton("Añadir")
        self.bottom_frame_layout.addWidget(self.add_button)
        self.add_button.clicked.connect(self.add_concepto)

        self.delete_button = QPushButton("Eliminar")
        self.bottom_frame_layout.addWidget(self.delete_button)
        self.delete_button.clicked.connect(self.delete_concepto)

        self.layout.addWidget(self.bottom_frame)
    
    def close(self):
        return super().close()
      
    def edit_concepto(self):
        concepto = self.concepto_data[self.bottom_table.currentRow()]

        self.edit_concepto = EditConcepto(concepto, self)
        self.edit_concepto.show()

    def add_concepto(self):
        self.add_concepto = AddConcepto(self)
        self.add_concepto.show()

    def delete_concepto(self):

        # Create a confirm dialog
        confirm = QMessageBox()
        confirm.setWindowTitle("Eliminar")
        confirm.setText(f"¿Estás seguro de que quieres eliminar el concepto {self.pacientes_data[self.bottom_table.currentRow()].nombre}?")

        confirm.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        confirm.setDefaultButton(QMessageBox.No)

        # If the user confirms, delete the clinica
        if confirm.exec_() == QMessageBox.No:
            return

        concepto = self.add_concepto_data[self.bottom_table.currentRow()]
    
    def load_data(self):
        pass

    def order_data(self):
        pass

    def listar_data(self):
        pass
   
class EditConcepto(QWidget):
    def __init__(self, concepto: Concepto, upper) -> None:
        super().__init__()
        self.concepto = concepto
        self.upper = upper
        self.initUI()
    
    def initUI(self):
        self.layout = QHBoxLayout() # type: ignore
        self.setLayout(self.layout)

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

        self.precio_label = QLabel("Precio")
        self.precio_lineedit = QLineEdit()

        self.codigo_lineedit.setText(self.concepto.codigo) # type: ignore
        self.nombre_lineedit.setText(self.concepto.nombre) # type: ignore
        self.domicilio_lineedit.setText(self.concepto.precio) # type: ignore
     
        self.layout.addWidget(self.codigo_label)
        self.layout.addWidget(self.codigo_lineedit)
        self.layout.addWidget(self.nombre_label)
        self.layout.addWidget(self.nombre_lineedit)
        self.layout.addWidget(self.precio_label)
        self.layout.addWidget(self.precio_lineedit)

        # Create a button 'Guardar'
        self.save_button = QPushButton("Guardar")
        self.layout.addWidget(self.save_button)

        # Add actions
        self.save_button.clicked.connect(self.save_data)
    
    def save_data(self):
        thread_safe_db = Database()
  
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
            



class AddConcepto(QWidget):
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
        self.codigo_label = QLabel("Código")
        self.codigo_lineedit = QLineEdit()
        
        self.nombre_label = QLabel("Nombre")
        self.nombre_lineedit = QLineEdit()

        self.precio_label = QLabel("Precio")
        self.precio_lineedit = QLineEdit()

        self.layout.addWidget(self.codigo_label)
        self.layout.addWidget(self.codigo_lineedit)
        self.layout.addWidget(self.nombre_label)
        self.layout.addWidget(self.nombre_lineedit)
        self.layout.addWidget(self.precio_label)                       
        self.layout.addWidget(self.precio_lineedit)                       
 
        # Create a button 'Guardar'
        self.save_button = QPushButton("Guardar")
        self.layout.addWidget(self.save_button)

        # Add actions
        self.save_button.clicked.connect(self.save_data)
    
    def save_data(self):
        thread_safe_db = Database()

        concepto = Concepto(
            codigo=self.codigo_lineedit.text(),
            nombre=self.nombre_lineedit.text(),
            precio=self.precio_lineedit.text()
        )

        try:
            thread_safe_db.session.add(concepto)
            thread_safe_db.session.flush()
            thread_safe_db.session.commit()
            thread_safe_db.session.close()
            self.upper.load_data()
            self.upper.order_data()
            self.close()
        except Exception as e:
            print("Commit failed: ", e)
            thread_safe_db.session.rollback()

