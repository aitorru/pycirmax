from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, relationship
from sqlalchemy.ext.declarative import declarative_base
import logging

Base = declarative_base()

# Read the config file
import toml
with open('config.toml', 'r') as f:
    config = toml.load(f)

class Database:
    def __init__(self, db_name=config['database']['name'], user=config['database']['user'], password=config['database']['password'], host=config['database']['host'], port=config['database']['port']):
        try:
            self.engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db_name}')
            self._session = scoped_session(sessionmaker(bind=self.engine))
            # If tables dont exist, create them
            self.create_tables()
        except Exception as e:
            logging.error("Database connection error: %s", e)
            # Use qt to create an error dialog
            from PyQt5.QtWidgets import QMessageBox
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error de conexión con la base de datos")
            msg.setInformativeText("No se pudo conectar con la base de datos. Compruebe que el servidor de base de datos está en funcionamiento.")
            msg.setWindowTitle("Error")
            msg.exec_()
            # Exit the app
            import sys
            sys.exit(1)

    @property
    def session(self):
        return self._session()

    def create_tables(self):
        Base.metadata.create_all(self.engine)

class _Database:
    def __init__(self, db_name=config['database']['name'], user=config['database']['user'], password=config['database']['password'], host=config['database']['host'], port=config['database']['port']):
        self.engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db_name}')
        self._session = sessionmaker(bind=self.engine)

    @property
    def session(self):
        return self._session()

    def create_tables(self):
        Base.metadata.create_all(self.engine)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    code = Column(String)
    name = Column(String)
    password = Column(String)

    def set_password(self, password: str):
        self.password = password
    
    def set_name(self, name: str):
        self.name = name
    
    def set_code(self, code: str):
        self.code = code
    
    def get_password(self):
        return self.password

    def get_name(self):
        return self.name

    def get_code(self):
        return self.code

class Empresa(Base):
    __tablename__ = 'empresa'

    id = Column(Integer, primary_key=True)
    nif = Column(String)
    razon_social = Column(String)
    domicilio = Column(String)
    codigo_postal = Column(String)
    poblacion = Column(String)
    provincia = Column(String)
    telefono = Column(String)
    fax = Column(String)
    coletilla_gdpr = Column(String)
    # Create a foreign key relationship with `clinicas` table
    clinica_id = Column(Integer, ForeignKey('clinicas.id'))
    clinica = relationship("Clinica", backref="empresa")

class Presupuesto(Base):
    __tablename__ = 'presupuesto'

    id = Column(Integer, primary_key=True)
    encabezamiento = Column(String)
    pie = Column(String)
    forma_de_pago = Column(String)
    clinica_id = Column(Integer, ForeignKey('clinicas.id'))
    clinica = relationship("Clinica", backref="presupuesto")

class Factura(Base):
    __tablename__ = 'factura'

    id = Column(Integer, primary_key=True)
    encabezamiento = Column(String)
    pie = Column(String)
    coletilla_execion_IVA = Column(String)
    clinica_id = Column(Integer, ForeignKey('clinicas.id'))
    clinica = relationship("Clinica", backref="factura")
    

class Clinica(Base):
    __tablename__ = 'clinicas'

    id = Column(Integer, primary_key=True)
    letra = Column(String)
    nombre = Column(String)

class Sociedad(Base):
    __tablename__ = 'sociedad'

    id = Column(Integer, primary_key=True)
    codigo = Column(String)
    nombre = Column(String)

class Referidor(Base):
    __tablename__ = 'referidor'

    id = Column(Integer, primary_key=True)
    codigo = Column(String)
    nombre = Column(String)

class Paciente(Base):
    __tablename__ = 'paciente'

    id = Column(Integer, primary_key=True)
    codigo = Column(String)
    nombre = Column(String)
    domicilio = Column(String)
    cp = Column(String)
    poblacion = Column(String)
class _State:
    def __init__(self):
        self.usuario_activo: User | None = None

    def set_usuario_activo(self, usuario):
        self.usuario_activo = usuario

    def get_usuario_activo(self):
        return self.usuario_activo

    def get_nombre_usuario(self):
        if self.usuario_activo is None:
            return ''
        return str(self.usuario_activo.name)

db = _Database()
db.create_tables()

usuario_activo = _State()

