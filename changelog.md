# Changelog

## Shepherd 3.x.y

- Code improvements: Update requirements, use f-strings instead of format

## Shepherd 3.5.0

- Disabling certain commands completely is now possible by making the command permission in config.py an empty string.
- Remove command `/wakemac`, as use case didn't really seem to be relevant. Also better to not let the bot communicate with any device in the network.
- Remove unused keyboard handler from code

## Shepherd 3.4.1

- Fix bug that caused command permissions to be interpreted as the command itself for SSH commands

## Shepherd 3.4.0

- Fix bug where CSV files with empty lines could not be read. Empty lines are now allowed at the end and between lines
- Update formatting and clean imports
- Move custom types to specific file to make it easier to prevent circular dependencies
- Add type hints to all method headers
- Minor changes to readme.md

## Shepherd 3.3.0

- Identifiers of permissions are now granular to each command and can be configured in config.py
- Added `/ping` command to ping a machine and check if it is reachable
- Remove commands `/add` and `/remove`. Editing of machines is now only possible directly in the file machines.csv
- Update parts of the `/help` message

## Shepherd 3.2.1

- Fix minor bug that caused command descriptions to show up without whitespaces

## Shepherd 3.2.0

- Move all config relevant files to a common directory (./config)
- Create lib-folder for helper modules
- Permission management via users.csv file

## Shepherd 3.1.0

- Added `/command` command
- Refactor of storage related methods
- Add support for commands.csv file

## Shepherd 3.0.1

- Change versioning to "semantic versioning" with 3 Elements to a version number (MAJOR.MINOR.PATCH)
- Update logging for shutdown command
- Bugfix: fix check for number of arguments on shutdown command

## Shepherd 3.0

- First version of Shepherd after fork from Wolbot
- All mentions of wolbot changed to Shepherd
- Added `/shutdown` command (running over SSH)
- Add fields hostname, port and username to machines file (for SSH connections)
- Added MIT License

## 2.2

- Added the `/ip` command
- Added config entries for `/ip` command: `IP_WEBSERVICE`, `IP_REGEX`

## 2.1

- If `/wake` is called and there is only one machine stored in the machine list
    that one will automatically be selected

## 2.0

- The bot now displays a selection menu when no argument to `/wake` is provided
- A lot of new logging has been added
- Each machine now gets a persistent numerical ID
    which is also stored in the savefile
- The savefile format has been updated to include the ID
- The savefile now supports a savefile version to prevent errors
    when reading an outdated savefile version

