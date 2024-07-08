# Discord Library
import discord

# Logging
import log

# Constant values
import constant

# Sends a file to the channel


async def send_file(file, channel):

    try:

        # Send the response to the client
        await channel.send("Response received:", file=discord.File(file))

    # General failure
    except Exception as e:

        log.write_log(f"Failed to send response: {str(e)}", "error")


# Sends a message to the channel
async def send_message(message, channel, size = constant.MAX_MESSAGE_LENGTH):

    try:

        # Message size limit
        # Allows us to fit the code block characters
        limit = min(constant.MAX_MESSAGE_LENGTH - 7, size)

        # Character length of the current message
        length = 0

        # List of messages to send to the client
        messages = []

        # Next message we are building
        next = []

        # Loop over all of the lines in the message
        for msg in message:

            # Split the message on any newlines
            for line in msg.split("\n"):

                # Create a copy of the line
                line_cpy = line

                # If this line is longer than the character limit
                while len(line_cpy) > limit:

                    # If there is anything in the next array
                    if next:

                        # Add the current 'next' message
                        # to the messages list, after joining
                        # the string on the newline character
                        messages.append("\n".join(next))

                    # Set the next list to the new message
                    next = [line_cpy[:limit]]

                    # Remove the added content from the full message
                    line_cpy = line_cpy[limit:]

                # Verify this row would not make
                # the current next message

                # Get the length of the current line
                curlen = len(line_cpy)

                # If the curlen + the length property would break the limit
                if length + curlen > limit:

                    # If there is anything in the next array
                    if next:

                        # Add the current 'next' message
                        # to the messages list, after joining
                        # the string on the newline character
                        messages.append("\n".join(next))

                    # Set the next list to the new message
                    next = [line_cpy]

                    # Set the length property to the current length
                    length = curlen

                else:  # New message would not break the limit

                    # Add the line to the next array
                    next.append(line_cpy)

                    # Add the current length to the total length
                    length += curlen

            # If there is anything in the next array
            if next:

                # Add the current 'next' message
                # to the messages list, after joining
                # the string on the newline character
                messages.append("\n".join(next))

            # Loop over all of the messages
            for message in messages:

                # Send the message to the channel
                await channel.send(message)

    # General failure
    except Exception as e:

        log.write_log(f"Failed to send response: {str(e)}", "error")
