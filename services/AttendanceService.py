from database.repositories import AttendanceRepository

class AttendanceService:
    def __init__(self, session):
        self.session = session
        self._attendance_repo = None

    @property
    def attendance_repo(self):
        if self._attendance_repo is None:
            self._attendance_repo = AttendanceRepository(
                self.session
            )
        return self._attendance_repo


    async def create_attendance(
            self,
            user_id: int,
            object_id: int,
            date,
            action: str,
            note: str = None
    ):
        new_attendance = await self.attendance_repo.create(
            user_id = user_id,
            object_id = object_id,
            date = date,
            action = action,
            note = note
        )

        return new_attendance

    async def get_attendance_by(
        self,
        user_id: int,
        object_id: int = None,
        date = None,
        action: str = None,
        note: str = None
    ):
        attendance_data = {
            'user_id': user_id,
            'object_id': object_id,
            'date': date,
            'action': action,
            'note': note
        }

        attendance = await self.attendance_repo.read(
            **attendance_data
        )

        return attendance.first()
