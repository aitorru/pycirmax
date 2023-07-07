from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QLineEdit, QApplication, QHBoxLayout, QVBoxLayout, QGridLayout, QMessageBox
from PyQt5.QtCore import Qt
import bcrypt
from sqlalchemy import inspect

from db.db import User, Database

class ChangeKey(QWidget):
    def __init__(self, user: User):
        super().__init__()
        self.user = user
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("Cambio de clave")

        # Center the window on the screen
        width = 400
        height = 300

        screen_geometry = QApplication.desktop().screenGeometry()
        x = (screen_geometry.width() - width) / 2
        y = (screen_geometry.height() - height) / 2

        self.setGeometry(int(x), int(y), width, height)

        # Create a 2 column layout for the form and add widgets to it
        self.layout = QVBoxLayout() # type: ignore
        
        self.grid_layout = QGridLayout()
        
        self.codigo_edit = QLineEdit()
        self.codigo_edit.setText(str(self.user.code))
        self.codigo_edit.setDisabled(True)
        self.nombre_edit = QLineEdit()
        self.nombre_edit.setText(str(self.user.name))
        self.clave_edit = QLineEdit()
        self.clave_edit.setEchoMode(QLineEdit.Password)
        self.confirmar_clave_edit = QLineEdit()
        self.confirmar_clave_edit.setEchoMode(QLineEdit.Password)
        
        self.grid_layout.addWidget(QLabel('Codigo:'), 0, 0)
        self.grid_layout.addWidget(self.codigo_edit, 0, 1)
        
        self.grid_layout.addWidget(QLabel('Nombre:'), 1, 0)
        self.grid_layout.addWidget(self.nombre_edit, 1, 1)
        
        self.grid_layout.addWidget(QLabel('Clave:'), 2, 0)
        self.grid_layout.addWidget(self.clave_edit, 2, 1)
        
        self.grid_layout.addWidget(QLabel('Confirmar Clave:'), 3, 0)
        self.grid_layout.addWidget(self.confirmar_clave_edit, 3, 1)

        self.button_layout = QHBoxLayout()
        self.aceptar_button = QPushButton("Aceptar")
        self.cancelar_button = QPushButton("Cancelar")

        self.button_layout.addWidget(self.aceptar_button)
        self.aceptar_button.clicked.connect(self.change_credentials)
        self.button_layout.addWidget(self.cancelar_button)
        self.cancelar_button.clicked.connect(self.close)

        self.layout.addLayout(self.grid_layout)
        self.layout.addLayout(self.button_layout)
        self.setLayout(self.layout)

    def detect_empty_fields(self):
        if self.lineEditUsername.text() == '' or self.lineEditPassword.text() == '':
            self.buttonAceptar.setEnabled(False)
        else:
            self.buttonAceptar.setEnabled(True)
    
    def change_credentials(self):
        db = Database()

        if self.clave_edit.text() != self.confirmar_clave_edit.text():
            QMessageBox.warning(self, "Error", "Las claves no coinciden")
            return
        
        # Generate hash with bcrypt
        hashed = bcrypt.hashpw(self.clave_edit.text().encode('utf-8'), bcrypt.gensalt())

        user = db.session.query(User).filter(User.id == self.user.id).first()

        if user is None:
            QMessageBox.warning(self, "Error", "Usuario no encontrado")
            return
        
        user.code = self.codigo_edit.text()
        user.name = self.nombre_edit.text()
        user.password = hashed.decode('utf-8')

        try:
            db.session.flush()
            db.session.commit()
            QMessageBox.information(self, "Exito", "Usuario actualizado")
            db.session.close()
        except Exception as e:
            print("Commit failed: ", e)
            db.session.rollback()
        self.close()

    def close(self):
        self.hide()
