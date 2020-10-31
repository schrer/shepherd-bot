# Shepherd

Wake-on-Lan and SSH Telegram bot

![chat example](images/chat.jpg)

## Commands

> See `/help` for a list of available commands

## Requirements

### Bot host
- python 3
- Virtualenv

### Target machines
- SSH server (only for SSH commands like `/shutdown` and `/command`)
- WOL support (for `/start` command)

## Installation

Clone the repository
```
# mkdir -p /opt/shepherd-bot
# chown -R user:group /opt/shepherd-bot
$ git clone url /opt/shepherd-bot
$ cd /opt/shepherd-bot
```

All config files are in the subfolder `config`.
```
$ cd config
```

For all config files (`config.py`,`users.csv`,`machines.csv`,`commands.csv`) there is an example file. Copy or rename them to omit the `example` from their name and edit the config with your favorite editor (aka `nano`) like this:
```
$ cp config.example.py config.py
$ nano config.py
```
`users.csv`: Set up users that are allowed to use the bot and give them permissions. If you want to give several permissions to one user separate them with a comma, giving the permission "\*" will give this user all available permissions:
```
id;name;chatid;permissions
```

`commands.csv`: Set up commands for the `/command` keyword. The colums in the CSV are the following (also see commands.example.csv for example lines):
```
id;name;type;command;description;permission
```

`machines.csv`: Setting up machines manually is optional, since you can let the bot add MAC addresses for the wake command only with a dedicated command, but if you want to use them for SSH commands (`shutdown`, commands defined in `commands.csv`) you need to manually edit the file:
```
id;machineName;mac-address;ip-address;ssh-port;username
```

Set up the Python environment
```
$ virtualenv shepherd_venv
$ source shepherd_venv/bin/activate
(venv)$ pip install -r requirements.txt
```
If any errors occur during the reuirements installation, you are possibly missing some build dependencies. Check from the errors what could be missing and install that with `apt`.
One that was missing for me was libffi-dev as dependency for cffi, which in turn is a transitive dependency of Shepherd via Paramiko (for SSH connections).

Start the application
```
(venv)$ python3 shepherd-bot.py
```

### Autostart on Raspberry Pi

The easiest way is to add the launcher script to `/etc/rc.local`.
```
/opt/shepherd-bot/shepherd-launcher.sh
```

For all commands that run over SSH, it will also be necessary to do some more setup on the Raspberry Pi and the target machine.
In order to be able to login when running Shepherd from `/etc/rc.local`, the root user has to have an auth-key available, that is listed as authorized_key on the SSH server (a.k.a. the machine you want to command). This can be done by adding such a key into the directory `/root/.ssh` on the Raspberry Pi.

### Shutdown command

Besides the setup for an SSH connection over Python, the machine that should be shut down also needs to be prepared.
When running the command `sudo shutdown`, sudo should be configured to not ask for a password with the executing user.
This can be done by running `sudo visudo`. This will open a file, add the following into a new line: `<your_username> ALL=(ALL) NOPASSWD: /sbin/shutdown`, where <your_username> is the username you use as SSH login-detail stored for the Telegram bot.

## Acknowledgements

The base for this repository was [wolbot by Osir](https://github.com/osir/wolbot). Backwards compatibility is not kept, but the version numbering is, so the first official version of Shepherd is 3.0
