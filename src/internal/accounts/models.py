
from sqlalchemy import (
    Column,
    String,
    LargeBinary,
    Boolean,
    ForeignKey,
    Text)
from sqlalchemy.orm import relationship

from src.internal.databases import AbstractModel, Base


class Accounts(AbstractModel, Base):
    __tablename__ = "accounts_model_db"
    __table_args__ = {'extend_existing': True}

    username = Column(String, nullable = False, unique = True)
    encrypt_key = Column(LargeBinary)
    password = Column(LargeBinary)
    user_id = Column(String, ForeignKey('users_model_db.id'), nullable = False)
    authentications = relationship('Authentications')