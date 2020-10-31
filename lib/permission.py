from enum import Enum

import config.config as config
from lib.storage import (read_users_file)

ALMIGHTY_PERMISSION = '*'

users = []

def has_permission(userid, permission):
    user = __find_user(userid)
    if user is None:
        return False
    return (ALMIGHTY_PERMISSION in user.permissions) or (permission in user.permissions)

def is_known_user(userid):
    user = __find_user(userid)
    return user is not None

def get_user_name(userid):
    user = __find_user(userid)
    if user is None:
        return None
    return user.name
    
def load_users():
    global users
    users = read_users_file(config.USERS_STORAGE_PATH)

def __find_user(id):
    return next((u for u in users if u.telegram_id==str(id)), None)

