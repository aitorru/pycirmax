- #tablas
- #accion_necesaria
**Se tendrá que configurar de manera manual**

```python
class Presupuesto(Base):
    __tablename__ = 'presupuesto'
    id = Column(Integer, primary_key=True)
    encabezamiento = Column(String)
    pie = Column(String)
    forma_de_pago = Column(String)
    clinica_id = Column(Integer, ForeignKey('clinicas.id'))
    clinica = relationship("Clinica", backref="presupuesto")
```

### `clinicas.id`
Ver [[tablas/Clínicas]].