# WOLBOT

Simple Wake-on-Lan Telegram bot

![chat example](images/chat.jpg)

## Commands

> See `/help` for a list of available commands

## Requirements
- python 3
- python-telegram-bot
- Virtualenv (recommended)

## Installation

Clone the repository
```
# mkdir -p /opt/wolbot
# chown -R user:group /opt/wolbot
$ git clone url /opt/wolbot
$ cd /opt/wolbot
```

Edit the config with your favorite editor (aka `vim`)
```
$ cp config.example.py config.py
$ vim config.py
```

Set up the Python environment
```
$ virtualenv wolbot_venv
$ source wolbot_venv/bin/activate
(venv)$ pip install -r requirements.txt
```

Start the application
```
(venv)$ python3 wolbot.py
```

### Autostart on Raspberry Pi

The easiest way is to add the launcher script to `/etc/rc.local`.
```
/opt/wolbot/wolbot-launcher.sh
```

For all commands that run over SSH, it will also be necessary to do some more setup on the Raspberry Pi.
In order to be able to login when running wolbot from `/etc/rc.local`, there has to root user has to have an auth-key available, that is listed as authorized_key on the SSH server (a.k.a. the machine you want to command). This can be done by adding such a key into the directory `/root/.ssh`.

### Shutdown command

Besides the setup for an SSH connection over Python, the machine that should be shut down also needs to be prepared.
When running the command `sudo shutdown`, sudo should be configured to not ask for a password with the executing user.
This can be done by running `sudo visudo`. This will open a file, add the following into a new line: `<your_username> ALL=(ALL) NOPASSWD: /sbin/shutdown`
