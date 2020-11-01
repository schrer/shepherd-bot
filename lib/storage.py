import os.path
import logging
import config.config as config
from lib.utils import (is_not_blank)
from lib.commands import (CommandType, Command, SSHCommand)

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
    def __init__(self, id, name, telegram_id, permissions):
        self.id = id
        self.name = name
        self.telegram_id = str(telegram_id)
        self.permissions = permissions

def write_machines_file(path, machines):
    return __write_storage_file(path, machines, __machine_to_line, MACHINE_FILE_VERSION)

def read_machines_file(path):
    return __read_storage_file(path, __line_to_machine, MACHINE_FILE_VERSION)

def read_commands_file(path):
    return __read_storage_file(path, __line_to_command, COMMAND_FILE_VERSION)

def read_users_file(path):
    return __read_storage_file(path, __line_to_user, USER_FILE_VERSION)

def __write_storage_file(path, machines, object_converter, filespec_version):
    logger.info('Writing stored machines to "{p}"'.format(p=path))
    csv=''
    # Add meta settings
    csv += '$VERSION={v}\n'.format(v=filespec_version)
    
    # Add data
    for m in machines:
        csv += object_converter(m)

    with open(path, 'w') as f:
        f.write(csv)


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


def __machine_to_line(machine):
    if is_not_blank(m.host) and is_not_blank(m.user) and not m.port==None:
        return '{i};{n};{a};{h};{p};{u}\n'.format(i=machine.id, n=machine.name, a=machine.addr, h=machine.host, p=machine.port, u=machine.user)
    return '{i};{n};{a};;;\n'.format(i=machine.id, n=machine.name, a=machine.addr)

def __line_to_machine(line):
    line = "".join(line.split())
    mid, name, addr, host, port, user = line.split(';', 5)
    return Machine(int(mid), name, addr, host, port, user)

def __line_to_command(line):
    cid, name, type, command, description, permission = line.split(';', 5)
    cid = "".join(cid.split())
    name = "".join(name.split())
    command = "".join(command.split())
    permission = "".join(permission.split())
    if SSHCommand.type.value == type:
        return SSHCommand(int(cid), name, description, command, permission)
    return Command(int(cid), name, description, permission)

def __line_to_user(line):
    line = "".join(line.split())
    uid, name, telegram_id, permissions = line.split(';', 3)
    permissionList = __get_permissions_for_stringlist(permissions)
    return User(uid, name, telegram_id, permissionList)
    
def __get_permissions_for_stringlist(value):
    permissions = value.split(',')
    return permissions
