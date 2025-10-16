from .Base import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key = True)
    telegram_id: Mapped[int] = mapped_column(unique = True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    middle_name: Mapped[str] = mapped_column(nullable = True)
    speciality_id: Mapped[int] = mapped_column(ForeignKey('specialities.id'))
    phone: Mapped[str] = mapped_column(unique = True)
    is_admin: Mapped[bool] = mapped_column(default = False)

    attendances = relationship("Attendance", back_populates = "users")
    specialities = relationship("Speciality", back_populates = "users")