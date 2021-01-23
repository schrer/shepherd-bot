import logging

import config.config as config
from lib.sshcontrol import (run_remote_command)
from lib.types import CommandType, Machine

logging.basicConfig(
    format=config.LOG_FORMAT,
    level=config.LOG_LEVEL)
logger = logging.getLogger(__name__)


def execute_command(command, machine: Machine) -> str:
    if command.type.value == CommandType.SSH.value:
        logger.info('SSH command. Com: {c} | M: {m}'.format(c=command.name, m=machine.name))
        return run_remote_command(machine.host, machine.port, machine.user, command.command)
    if command.type.value == CommandType.GENERIC.value:
        logger.info('Generic command. Com: {c} | M: {m}'.format(c=command.name, m=machine.name))
        return 'Specify a command type other than generic to be able to execute the command.'

    logger.info('Unknown command: {c} for machine: {m}'.format(c=command.name, m=machine.name))
    return 'Unknown command type, cannot execute.'
