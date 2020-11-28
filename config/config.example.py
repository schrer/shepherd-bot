import logging

# Telegram Web API Token
TOKEN='123456789:abcxdefghijklmnopqrs-tuvwxyzabcdefg'

# Location to store the saved machines
MACHINES_STORAGE_PATH='/opt/shepherd-bot/config/machines.csv'

# Location to store the saved commands
COMMANDS_STORAGE_PATH='/opt/shepherd-bot/config/commands.csv'

# Location to store the saved users
USERS_STORAGE_PATH='/opt/shepherd-bot/config/users.csv'

# Separator to use when printing addresses
MAC_ADDR_SEPARATOR='-'

# The webservice to call to get the bot's public IP
IP_WEBSERVICE='https://ipv4.icanhazip.com/'

# The Regex used to find the IP in the webservice response
IP_REGEX='([0-9]{1,3}\.){3}[0-9]{1,3}'

# Logger format for whole application
LOG_FORMAT='%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# General log level to use in the application
LOG_LEVEL=logging.INFO

# Turn verification of host keys off or on. Not advisible, only turn off in private networks and for testing purposes, if ever
VERIFY_HOST_KEYS=True

PERM_WAKE='wake'
PERM_SHUTDOWN='shutdown'
PERM_LIST=PERM_WAKE
PERM_WAKEMAC=PERM_WAKE
PERM_PING=PERM_WAKE
