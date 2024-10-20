from ..db.connection import Base
from sqlalchemy import Column, Integer, String, Boolean # type: ignore

class Todos(Base):
    __tablename__ = 'todos'
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, default=None)
    description = Column(String, default=None)
    is_active = Column(Boolean, default=True)
    rating = Column(Integer, default=None)