- #tablas
- #accion_necesaria
**Se tendrá que configurar por el fichero.** Ver [[Configuración del programa]].

```python
class Clinica(Base):
    __tablename__ = 'clinicas'
    id = Column(Integer, primary_key=True)
    letra = Column(String)
    nombre = Column(String)
```
