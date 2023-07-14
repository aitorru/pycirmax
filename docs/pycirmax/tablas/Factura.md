- #tablas 
- #accion_necesaria 
**Se tendrá que configurar de manera manual**

```python
class Factura(Base):
    __tablename__ = 'factura'
    id = Column(Integer, primary_key=True)
    encabezamiento = Column(String)
    pie = Column(String)
    coletilla_execion_IVA = Column(String)
    clinica_id = Column(Integer, ForeignKey('clinicas.id'))
    clinica = relationship("Clinica", backref="factura")
```

### `clinicas.id`
Ver [[tablas/Clínicas]].