from .Base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models import User

class Speciality(Base):
    __tablename__ = 'specialities'

    id: Mapped[int] = mapped_column(primary_key = True, autoincrement = True)
    name: Mapped[str] = mapped_column(unique = True)

    users: Mapped[list['User']] = relationship(
        'User',
        back_populates = 'speciality',
        cascade = 'all, delete-orphan'
    )