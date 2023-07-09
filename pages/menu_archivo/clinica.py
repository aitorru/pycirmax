from PyQt5.QtWidgets import QWidget, QApplication, QHBoxLayout, QPushButton, QTabWidget, QVBoxLayout, QFrame, QTabBar, QFormLayout, QLabel, QLineEdit, QTextEdit, QMessageBox, QGroupBox, QRadioButton, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import QSize

from db.db import db, Clinica, config

class ClinicaPage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.initUI()
        self.load_data()
    
    def initUI(self):
        self.setWindowTitle("Clinica")

        # Center the window on the screen
        width = 300
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
        self.nombre_radio = QRadioButton("Nombre")
        self.orden_groupbox_layout.addWidget(self.codigo_radio)
        self.orden_groupbox_layout.addWidget(self.nombre_radio)


        # Create two buttons 'Edicion' and 'Salir'
        self.edicion_button = QPushButton("Guardar")
        self.salir_button = QPushButton("Salir")
        self.top_frame_layout.addStretch(1)
        self.top_frame_layout.addWidget(self.edicion_button)
        self.top_frame_layout.addWidget(self.salir_button)

        # Add actions
        self.edicion_button.clicked.connect(self.save_data)
        self.salir_button.clicked.connect(self.close) # type: ignore

        # Create a table
        self.bottom_table = QTableWidget()
        self.layout.addWidget(self.bottom_table)
    
    def close(self):
        return super().close()

    def save_data(self):

        to_insert_data = self.clinicas_data[self.bottom_table.currentRow()]

        import toml
        config['config']['clinica_id'] = to_insert_data.id

        # Save the config file
        with open('config.toml', 'w') as f:
            toml.dump(config, f)



    def load_data(self):
        self.clinicas_data = db.session.query(Clinica).order_by(Clinica.letra).all()

        self.bottom_table.setRowCount(len(self.clinicas_data))
        self.bottom_table.setColumnCount(2)

        self.bottom_table.setHorizontalHeaderLabels(["Codigo", "Nombre"])

        for i, clinica in enumerate(self.clinicas_data):
            self.bottom_table.setItem(i, 0, QTableWidgetItem(clinica.letra)) # type: ignore
            self.bottom_table.setItem(i, 1, QTableWidgetItem(clinica.nombre)) # type: ignore
        