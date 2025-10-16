from .Base import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Attendance(Base):
    __tablename__ = 'attendances'

    id: Mapped[int] = mapped_column(primary_key = True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    object_id: Mapped[int] = mapped_column(ForeignKey('objects.id'))
    date: Mapped[str]
    action: Mapped[str]
    note: Mapped[str] = mapped_column(nullable = True)

    users = relationship("User", back_populates = "attendances")
    objects = relationship("Object", back_populates = "attendances")