#
# Copyright (C) 2019 James Parkhurst
#
# This code is distributed under the BSD license.
#
import getpass


class HalError(RuntimeError):
    """
    A sci-fi error message!

    Example:

        >>> def open_pod_bay_doors():
        ...     raise HalError("Open the pod bay doors, HAL.")

    """

    def __init__(self, message="", template=None):
        """
        Initialise the exception

        The template argument if present should be a format string containing:
            - message: the error message
            - username: the username

        The default template is: 
            {message}\\\\n\\\\nI'm sorry, {username}. I'm afraid I can't do that.

        Args:
            message (str): The exception message.
            template (str): The exception template. 

        """

        # Get the username
        try:
            username = getpass.getuser()
        except Exception:
            username = "Dave"

        # Get the template
        if template is None:
            template = "{message}\n\nI'm sorry, {username}. I'm afraid I can't do that."

        # Put in HAL error text.
        text = template.format(username=username, message=message)

        # Init base class
        super().__init__(text)
