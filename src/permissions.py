# Server config
import config


def check_channel_permissions(channel, access_type):

    # Get the channel id
    channel_id = channel.id

    # If the access type is in the channel config
    if access_type in config.CHANNELS:

        # All channels are granted access
        if config.CHANNELS[access_type] == None:
            return True

        # Channel is granted access
        elif channel_id in config.CHANNELS[access_type]:
            return True

    # No access
    return False


def check_author_permissions(author, access_type):

    # Get the author id
    author_id = author.id

    # If the access type is in the user config
    if access_type in config.USERS:

        # All users are granted access
        if config.USERS[access_type] == None:
            return True

        # Author is granted access
        elif author_id in config.USERS[access_type]:
            return True

    # If the access type is in the role config
    if access_type in config.ROLES:

        # All roles are granted access
        if config.ROLES[access_type] == None:
            return True

        # Loop over the roles
        for role in author.roles:

            # Get the role id
            role_id = role.id

            # Role is granted access
            if role_id in config.ROLES[access_type]:
                return True

    # No access
    return False
