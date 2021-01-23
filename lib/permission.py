from typing import overload, List, Union

import config.config as config
from lib.storage import (read_users_file)
from lib.types import User

ALMIGHTY_PERMISSION = '*'

users: List[User] = []


def has_permission(userid: str, permission: str) -> bool:
    user: User = __find_user(userid)
    if user is None:
        return False
    return (ALMIGHTY_PERMISSION in user.permissions) or (permission in user.permissions)


def is_known_user(userid: str) -> bool:
    user: User = __find_user(userid)
    return user is not None


def get_user_name(userid: str) -> Union[str, None]:
    user: User = __find_user(userid)
    if user is None:
        return None
    return user.name


def load_users() -> None:
    global users
    users = read_users_file(config.USERS_STORAGE_PATH)


@overload
def __find_user(tel_id: str) -> User:
    return next((u for u in users if u.telegram_id == tel_id), None)


@overload
def __find_user(tel_id: int) -> User:
    return next((u for u in users if u.telegram_id == str(tel_id)), None)


def __find_user(tel_id) -> User:
    return next((u for u in users if u.telegram_id == str(tel_id)), None)
