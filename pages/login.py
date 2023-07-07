import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel, QLineEdit, QMessageBox, QApplication
from PyQt5.QtCore import Qt
import bcrypt

from db.db import User, db, usuario_activo
from pages.change_key import ChangeKey
from pages.primary import MainWindow

class LoginPage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Inicio de Sesión")
        layout = QVBoxLayout()

        # Center the window on the screen
        width = 400
        height = 300

        screen_geometry = QApplication.desktop().screenGeometry()
        x = (screen_geometry.width() - width) / 2
        y = (screen_geometry.height() - height) / 2

        self.setGeometry(int(x), int(y), width, height)

        self.labelUsername = QLabel("Usuario")
        self.lineEditUsername = QLineEdit()
        self.lineEditUsername.textChanged.connect(self.detect_empty_fields)

        self.labelPassword = QLabel("Clave")
        self.lineEditPassword = QLineEdit()
        self.lineEditPassword.setEchoMode(QLineEdit.Password)
        self.lineEditPassword.textChanged.connect(self.detect_empty_fields)

        self.buttonLogin = QPushButton("Aceptar")
        self.buttonLogin.clicked.connect(self.check_credentials)

        self.buttonExit = QPushButton("Salir")
        self.buttonExit.clicked.connect(self.close)

        self.change_key_button = QPushButton("Cambiar clave")
        self.change_key_button.clicked.connect(self.change_key)

        layout.addWidget(self.labelUsername)
        layout.addWidget(self.lineEditUsername)
        layout.addWidget(self.labelPassword)
        layout.addWidget(self.lineEditPassword)
        layout.addWidget(self.buttonLogin)
        layout.addWidget(self.buttonExit)
        layout.addWidget(self.change_key_button)

        self.setLayout(layout)

        # Disable by default
        self.buttonLogin.setEnabled(False)
        self.change_key_button.setEnabled(False)

    def check_credentials(self):
        username = self.lineEditUsername.text()

        # Password is empty as we dont need it
        user_to_check = User(code=username, password="")

        # Get all users in the db and check if the user exists
        users = db.session.query(User).where(User.code == user_to_check.code).all() # type: ignore
        if len(users) == 0:
            QMessageBox.warning(self, 'Error', 'Usuario no encontrado')
            return
        for user in users:
            if bcrypt.checkpw(bytes(self.lineEditPassword.text(), 'utf-8'), bytes(str(user.password), 'utf-8')):
                QMessageBox.information(self, 'Success', 'Contraseña correcta')
                usuario_activo.set_usuario_activo(user)
                self.hide()
                self.main_window = MainWindow()
                self.main_window.show()
            else:
                QMessageBox.warning(self, 'Error', 'Contraseña incorrecta')
    
    def keyPressEvent(self, event):
        if self.lineEditUsername.text() == '' or self.lineEditPassword.text() == '':
            return
        # If the user presses enter, check the credentials
        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            self.check_credentials()

    def change_key(self):
        if self.lineEditUsername.text() == '' or self.lineEditPassword.text() == '':
            return
        
        username = self.lineEditUsername.text()

        # Password is empty as we dont need it
        user_to_check = User(code=username, password="")

        # Get all users in the db and check if the user exists
        users = db.session.query(User).where(User.code == user_to_check.code).all() # type: ignore
        if len(users) == 0:
            QMessageBox.warning(self, 'Error', 'Usuario no encontrado')
            return
        for user in users:
            if bcrypt.checkpw(bytes(self.lineEditPassword.text(), 'utf-8'), bytes(str(user.password), 'utf-8')):
                self.main_window = ChangeKey(user)
                self.main_window.show()
            else:
                QMessageBox.warning(self, 'Error', 'Contraseña incorrecta')


        

    def detect_empty_fields(self):
        if self.lineEditUsername.text() == '' or self.lineEditPassword.text() == '':
            self.buttonLogin.setEnabled(False)
            self.change_key_button.setEnabled(False)
        else:
            self.buttonLogin.setEnabled(True)
            self.change_key_button.setEnabled(True)
    
    def close(self):
        sys.exit()