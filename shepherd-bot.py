#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import re

from telegram import (InlineKeyboardButton,
                      InlineKeyboardMarkup)
from telegram.ext import (Updater,
                          CommandHandler,
                          CallbackQueryHandler)
import requests
from paramiko.ssh_exception import (SSHException)

import version
import config.config as config
import lib.wol as wol
import lib.sshcontrol as ssh_control
import lib.permission as perm
from lib.storage import (read_machines_file, read_commands_file)
from lib.utils import (find_by_name, check_ssh_setup, ping_server)
from lib.commands import (execute_command)

logging.basicConfig(
    format=config.LOG_FORMAT,
    level=config.LOG_LEVEL)
logger = logging.getLogger(__name__)
machines = []
commands = []


##
# Command Handlers
##

def cmd_help(update, context):
    log_call(update)
    if not identify(update):
        return
    help_message = """
Shepherd v{v}

/help
    Display this help

/wake [name]
    Wake saved machine with name

/wakemac <mac>
    Wake machine with mac address

/shutdown [name]
    Shutdown saved machine with name
    
/command [name] <command>
    Run command on machine via SSH. If neither machine name nor command are specified, a list of supported commands is sent

/ping [name]
    Ping a server to check if it is online and reachable by the bot

/list
    List all saved machines

/ip
    Get the public IP address of the network Shepherd is in

Names are only required if more than one machine is configured and may only contain a-z, 0-9 and _
Mac addresses can use the separator '{separator}'
    """.format(v=version.V, separator=config.MAC_ADDR_SEPARATOR)
    update.message.reply_text(help_message)


def cmd_wake(update, context):
    log_call(update)
    # Check correctness of call
    CMD_PERMISSION = config.PERM_WAKE
    if not identify(update) or not authorize(update, CMD_PERMISSION):
        return

    # When no args are supplied
    args = context.args
    if len(args) < 1 and len(machines) != 1:
        if not len(machines):
            update.message.reply_text('Please add a machine in the configuration first!')
        markup = InlineKeyboardMarkup(generate_machine_keyboard(machines))
        update.message.reply_text('Please select a machine to wake:', reply_markup=markup)
        return

    if len(args) > 1:
        update.message.reply_text('Please supply only a machine name')
        return

    # Parse arguments and send WoL packets
    if len(args) == 0:
        machine_name = machines[0].name
    else:
        machine_name = args[0]
    for m in machines:
        if m.name == machine_name:
            send_magic_packet(update, m.addr, m.name)
            return
    update.message.reply_text('Could not find ' + machine_name)


def cmd_wake_keyboard_handler(update, context):
    try:
        n = int(update.callback_query.data)
    except ValueError:
        pass
    matches = [m for m in machines if m.id == n]
    if len(matches) < 1:
        return
    send_magic_packet(update, matches[0].addr, matches[0].name)


def cmd_wake_mac(update, context):
    log_call(update)
    # Check correctness of call
    CMD_PERMISSION = config.PERM_WAKEMAC
    if not identify(update) or not authorize(update, CMD_PERMISSION):
        return

    args = context.args
    if len(args) < 1:
        update.message.reply_text('Please supply a mac address')
        return

    # Parse arguments and send WoL packets
    mac_address = args[0]
    send_magic_packet(update, mac_address, mac_address)


def cmd_shutdown(update, context):
    log_call(update)
    # Check correctness of call
    CMD_PERMISSION = config.PERM_SHUTDOWN
    if not identify(update) or not authorize(update, CMD_PERMISSION):
        return

    args = context.args
    # When no args are supplied
    if len(args) < 1 and len(machines) != 1:
        if not len(machines):
            update.message.reply_text('Please add a machine in the configuration first!')
        markup = InlineKeyboardMarkup(generate_machine_keyboard(machines))
        update.message.reply_text('Please select a machine to wake:', reply_markup=markup)
        return

    # Parse arguments and send shutdown command
    if len(args) == 0:
        machine_name = machines[0].name
    else:
        machine_name = args[0]

    machine = find_by_name(machines, machine_name)

    if machine is None:
        update.message.reply_text('Could not find ' + machine_name)
        return

    if check_ssh_setup(machine):
        logger.info(
            'host: {host}| user: {user}| port: {port}'.format(host=machine.host, user=machine.user, port=machine.port))
        send_shutdown_command(update, machine.host, machine.port, machine.user, machine.name)
    else:
        logger.info('Machine {name} not set up for SSH connections.'.format(name=machine.name))
        update.message.reply_text(machine.name + ' is not set up for SSH connection')
    return


