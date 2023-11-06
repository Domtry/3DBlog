from sqlalchemy import (
    Column,
    String,
    Integer,
    ForeignKey,
)

from src.internal.databases import AbstractModel, Base


class Model3D(AbstractModel, Base):
    __tablename__ = "model3d_model_db"
    __table_args__ = {'extend_existing': True}

    label = Column(String(250), nullable = False)
    image_path = Column(String, nullable = False)
    description = Column(String(250), nullable = False)
    number_views = Column(Integer, nullable = True, default = 0)
    user_id = Column(String(120), ForeignKey('users_model_db.id'), nullable = False)
