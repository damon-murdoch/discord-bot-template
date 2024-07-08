# Discord Bot Template

## Expandable Discord Bot Template
### Created By Damon Murdoch ([@SirScrubbington](https://github.com/SirScrubbington))

## Description

This project is a simple Discord bot written in Python, designed as a template to be easily expandable with custom modules. The bot includes basic functionalities and can be enhanced by adding new module files to the 'modules' directory.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Problems / Improvements](#problems--improvements)
- [Changelog](#changelog)
- [Sponsor this Project](#sponsor-this-project)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/damon-murdoch/discord-bot-template
   cd discord-bot-template
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Copy the example configuration file and update it as required
   ```
   cp config.example.py config.py
   ```

4. Add your discord token to your `config.py` file
    ```
    DISCORD_TOKEN=my-discord-token
    ```

5. Configure discord permissions
    ```
    # Channel Access
    CHANNELS = {
        'basic': None # All channels
    }

    # Role Access
    ROLES = {
        'basic': [discord-role-id] # Role with id 'discord-role-id'
    }

    # User Access
    USERS = {
        'basic': [] # Nobody
    }
    ```

## Usage

1. Run the bot:
   ```bash
   python bot.py
   ```

2. The bot will be online and ready to use. Add custom modules to the 'modules' directory to expand its functionality.

### Example Command

A basic sample command, `hello.py` has been provided for you. The following properties are required for all command files:

```
# Command Name / Aliases
names = ["sample-name", "sample-alias"]

# Command description
desc = "A simple command description"

# Arguments
args = ["none"]

# Example
examples = []

# Access Type
# This value can be set to any string - However, you will need to add
# custom permissions for new values to the the USERS, CHANNELS and ROLES
# sections in your config.py for the command to be available.
access_type = "basic"


def exec(args, author, channel):
    
    # Result object
    result = {"error": None, "result": None}

    ...
    Do some things in here :)
    ...

    # Return the result object
    return result
```

If the `result` property of the returned object contains a valid filename on the host system, 
the file will be sent to the channel the command was sent from. Otherwise, the `result` property
will be assumed to be a message string and will be sent as a message to the channel.

## Problems / Improvements

If you have any suggested improvements for this project or encounter any issues, please feel free to open an 
issue [here](../../issues) or send me a message on Twitter detailing the issue and how it can be replicated.

## Changelog

### Ver. 0.1.0

- Initial release with basic bot functionality and module support.

## Sponsor this Project

If you'd like to support this project and other future projects, please feel free to use the PayPal donation link below.
[https://www.paypal.com/paypalme/sirsc](https://www.paypal.com/paypalme/sirsc)
