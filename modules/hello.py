# Command Name / Aliases
names = ["hello", "h"]

# Command description
desc = "Displays a simple greeting"

# Arguments
args = ["none"]

# Example
examples = []

# Basic access
access_type = "basic"


def exec(args, author, channel):

    # Result object
    result = {"error": None, "result": None}

    try:

        # Author nickname
        name = author.nick

        # Set the result to the hello message
        result["result"] = f"Hello {name}!"

    # General failure
    except Exception as e:

        # Set the error to the message
        result["error"] = str(e)

    # Return the result object
    return result
