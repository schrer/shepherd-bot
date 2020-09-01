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
- SSH server (only for SSH commands)
- WOL support (for `/start` command)

## Installation

Clone the repository
```
# mkdir -p /opt/shepherd-bot
# chown -R user:group /opt/shepherd-bot
$ git clone url /opt/shepherd-bot
$ cd /opt/shepherd-bot
```

Edit the config with your favorite editor (aka `vim`)
```
$ cp config.example.py config.py
$ vim config.py
```

Set up the Python environment
```
$ virtualenv shepherd_venv
$ source shepherd_venv/bin/activate
(venv)$ pip install -r requirements.txt
```
If any errors occur during the reuirements installation, you are possibly missing some build dependencies. Check from the errors what could be missing and install that with `apt`.

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
