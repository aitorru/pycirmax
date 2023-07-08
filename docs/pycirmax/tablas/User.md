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
