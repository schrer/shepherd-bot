import re

def is_valid_name(name):
    pattern = '[^_a-z0-9]'
    return not re.search(pattern, name)


def normalize_mac_address(addr):
    if len(addr) == 12:
        pass
        return config.MAC_ADDR_SEPARATOR.join(
                addr[i:i+2] for i in range(0,12,2))
    elif len(addr) == 12 + 5:
        sep = addr[2]
        return addr.replace(sep, config.MAC_ADDR_SEPARATOR)
    else:
        raise ValueError('Incorrect MAC address format')


def get_highest_id(elements):
    highest = -1
    for m in elements:
        if m.id > highest:
            highest = m.id
    return highest

def is_not_blank(string):
    return bool(string and string.strip())

def find_by_name(objects, name):
    for o in objects:
        if o.name == name:
            return o
    return None
        
def check_ssh_setup(machine):
    return is_not_blank(machine.host) and is_not_blank(machine.user) and not machine.port==None