def cmd_list(update, context):
    log_call(update)
    # Check correctness of call
    CMD_PERMISSION = config.PERM_LIST
    if not identify(update) or not authorize(update, CMD_PERMISSION):
        return

    # Print all stored machines
    msg = '{num} Stored Machines:\n'.format(num=len(machines))
    for m in machines:
        msg += '#{i}: "{n}" → {a}\n'.format(i=m.id, n=m.name, a=m.addr)
    update.message.reply_text(msg)


def cmd_ip(update, context):
    log_call(update)
    # Check correctness of call
    if not identify(update):
        return

    try:
        # Get IP from webservice
        r = requests.get(config.IP_WEBSERVICE)
        # Extract IP using regex
        pattern = re.compile(config.IP_REGEX)
        match = pattern.search(r.text)

        if not match:
            raise RuntimeError('Could not find IP in webpage response')
        update.message.reply_text(match.group())
    except RuntimeError as e:
        update.message.reply_text('Error: ' + str(e))


def cmd_command(update, context):
    log_call(update)

    if not identify(update):
        return

    if len(machines) == 0:
        update.message.reply_text('No machines are registered. Please add a machine in the configuration first!')
        return

    args = context.args
    if len(args) == 0:
        list_commands(update)
        return

    if len(args) > 2:
        update.message.reply_text('Only one command can be processed at a time.')
        return

    if len(args) == 1:
        machine_name = machines[0].name
        command_name = args[0]
    else:
        machine_name = args[0]
        command_name = args[1]

    command = find_by_name(commands, command_name)

    if command is None:
        update.message.reply_text('Could not find command "{cmd}"'.format(cmd=command_name))
        return

    CMD_PERMISSION = command.permission
    if not authorize(update, CMD_PERMISSION):
        return

    machine = find_by_name(machines, machine_name)

    if machine is None:
        update.message.reply_text('Could not find machine {machine}.'.format(machine=machine_name))
        return

    if not check_ssh_setup(machine):
        update.message.reply_text('Machine {machine} is not set up for SSH connections.'.format(machine=machine_name))
        return

    try:
        logger.info('Attempting to run command on machine {m}: {c}'.format(m=machine.name, c=command.name))
        msg = execute_command(command, machine)
        update.message.reply_text('Command executed:\n{m}'.format(m=msg))
    except SSHException as e:
        update.message.reply_text('Error in SSH messaging: {e}'.format(e=str(e)))
        return
    except RuntimeError as e:
        update.message.reply_text('An unexpected error occurred: {e}'.format(e=str(e)))
        return


def cmd_ping(update, context):
    log_call(update)
    # Check correctness of call
    CMD_PERMISSION = config.PERM_PING
    if not identify(update) or not authorize(update, CMD_PERMISSION):
        return

    # When no args are supplied
    args = context.args
    if len(args) < 1 and len(machines) != 1:
        if not len(machines):
            update.message.reply_text('Please add a machine with in the configuration first!')
        markup = InlineKeyboardMarkup(generate_machine_keyboard(machines))
        update.message.reply_text('Please select a machine to wake:', reply_markup=markup)
        return

    if len(args) > 1:
        update.message.reply_text('Please supply only a machine name')
        return

    # Parse arguments and send WoL packets
    if len(args) == 0:
        machine_name = machines[0].name
    else:
        machine_name = args[0]
    for m in machines:
        if m.name == machine_name:
            if ping_server(m.host):
                update.message.reply_text('Pong\nServer is running.')
            else:
                update.message.reply_text('Could not reach {name} under IP {host}'.format(name=m.name, host=m.host))
            return
    update.message.reply_text('Could not find ' + machine_name)


def list_commands(update):
    msg = '{num} Stored Commands:\n'.format(num=len(commands))
    for c in commands:
        msg += '{name}: {description}\n'.format(name=c.name, description=c.description)

    msg += '\nRun a command with /command [machine_name] <cmd_name>'

    update.message.reply_text(msg)


