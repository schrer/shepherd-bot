import os.path
import logging
import config.config as config
from lib.commands import (Command, SSHCommand)

# Compatible machine file version with this code
MACHINE_FILE_VERSION = '3.0'
# Compatible command file version with this code
COMMAND_FILE_VERSION = '2.0'
# Compatible user file version with this code
USER_FILE_VERSION = '1.0'

logging.basicConfig(
    format=config.LOG_FORMAT,
    level=config.LOG_LEVEL)
logger = logging.getLogger(__name__)


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


def read_machines_file(path):
    return __read_storage_file(path, __line_to_machine, MACHINE_FILE_VERSION)


def read_commands_file(path):
    return __read_storage_file(path, __line_to_command, COMMAND_FILE_VERSION)


def read_users_file(path):
    return __read_storage_file(path, __line_to_user, USER_FILE_VERSION)


def __read_storage_file(path, line_converter, filespec_version):
    objects = []
    logger.info('Reading stored entries from "{p}"'.format(p=path))
    # Warning: file contents will not be validated
    if not os.path.isfile(path):
        logger.error('No file found in {p}'.format(p=path))
        return
    with open(path, 'r') as f:
        for i, line in enumerate(f):
            # Remove all whitespaces
            line = line.strip()
            # Handle Settings
            if line.startswith('$VERSION'):
                _, value = line.split('=', 1)
                if not value.strip() == filespec_version:
                    raise ValueError('Incompatible storage file version')
            else:
                objects.append(line_converter(line))

    return objects


def __line_to_machine(line):
    line = "".join(line.split())
    mid, name, addr, host, port, user = line.split(';', 5)
    return Machine(int(mid), name, addr, host, port, user)


def __line_to_command(line):
    cid, name, command_type, command, description, permission = line.split(';', 5)
    cid = "".join(cid.split())
    name = "".join(name.split())
    permission = "".join(permission.split())
    if SSHCommand.type.value == command_type:
        return SSHCommand(int(cid), name, description, command, permission)
    return Command(int(cid), name, description, permission)


def __line_to_user(line):
    line = "".join(line.split())
    uid, name, telegram_id, permissions = line.split(';', 3)
    permission_list = __get_permissions_for_stringlist(permissions)
    return User(uid, name, telegram_id, permission_list)


def __get_permissions_for_stringlist(value):
    permissions = value.split(',')
    return permissions
