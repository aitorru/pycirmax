- #tablas 
- #todo

```python
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    code = Column(String)
    name = Column(String)
    password = Column(String)
```

## Definiciones

El código es el nombre de usuario.
El nombre es el propio nombre del usuario.
Contraseña se puede entender.