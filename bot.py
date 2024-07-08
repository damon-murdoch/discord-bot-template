# OS Library
import os

# Logging Module
import src.log as log

# Discord bot config
import config as config

# Discord Bot Library
from discord.ext import commands

# Discord Intents (i.e. Required Permissions)
from src.intents import intents as bot_intents

# Bot response functions
import src.response as bot_response

# Bot command processing / module loading functions
from src.module import load_modules, process_command

# Constant Values
import src.constant as constant

# Create discord bot
bot = commands.Bot(intents=bot_intents)

# Bot root directory
BOT_FOLDER = os.path.dirname(os.path.realpath(__file__))


@bot.event
async def on_ready():

    # Get the path to the module folder
    module_folder = os.path.join(BOT_FOLDER, config.MODULE_FOLDER)

    # Attempt to load the modules
    module_count = load_modules(module_folder)

    log.write_log(
        f"Discord bot '{config.BOT_NAME} 'started! Version: {config.BOT_VERSION} [{constant.TEMPLATE_VERSION}]",
        "success",
    )

    log.write_log(f"Modules loaded: {module_count}")


@bot.event
async def on_message(message):
    try:

        # Get the message content (string), removing leading/trailing space
        content: str = str(message.content).strip()

        # If the message content starts with the prefix
        if content.startswith(config.COMMAND_PREFIX):

            # Get message author
            author = message.author

            # Get message channel
            channel = message.channel

            # If the author is a bot
            if author.bot == True:
                raise Exception(
                    "Commands sent by bots will will be ignored to prevent recursion!"
                )

            # Split the command into tokens and remove the prefix
            tokens = content[len(config.COMMAND_PREFIX) :].split("")

            # Command name is the first token
            command = tokens[0]

            # Arguments are the following tokens
            args = tokens[1:]

            # Process the command
            result = process_command(command, args, author, channel)

            # Result is returned
            if result:

                # (Optional) file to send to the client
                file = None

                # Message to send to the client
                msg = ""

                # Message is a filename
                if os.path.isfile(result):

                    # Set the file to the result path
                    file = result

                else:  # Message is not a filename

                    # Set the message to the result
                    msg = result

                # File is defined
                if file:

                    # Send the file to the client
                    await bot_response.send_file(file, channel)

                else:  # No file defined

                    # Send the message to the channel
                    await bot_response.send_message([msg], channel, config.MESSAGE_LENGTH)

                log.write_log(f"Response Received: {msg}", "general")

            else:  # No response received

                msg = "No response received!"

                # Send the message to the channel
                await bot_response.send_message([msg], channel, config.MESSAGE_LENGTH)

                log.write_log(msg, "error")

    except Exception as e:  # Failed to process message
        log.write_log(f"Failed to handle message! {str(e)}", "error")


# Check config for discord token
token = config.DISCORD_TOKEN
if token:
    # Start the bot
    bot.run(token)
else:  # No token
    raise Exception(
        "No discord token! Please set DISCORD_TOKEN in config.py!"
    )
