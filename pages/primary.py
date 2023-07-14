import sys
from PyQt5.QtWidgets import QMainWindow, QAction, QMenu, QApplication
from db.db import usuario_activo



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Clínica de Cirugía Oral y Maxilofacial")
        
        # Center the window on the screen

        width = 800
        height = 600

        screen_geometry = QApplication.desktop().screenGeometry()
        x = (screen_geometry.width() - width) / 2
        y = (screen_geometry.height() - height) / 2

        self.setGeometry(int(x), int(y), width, height)

        # Create the status bar
        self.statusBar().showMessage(f'Usuario: {usuario_activo.get_nombre_usuario()}')
        

        # Create the top menu bar
        menubar = self.menuBar()

        archivos_menu = QMenu("Archivos", self)
        menubar.addMenu(archivos_menu)

        configuracion_action = QAction("Configuración", self)
        configuracion_action.triggered.connect(self.open_configuracion)
        archivos_menu.addAction(configuracion_action)
        archivos_menu.addSeparator()

        clinicas_action = QAction("Clínicas", self)
        clinicas_action.triggered.connect(self.open_clinicas)
        archivos_menu.addAction(clinicas_action)

        sociedades_action = QAction("Sociedades", self)
        sociedades_action.triggered.connect(self.open_sociedades)
        archivos_menu.addAction(sociedades_action)

        referidores_action = QAction("Referidores", self)
        archivos_menu.addAction(referidores_action)

        pacientes_action = QAction("Pacientes", self)
        archivos_menu.addAction(pacientes_action)

        conceptos_action = QAction("Conceptos", self)
        archivos_menu.addAction(conceptos_action)

        presupuestos_action = QAction("Presupuestos", self)
        archivos_menu.addAction(presupuestos_action)
        archivos_menu.addSeparator()

        cerrar_sesion_action = QAction("Cerrar Sesión", self)
        cerrar_sesion_action.triggered.connect(self.close_session)
        archivos_menu.addAction(cerrar_sesion_action)

        salir_action = QAction("Salir", self)
        salir_action.triggered.connect(self.close)
        archivos_menu.addAction(salir_action)

        edicion_menu = QMenu("Edición", self)
        menubar.addMenu(edicion_menu)
        edicion_menu.setDisabled(True)

        consultas_menu = QMenu("Consultas", self)
        menubar.addMenu(consultas_menu)
        consultas_menu.setDisabled(True)

        utilidades_menu = QMenu("Utilidades", self)
        menubar.addMenu(utilidades_menu)

        ordenar_action = QAction("Ordenar", self)
        utilidades_menu.addAction(ordenar_action)

        salvaguarda_action = QAction("Salvaguarda", self)
        utilidades_menu.addAction(salvaguarda_action)

        restauracion_action = QAction("Restauración", self)
        utilidades_menu.addAction(restauracion_action)

        utilidades_menu.addSeparator()

        impresora_action = QAction("Impresora", self)
        utilidades_menu.addAction(impresora_action)
        
        utilidades_menu.addSeparator()

        usuario_action = QAction("Usuario", self)
        utilidades_menu.addAction(usuario_action)

        accesos_action = QAction("Accesos", self)
        utilidades_menu.addAction(accesos_action)

        actividad_action = QAction("Actividad", self)
        utilidades_menu.addAction(actividad_action)
        

        ayuda_menu = QMenu("Ayuda", self)
        menubar.addMenu(ayuda_menu)


    def close(self):
        sys.exit()
    
    def close_session(self):
        from pages.login import LoginPage
        from db.db import usuario_activo
        usuario_activo.set_usuario_activo(None)
        self.hide()
        self.login_page = LoginPage()
        self.login_page.show()

    def open_configuracion(self):
        from pages.menu_archivo.config import ConfigPage
        self.configuracion_page = ConfigPage()
        self.configuracion_page.show()
    
    def open_clinicas(self):
        from pages.menu_archivo.clinica import ClinicaPage
        self.clinica_page = ClinicaPage()
        self.clinica_page.show()
    
    def open_sociedades(self):
        from pages.menu_archivo.sociedades import SociedadPage
        self.sociedad_page = SociedadPage()
        self.sociedad_page.show()