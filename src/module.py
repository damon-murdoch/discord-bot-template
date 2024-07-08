## External Modules ##

import glob
import sys
import os
import urllib3
import importlib.util

## Internal Module ##

from src.permissions import check_author_permissions, check_channel_permissions

import src.constant as constant
import src.log as log

# Configuration File
import config

# Given a list of modules,
# generates a help message listing
# all of the available modules.

# Get helps for all commands on the server
# (or, if a search string is provided, help
# for all commands matching the provided
# string.)

# List of modules
LOADED_MODULES = []


def get_help(modules, args):

    # Will be joined at the end
    helpmsg = [
        f"{config.BOT_NAME} Version {config.BOT_VERSION} [{constant.TEMPLATE_VERSION}]",
        "=================================\n",
    ]

    # Any arguments provided
    if len(args) > 0:

        # Add arguments to the help message
        helpmsg.append(f"Search: {', '.join(args)}")

    # Convert the args array to a tuple
    args = tuple(args)

    # Loop over the modules
    for module in modules:

        # Default: Not found
        found = False

        # Search is not null
        if len(args) > 0:

            # Loop over all of the names
            for name in module.names:

                # Name starts with any arg
                if name.startswith(args):

                    # Set found to true
                    found = True

                    # Break the loop
                    break

        else:  # Search is null

            # Found by default
            found = True

        # Search string is found
        if found:

            try:
                # Add the command help to the string

                # Basic Info
                helpmsg.append(
                    f"{module.__name__} ({','.join(module.names)}): {module.desc}",
                )

                # Arguments
                helpmsg.append(f"args: {' '.join(module.args)}")

                # Loop over the examples
                for example in module.examples:

                    # Not all commands will have these, but the array is REQUIRED.
                    helpmsg.append(
                        f"example: {config.COMMAND_PREFIX}{module.names[0]} {example}"
                    )

                # Padding
                helpmsg.append("")

            # Failed to generate help msg
            except Exception as e:
                log.write_log(
                    f"Failed to generate help for {module.__name__}: {str(e)}",
                    "warning",
                )

    # Return the help message
    return "\n".join(helpmsg)


# Given a filename, imports
# the given module and returns it.


def import_file(filename):

    # Get the filename (minus extension) for the module
    name = os.path.splitext(os.path.basename(filename))[0]

    # Get the module spec from the file path
    spec = importlib.util.spec_from_file_location(name, filename)

    # Module loader
    loader = importlib.util.LazyLoader(spec.loader)

    # Import the module using the module spec
    module = importlib.util.module_from_spec(spec)

    # Add the module to the system modules
    sys.modules[name] = module

    # Execute the module
    loader.exec_module(module)

    # Return the imported module
    return module


# Given a folder, imports all
# of the modules in the given folder


def import_modules(path, recurse=True):

    # List of module files
    modules = []

    # Get all of the python files in the folder (recursively if set)
    items = glob.iglob(os.path.join(path, "**"), recursive=recurse)

    # Loop over the items
    for item in items:

        try:
            # If the file is a python file
            if os.path.splitext(item)[-1] == ".py":

                # Attempt to import the module file
                modules.append(import_file(item))

                log.write_log(f"Imported: {item}", "success")

        except Exception as e:
            log.write_log(f"Failed to import module! {str(e)}", "error")

    # Return the modules list
    return modules


def load_modules(path):

    # Use global variable
    global LOADED_MODULES

    # If the modules folder does not exist
    if not os.path.isdir(path):

        # Create the folder (or folders)
        os.makedirs(path, exist_ok=True)

    # Update loaded modules list
    LOADED_MODULES = import_modules(path, config.MODULE_RECURSE)

    # Get the number of modules
    num_modules = len(LOADED_MODULES)

    # Return module count
    return num_modules


def process_command(command, args, author, channel):

    # Use global variable
    global LOADED_MODULES

    try:  # Main Process

        # Get loaded modules
        modules = LOADED_MODULES

        # Special Case: Help Command
        if command == "help":
            return get_help(modules, args)

        # Loop over the modules
        for module in modules:

            # Check if the command matches any of the aliases
            if command in module.names:

                # Dereference access type
                access_type = module.access_type

                # Check if channel has access to the command
                if check_channel_permissions(channel, access_type) == False:
                    raise Exception(
                        f"Unrecognised command: '{command}'"
                    )  # Do not leak commands

                # Check if the author has access to the command
                if check_author_permissions(author, access_type) == False:
                    raise Exception(
                        f"You do not have access to this command"
                    )  # More useful error

                # Execute the command
                result = module.exec(args, author, channel)

                # If an error occured
                if result["error"]:
                    raise Exception(result["error"])

                # Otherwise, return the result
                return result["result"]

        # Command was not found
        raise Exception(f"Unrecognised command: '{command}'")

    # General failure
    except Exception as e:

        # Generate the error message
        errmsg = f"Failed: {str(e)}"

        log.write_log(errmsg, "error")

        # Return the exception
        return f"{errmsg}! For a list of valid commands, please use 'help'."
