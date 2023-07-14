- #tablas
- #accion_necesaria
**Se tendrá que configurar de manera manual**

```python
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
```

### `clinicas.id`
Ver [[tablas/Clínicas]].