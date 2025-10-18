from database.repositories import AttendanceRepository

class AttendanceService:
    def __init__(self, session):
        self._attendance_repo = AttendanceRepository(
            session
        )

    async def create_attendance(
            self,
            user_id: int,
            object_id: int,
            date,
            action: str,
            note: str = None
    ):
        new_attendance = await self._attendance_repo.create(
            user_id = user_id,
            object_id = object_id,
            date = date,
            action = action,
            note = note
        )

        return new_attendance

    async def get_attendance_by(
        self,
        user_id: int = None,
        object_id: int = None,
        date = None,
        action: str = None
    ):
        attendance_data = {}

        if user_id is not None:
            attendance_data['user_id'] = user_id
        if object_id is not None:
            attendance_data['object_id'] = object_id
        if date is not None:
            attendance_data['date'] = date
        if action is not None:
            attendance_data['action'] = action

        if len(attendance_data) == 0:
            return await self._attendance_repo.read(many = True)

        return await self._attendance_repo.read(
            **attendance_data
        )
