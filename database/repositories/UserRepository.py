from models import User
from .BaseRepository import BaseRepository

class UserRepository(BaseRepository):
    model = User