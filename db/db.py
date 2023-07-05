from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Database:
    def __init__(self, db_name, user, password, host='localhost', port=3306):
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

db = Database('Cirmax', 'cirmax', 'cirmaxp')
db.create_tables()

usuario_activo = _State()