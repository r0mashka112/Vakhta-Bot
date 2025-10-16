from .message_handlers import router as message_router
from .command_handlers import router as command_router

from .fsm import (
    fsm_auth_router,
    fsm_edit_my_data_router,
    fsm_choose_object_and_date_router
)

__all__ = [
    'message_router',
    'command_router',
    'fsm_auth_router',
    'fsm_edit_my_data_router',
    'fsm_choose_object_and_date_router'
]