from sqlalchemy import (
    Column,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from src.internal.databases import AbstractModel, Base


class Users(AbstractModel, Base):
    __tablename__ = "users_model_db"
    __table_args__ = {'extend_existing': True}

    name = Column(String(250), nullable = False)
    pseudo = Column(String(250), nullable = False)
    email = Column(String, nullable = False)
    badges = Column(Text, nullable = True, default = "")
    model3ds = relationship('Model3D')
    accounts = relationship('Accounts')