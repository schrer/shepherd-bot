import paramiko
import socket
import logging
import config
from paramiko.client import (SSHClient)
from paramiko.ssh_exception import (SSHException)

DEFAULT_TIMEOUT = 10

logging.basicConfig(
        format=config.LOG_FORMAT,
        level=config.LOG_LEVEL)
logger = logging.getLogger(__name__)

def shutdown(hostname, port, username):
    """
    Sends a command to the specified hostname to shutdown within 1 minute.
    Requires that the login user is allowed to run shutdown without sudo-password.
    """
    command = 'sudo shutdown'
    return run_remote_command(hostname, port, username, command)


def run_remote_command(hostname, port, username, command):
    """
    Runs a command on a remote machine using SSH.
    
    :param str hostname: the server to connect to
    :param int port: the SSH port of the server
    :param str username: the username for login
    :param str command: the command to be executed
    
    :raises SSHException
    """
    log_command_execution(hostname, port, username, command)
    try:
        client = connect_SSHClient(hostname, port, username)
    except SSHException:
        logger.warning('Caught SSHException during SSHClient setup.')
        raise
    except socket.timeout as e:
        logger.warning('Caught connection timeout during SSHClient setup.')
        raise SSHException(e)
    except socket.gaierror as e:
        logger.warning('Cannot find host for SSHClient connection.')
        raise SSHException(e)
    except:
        logger.warning('Something unexpected went wrong during SSHClient setup.')
        raise
        
    try:
        stdin , stdout, stderr = client.exec_command(command)
    except SSHException:
        logger.warning('An error occured during command execution via SSH.')
        raise
    
    output = ''
    for line in stdout:
        output += line

    for line in stderr:
        output += line

    close_SSHClient(client)
    return output
    
        
def connect_SSHClient(hostname, port, username):
    """
    Opens an SSH connection to the specified host. For authentication, any key from an SSH Agent or id_(rsa|ecds|dsa) in ~/.ssh is
    automatically detected by Paramiko and tried for authentication.
    
    :param str hostname: the server to connect to
    :param int port: the SSH port of the server
    :param str username: the username for login
    """
    client = paramiko.SSHClient()
    if config.VERIFY_HOST_KEYS:
        client.load_system_host_keys()
    else:
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname, username=username, port=port, timeout=DEFAULT_TIMEOUT)
    return client

def close_SSHClient(client):
    client.close()
    
def log_command_execution(hostname, port, username, command):
    logger.info('Trying to run command. Host: ' + hostname + ' | Port: ' + str(port) + ' | User: ' + username + ' | Command: ' + command)
