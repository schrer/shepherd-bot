from enum import Enum
from typing import List


class CommandType(Enum):
    GENERIC = 'generic'
    SSH = 'ssh'


class Command:
    type: CommandType = CommandType.GENERIC

    def __init__(self, mid: int, name: str, description: str, permission: str):
        self.id: int = mid
        self.name: str = name
        self.description: str = description
        self.permission: str = permission


class SSHCommand(Command):
    type: CommandType = CommandType.SSH

    def __init__(self, mid: int, name: str, description: str, permission: str, command: str):
        super(SSHCommand, self).__init__(mid, name, description, permission)
        self.command: str = command


class Machine:
    def __init__(self, mid: int, name: str, addr: str, host: str = None, port: int = 22, user: str = None):
        self.id: int = mid
        self.name: str = name
        self.addr: str = addr
        self.host: str = host
        self.port: int = port
        self.user: str = user


class User:
    def __init__(self, uid: int, name: str, telegram_id: str, permissions: List[str]):
        self.id: int = uid
        self.name: str = name
        self.telegram_id: str = str(telegram_id)
        self.permissions: List[str] = permissions
