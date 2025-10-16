from models import Attendance
from .BaseRepository import BaseRepository

class AttendanceRepository(BaseRepository):
    model = Attendance
