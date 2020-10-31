import os.path
import logging
import config.config as config
from lib.utils import (is_not_blank)
from lib.commands import (CommandType, Command, SSHCommand)

# Compatible machine file version with this code
MACHINE_FILE_VERSION = '3.0'
# Compatible command file version with this code
COMMAND_FILE_VERSION = '1.0'

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

def write_machines_file(path, machines):
    return __write_storage_file(path, machines, __machine_to_line, MACHINE_FILE_VERSION)

def read_machines_file(path):
    return __read_storage_file(path, __line_to_machine, MACHINE_FILE_VERSION)

def read_commands_file(path):
    return __read_storage_file(path, __line_to_command, COMMAND_FILE_VERSION)


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
    mid, name, addr, host, port, user = line.split(';', 5)
    return Machine(int(mid), name, addr, host, port, user.strip())

def __line_to_command(line):
    mid, name, type, command, description = line.split(';', 4)
    if SSHCommand.type.value == type:
        return SSHCommand(int(mid), name, description, command)
    return Command(int(mid), name, description)
