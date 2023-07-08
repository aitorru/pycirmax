from PyQt5.QtWidgets import QWidget, QApplication, QHBoxLayout, QPushButton, QTabWidget, QVBoxLayout, QFrame, QTabBar, QFormLayout, QLabel, QLineEdit, QTextEdit, QMessageBox
from PyQt5.QtCore import QSize

from db.db import config, db, Empresa, Database, Presupuesto

class ConfigPage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Configuración")

        # Load classes first
        self.empresa = EmpresaPage()
        self.presupuestos = PresupuestosPage()

        # Center the window on the screen
        width = 1000
        height = 800

        screen_geometry = QApplication.desktop().screenGeometry()
        x = (screen_geometry.width() - width) / 2
        y = (screen_geometry.height() - height) / 2

        self.setGeometry(int(x), int(y), width, height)

        # Create a down layout for the form and add widgets to it
        self.layout = QVBoxLayout() # type: ignore

        # Create the following buttons 'Editar' 'Validar' 'Cancelar' 'Salir'
        # and add them to the layout
        
        # Create a horizontal layout for the buttons
        self.button_frame = QFrame()
        self.button_frame_layout = QHBoxLayout()

        self.editar_button = QPushButton("Editar")
        self.editar_button.clicked.connect(self.allow_editing)
        self.validar_button = QPushButton("Validar")
        self.validar_button.setDisabled(True)
        self.validar_button.clicked.connect(self.save_data)
        self.cancelar_button = QPushButton("Cancelar")
        self.cancelar_button.setDisabled(True)
        self.cancelar_button.clicked.connect(self.disable_editing)
        self.salir_button = QPushButton("Salir")
        self.salir_button.clicked.connect(self.hide)

        self.button_frame_layout.addWidget(self.editar_button)
        self.button_frame_layout.addStretch(1)
        self.button_frame_layout.addWidget(self.validar_button)
        self.button_frame_layout.addWidget(self.cancelar_button)
        self.button_frame_layout.addWidget(self.salir_button)

        self.button_frame.setLayout(self.button_frame_layout)

        self.setLayout(self.layout)

        # Now create QTabWidget and add the entries 'Empresa' 'Presupuestos' and 'Facturas'
        # to it. Then add the QTabWidget to the layout
        self.tab_widget = QTabWidget()\
        # TODO: This does not work
        # self.tab_widget.setTabBar(CustomTabBar())  # Use the custom tab bar
        self.tab_widget.addTab(self.empresa, "Empresa")
        self.tab_widget.addTab(self.presupuestos, "Presupuestos")
        self.tab_widget.addTab(FacturasPage(), "Facturas")

        self.layout.addWidget(self.button_frame)
        self.layout.addWidget(self.tab_widget)
    
    def allow_editing(self):
        self.editar_button.setEnabled(False)
        self.validar_button.setEnabled(True)
        self.cancelar_button.setEnabled(True)
        self.salir_button.setEnabled(False)

        # TODO: Add the rest
        self.empresa.enable_all_fields()
        self.presupuestos.enable_all_fields()
    
    def disable_editing(self):
        # TODO: Add the rest
        self.editar_button.setEnabled(True)
        self.validar_button.setEnabled(False)
        self.cancelar_button.setEnabled(False)
        self.salir_button.setEnabled(True)

        self.empresa.load_data()
        self.presupuestos.load_data()
        self.empresa.disable_all_fields()
        self.presupuestos.disable_all_fields()
    
    def save_data(self):
        # TODO: Add the rest
        self.empresa.save_data()
        self.presupuestos.save_data()

        self.disable_editing()

        QMessageBox.information(self, "Exito", "Configuración guardada con éxito")


