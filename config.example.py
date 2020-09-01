import logging

# Telegram Web API Token
TOKEN='123456789:abcxdefghijklmnopqrs-tuvwxyzabcdefg'

# List of allowed user ids
ALLOWED_USERS=['123456789', '123123123']

# Location to store the saved machines
STORAGE_PATH='/opt/shepherd-bot/machines.csv'

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