##
# Other Functions
##

def error(update, context):
    logger.warning('Update "{u}" caused error "{e}"'.format(u=update, e=context.error))


def log_call(update):
    uid = update.message.from_user.id
    cmd = update.message.text.split(' ', 1)
    if len(cmd) > 1:
        logger.info('User [{u}] invoked command {c} with arguments [{a}]'
                    .format(c=cmd[0], a=cmd[1], u=uid))
    else:
        logger.info('User [{u}] invoked command {c}'
                    .format(c=cmd[0], u=uid))


def send_magic_packet(update, mac_address, display_name):
    try:
        wol.wake(mac_address)
    except ValueError as e:
        update.message.reply_text(str(e))
        return
    poke = 'Sending magic packets...\n{name}'.format(
        name=display_name)

    if update.callback_query:
        update.callback_query.edit_message_text(poke)
    else:
        update.message.reply_text(poke)


def send_shutdown_command(update, hostname, port, user, display_name):
    try:
        cmdOutput = ssh_control.shutdown(hostname, port, user)
    except ValueError as e:
        update.message.reply_text(str(e))
        return
    except SSHException as e:
        update.message.reply_text(
            'An error occurred while trying to send the shutdown command over SSH.\n{e}\n'.format(e=str(e)))
        return

    poke = 'Shutdown command sent to {name}. Output:\n{output}'.format(
        name=display_name, output=cmdOutput)

    if update.callback_query:
        update.callback_query.edit_message_text(poke)
    else:
        update.message.reply_text(poke)


def generate_machine_keyboard(machines):
    kbd = []
    for m in machines:
        btn = InlineKeyboardButton(m.name, callback_data=m.id)
        kbd.append([btn])
    return kbd


def identify(update):
    if not perm.is_known_user(update.message.from_user.id):
        logger.warning('Unknown User {fn} {ln} [{i}] tried to call bot'.format(
            fn=update.message.from_user.first_name,
            ln=update.message.from_user.last_name,
            i=update.message.from_user.id))
        # TODO: reply with GIF of Post Malone waving with finger in police outfit
        update.message.reply_text('You are not authorized to use this bot.\n'
                                  + 'To set up your own visit https://github.com/schrer/shepherd-bot')
        return False
    return True


def authorize(update, permission):
    if not perm.has_permission(update.message.from_user.id, permission):
        name = perm.get_user_name(update.message.from_user.id)
        logger.warning('User {na} [{id}] tried to use permission "{pe}" but does not have it'.format(
            na=name,
            id=update.message.from_user.id,
            pe=permission))
        update.message.reply_text('Sorry, but you are not authorized to run this command.\n'
                                  + 'Ask your bot admin if you think you should get access.')
        return False
    return True


def main():
    logger.info('Starting Shepherd bot version {v}'.format(v=version.V))
    if not config.VERIFY_HOST_KEYS:
        logger.warning('Verification of host keys for SSH connections is deactivated.')
    global machines
    global commands
    machines = read_machines_file(config.MACHINES_STORAGE_PATH)
    commands = read_commands_file(config.COMMANDS_STORAGE_PATH)
    perm.load_users()

    # Set up updater
    updater = Updater(config.TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Add handlers
    dispatcher.add_handler(CommandHandler('help', cmd_help))
    dispatcher.add_handler(CommandHandler('list', cmd_list))
    dispatcher.add_handler(CommandHandler('ip', cmd_ip))
    dispatcher.add_handler(CommandHandler('wake', cmd_wake, pass_args=True))
    dispatcher.add_handler(CallbackQueryHandler(cmd_wake_keyboard_handler))
    dispatcher.add_handler(CommandHandler('wakemac', cmd_wake_mac, pass_args=True))
    dispatcher.add_handler(CommandHandler('shutdown', cmd_shutdown, pass_args=True))
    dispatcher.add_handler(CommandHandler('command', cmd_command, pass_args=True))
    dispatcher.add_handler(CommandHandler('ping', cmd_ping, pass_args=True))

    dispatcher.add_error_handler(error)

    # Start bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