class EmpresaPage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.initUI()
        self.load_data()
        self.disable_all_fields()

    def initUI(self):
        self.layout = QFormLayout() # type: ignore
        self.setLayout(self.layout)

        self.nif_label = QLabel("N.I.F.")
        self.nif_edit = QLineEdit()

        self.layout.addRow(self.nif_label, self.nif_edit)

        self.razon_social_label = QLabel("Razón Social")
        self.razon_social_edit = QLineEdit()

        self.layout.addRow(self.razon_social_label, self.razon_social_edit)

        self.domicilio_label = QLabel("Domicilio")
        self.domicilio_edit = QLineEdit()

        self.layout.addRow(self.domicilio_label, self.domicilio_edit)

        self.codigo_postal_label = QLabel("Código Postal")
        self.codigo_postal_edit = QLineEdit()

        self.layout.addRow(self.codigo_postal_label, self.codigo_postal_edit)

        self.poblacion_label = QLabel("Población")
        self.poblacion_edit = QLineEdit()

        self.layout.addRow(self.poblacion_label, self.poblacion_edit)

        self.provincia_label = QLabel("Provincia")
        self.provincia_edit = QLineEdit()

        self.layout.addRow(self.provincia_label, self.provincia_edit)

        self.telefono_label = QLabel("Teléfono")
        self.telefono_edit = QLineEdit()

        self.layout.addRow(self.telefono_label, self.telefono_edit)

        self.fax_label = QLabel("Fax")
        self.fax_edit = QLineEdit()

        self.layout.addRow(self.fax_label, self.fax_edit)

        self.coletilla_gdpr_label = QLabel("Coletilla GDPR")
        self.coletilla_gdpr_edit = QTextEdit()

        self.layout.addRow(self.coletilla_gdpr_label, self.coletilla_gdpr_edit)

    def load_data(self):
        # Pull the clinica from the db
        self.config_from_db = db.session.query(Empresa).where(Empresa.clinica_id == config['config']['clinica_id']).first()

        if self.config_from_db == None:
            QMessageBox.critical(self, "Error", "No se ha encontrado la clínica en la base de datos. Existe el fichero config.toml? Existe la clínica en la base de datos?Existe clinica_id en el fichero?")
            return
        
        # Fill the form with the data
        self.nif_edit.setText(self.config_from_db.nif) # type: ignore
        self.razon_social_edit.setText(self.config_from_db.razon_social) # type: ignore
        self.domicilio_edit.setText(self.config_from_db.domicilio) # type: ignore
        self.codigo_postal_edit.setText(self.config_from_db.codigo_postal) # type: ignore
        self.poblacion_edit.setText(self.config_from_db.poblacion) # type: ignore
        self.provincia_edit.setText(self.config_from_db.provincia) # type: ignore
        self.telefono_edit.setText(self.config_from_db.telefono) # type: ignore
        self.fax_edit.setText(self.config_from_db.fax) # type: ignore
        self.coletilla_gdpr_edit.setText(self.config_from_db.coletilla_gdpr) # type: ignore
    
    def disable_all_fields(self):
        self.nif_edit.setEnabled(False)
        self.razon_social_edit.setEnabled(False)
        self.domicilio_edit.setEnabled(False)
        self.codigo_postal_edit.setEnabled(False)
        self.poblacion_edit.setEnabled(False)
        self.provincia_edit.setEnabled(False)
        self.telefono_edit.setEnabled(False)
        self.fax_edit.setEnabled(False)
        self.coletilla_gdpr_edit.setEnabled(False)
    
    def enable_all_fields(self):
        self.nif_edit.setEnabled(True)
        self.razon_social_edit.setEnabled(True)
        self.domicilio_edit.setEnabled(True)
        self.codigo_postal_edit.setEnabled(True)
        self.poblacion_edit.setEnabled(True)
        self.provincia_edit.setEnabled(True)
        self.telefono_edit.setEnabled(True)
        self.fax_edit.setEnabled(True)
        self.coletilla_gdpr_edit.setEnabled(True)

    def save_data(self):
        thread_safe_db = Database()

        config_db = thread_safe_db.session.query(Empresa).where(Empresa.clinica_id == config['config']['clinica_id']).first()

        if config_db == None:
            QMessageBox.critical(self, "Error", "No se ha encontrado la clínica en la base de datos. Existe el fichero config.toml? Existe la clínica en la base de datos?Existe clinica_id en el fichero?")
            return
        
        config_db.nif = self.nif_edit.text() # type: ignore
        config_db.razon_social = self.razon_social_edit.text() # type: ignore
        config_db.domicilio = self.domicilio_edit.text() # type: ignore
        config_db.codigo_postal = self.codigo_postal_edit.text() # type: ignore
        config_db.poblacion = self.poblacion_edit.text() # type: ignore
        config_db.provincia = self.provincia_edit.text() # type: ignore
        config_db.telefono = self.telefono_edit.text() # type: ignore
        config_db.fax = self.fax_edit.text() # type: ignore
        config_db.coletilla_gdpr = self.coletilla_gdpr_edit.toPlainText() # type: ignore

        
        try:
            thread_safe_db.session.flush()
            thread_safe_db.session.commit()
            thread_safe_db.session.close()
        except Exception as e:
            print("Commit failed: ", e)
            thread_safe_db.session.rollback()


