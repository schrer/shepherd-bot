import logging
from enum import Enum

import config.config as config
from lib.sshcontrol import (run_remote_command)

logging.basicConfig(
        format=config.LOG_FORMAT,
        level=config.LOG_LEVEL)
logger = logging.getLogger(__name__)

class CommandType(Enum):
    GENERIC='generic'
    SSH='ssh'
    
class Command:
    type = CommandType.GENERIC
    def __init__(self, mid, name, description, permission):
        self.id = mid
        self.name = name
        self.description = description
        self.permission = permission

class SSHCommand(Command):
    type = CommandType.SSH
    def __init__(self, mid, name, description, command, permission):
        super(SSHCommand, self).__init__(mid, name, description, permission)
        self.command = command

def execute_command(command, machine):
    if command.type.value== CommandType.SSH.value:
        logger.info('SSH command. Com: {c} | M: {m}'.format(c=command.name, m=machine.name))
        return run_remote_command(machine.host, machine.port, machine.user, command.command)
    if command.type.value == CommandType.GENERIC.value:
        logger.info('Generic command. Com: {c} | M: {m}'.format(c=command.name, m=machine.name))
        return 'Specify a command type other than generic to be able to execute the command.'
    
    logger.info('Unknown command: {c} for machine: {m}'.format(c=command.name, m=machine.name))
    return 'Unknown command type, cannot execute.'
