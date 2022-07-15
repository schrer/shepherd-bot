import re
import platform
import subprocess
from typing import List, Union

import config.config as config
from lib.types import Machine, Command, User


def ping_server(hostname: str) -> bool:
    """
    Returns True if host (str) responds to a ping request.
    """

    # Option for the number of packets
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '1', hostname]
    return subprocess.call(command) == 0


def is_valid_name(name: str) -> bool:
    pattern = '[^_a-z0-9]'
    return not re.search(pattern, name)


def get_highest_id(elements: List[Union[Machine, Command, User]]) -> int:
    highest = -1
    for m in elements:
        if m.id > highest:
            highest = m.id
    return highest


def is_not_blank(string: str) -> bool:
    return bool(string and string.strip())


def find_by_name(objects: List[Union[Machine, Command, User]], name: str) -> Union[Machine, Command, User, None]:
    for o in objects:
        if o.name == name:
            return o
    return None


def check_ssh_setup(machine: Machine):
    return is_not_blank(machine.host) and is_not_blank(machine.user) and machine.port is not None