class PresupuestosPage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.initUI()
        self.load_data()
        self.disable_all_fields()

    def initUI(self):
        self.layout = QFormLayout() # type: ignore
        self.setLayout(self.layout)

        self.encabezamiento_label = QLabel("Encabezamiento")
        self.encabezamiento_edit = QTextEdit()

        self.layout.addRow(self.encabezamiento_label, self.encabezamiento_edit)

        self.pie_de_firma_label = QLabel("Pie de firma")
        self.pie_de_firma_edit = QLineEdit()

        self.layout.addRow(self.pie_de_firma_label, self.pie_de_firma_edit)

        self.coletilla_forma_de_pago_label = QLabel("Coletilla forma de pago")
        self.coletilla_forma_de_pago_edit = QTextEdit()

        self.layout.addRow(self.coletilla_forma_de_pago_label, self.coletilla_forma_de_pago_edit)
    
    def disable_all_fields(self):
        self.encabezamiento_edit.setEnabled(False)
        self.pie_de_firma_edit.setEnabled(False)
        self.coletilla_forma_de_pago_edit.setEnabled(False)
    
    def enable_all_fields(self):
        self.encabezamiento_edit.setEnabled(True)
        self.pie_de_firma_edit.setEnabled(True)
        self.coletilla_forma_de_pago_edit.setEnabled(True)

    def load_data(self):
        thread_safe_db = Database()
        presupuesto_from_db = thread_safe_db.session.query(Presupuesto).where(Presupuesto.clinica_id == config['config']['clinica_id']).first()

        if presupuesto_from_db == None:
            QMessageBox.critical(self, "Error", "No se ha encontrado la clínica en la base de datos. Existe el fichero config.toml? Existe la clínica en la base de datos?Existe clinica_id en el fichero?")
            return
        
        self.encabezamiento_edit.setText(presupuesto_from_db.encabezamiento) # type: ignore
        self.pie_de_firma_edit.setText(presupuesto_from_db.pie) # type: ignore
        self.coletilla_forma_de_pago_edit.setText(presupuesto_from_db.forma_de_pago) # type: ignore

    def save_data(self):
        thread_safe_db = Database()

        presupuesto_db = thread_safe_db.session.query(Presupuesto).where(Presupuesto.clinica_id == config['config']['clinica_id']).first()

        if presupuesto_db == None:
            QMessageBox.critical(self, "Error", "No se ha encontrado la clínica en la base de datos. Existe el fichero config.toml? Existe la clínica en la base de datos?Existe clinica_id en el fichero?")
            return
        
        presupuesto_db.encabezamiento = self.encabezamiento_edit.toPlainText() # type: ignore
        presupuesto_db.pie = self.pie_de_firma_edit.text() # type: ignore
        presupuesto_db.forma_de_pago = self.coletilla_forma_de_pago_edit.toPlainText() # type: ignore


        try:
            thread_safe_db.session.flush()
            thread_safe_db.session.commit()
            thread_safe_db.session.close()
        except Exception as e:
            print("Commit failed: ", e)
            thread_safe_db.session.rollback()
        



class FacturasPage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout() # type: ignore
        self.setLayout(self.layout)

        self.layout.addWidget(QPushButton("Facturas"))


class CustomTabBar(QTabBar):
    def tabSizeHint(self, index):
        size = super().tabSizeHint(index)
        width = self.width() // self.count()  # Divide the total width by the number of tabs
        return QSize(width, size.height())  # Return a size with the calculated width and original height