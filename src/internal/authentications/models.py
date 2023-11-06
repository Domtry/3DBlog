from sqlalchemy import Column, Boolean, ForeignKey, String, Text

from src.internal.databases import AbstractModel, Base


class Authentications(AbstractModel, Base):
    __tablename__ = "authentications_model_db"
    __table_args__ = {'extend_existing': True}

    access_token = Column(Text, nullable = False)
    refresh_token = Column(Text, nullable = False)
    is_expired = Column(Boolean, nullable = False, default = False)
    account_id = Column(String, ForeignKey('accounts_model_db.id'), nullable = False)