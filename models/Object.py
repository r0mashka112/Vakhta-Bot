from .Base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models import Attendance

class Object(Base):
    __tablename__ = 'objects'

    id: Mapped[int] = mapped_column(primary_key = True, autoincrement = True)
    name: Mapped[str] = mapped_column(unique = True)

    attendances: Mapped[list['Attendance']] = relationship(
        'Attendance',
        back_populates = 'object',
        cascade = 'all, delete-orphan'
    )