"""
    Purpose:
        User Input Helpers.

        This library is used to prompt the user for input and handle the inputs
"""

# Python Library Imports
import logging


###
# General Helpers
###


def get_input_from_user(prompt=None, max_input=50):
    """
    Purpose:
        Get input from the user until user exits for max input is reached
    Args:
        prompt (String): Prompt for the user. Use default if not set
        max_input (Int): Max number of user input before auto-exit
    Yields:
        user_input (String): string input by the user
    """

    end_strings = ('end', 'exit', 'e', 'stop', 'quit', 'q')
    if not prompt:
        prompt = f"Enter Some Data ({','.join(end_strings)} to end): "

    total_user_input = 0
    while True:
        if total_user_input >= max_input:
            logging.info(f"Max number of input ({max_input}) has been reached")
            break
        else:
            total_user_input += 1

        user_input = input(prompt).rstrip()
        if user_input in end_strings:
            logging.info(f"User has chosen to exit with msg: {user_input}")
            break
        else:
            logging.info(f"Got input from user: {user_input}")
            yield user_input
