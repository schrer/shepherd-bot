import logging

import config.config as config
from lib.sshcontrol import (run_remote_command)
from lib.types import CommandType, Machine, Command

logging.basicConfig(
    format=config.LOG_FORMAT,
    level=config.LOG_LEVEL)
logger = logging.getLogger(__name__)


def execute_command(command: Command, machine: Machine) -> str:
    if command.type.value == CommandType.SSH.value:
        logger.info(f'SSH command. Com: {command.name} | M: {machine.name}')
        return run_remote_command(machine.host, machine.port, machine.user, command.command)
    if command.type.value == CommandType.GENERIC.value:
        logger.info(f'Generic command. Com: {command.name} | M: {machine.name}')
        return 'Specify a command type other than generic to be able to execute the command.'

    logger.info(f'Unknown command: {command.name} for machine: {machine.name}')
    return 'Unknown command type, cannot execute.'
