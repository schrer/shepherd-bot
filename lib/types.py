from enum import Enum


class CommandType(Enum):
    GENERIC = 'generic'
    SSH = 'ssh'


class Command:
    type = CommandType.GENERIC

    def __init__(self, mid, name, description, permission):
        self.id = mid
        self.name = name
        self.description = description
        self.permission = permission


class SSHCommand(Command):
    type = CommandType.SSH

    def __init__(self, mid, name, description, permission, command):
        super(SSHCommand, self).__init__(mid, name, description, permission)
        self.command = command


class Machine:
    def __init__(self, mid, name, addr, host=None, port=22, user=None):
        self.id = mid
        self.name = name
        self.addr = addr
        self.host = host
        self.port = port
        self.user = user


class User:
    def __init__(self, uid, name, telegram_id, permissions):
        self.id = uid
        self.name = name
        self.telegram_id = str(telegram_id)
        self.permissions = permissions
