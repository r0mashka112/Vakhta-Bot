from .Base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Speciality(Base):
    __tablename__ = 'specialities'

    id: Mapped[int] = mapped_column(primary_key = True)
    name: Mapped[str] = mapped_column(unique = True)

    users = relationship("User", back_populates = "specialities")