# Based on https://code.activestate.com/recipes/358449-wake-on-lan/
# By Fadly Tabrani

import socket
import struct


def wake(mac_address):
    """ Switches on remote computers using WOL. """

    # Check mac_address format and try to compensate.
    if len(mac_address) == 12:
        pass
    elif len(mac_address) == 12 + 5:
        sep = mac_address[2]
        mac_address = mac_address.replace(sep, '')
    else:
        raise ValueError('Incorrect MAC address format')

    # Pad the synchronization stream.
    data = b''.join([b'FF' * 6, bytes(mac_address, 'ascii') * 16])
    send_data = b''

    # Split up the hex values and pack.
    for i in range(0, len(data), 2):
        send_data = b''.join([send_data, struct.pack('B', int(data[i: i + 2], 16))])

    # Broadcast it to the LAN.
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.sendto(send_data, ('<broadcast>', 9))
