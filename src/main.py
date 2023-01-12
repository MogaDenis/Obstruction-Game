from ui.console_ui import ConsoleUI
from ui.graphical_ui import GraphicalUI
import os
from settings.settings import Settings


class InvalidInputException(Exception):
    pass


def display_title():
    
    print("""
     ___  _         _                   _   _             
    / _ \| |__  ___| |_ _ __ _   _  ___| |_(_) ___  _ __  
   | | | | '_ \/ __| __| '__| | | |/ __| __| |/ _ \| '_ \ 
   | |_| | |_) \__ \ |_| |  | |_| | (__| |_| | (_) | | | |
    \___/|_.__/|___/\__|_|   \__,_|\___|\__|_|\___/|_| |_|
        """)

    print("\n~ Choose the interface you want to use:\n")
    print("\t1 - Graphical User Interface")
    print("\t2 - Console User Interface")
    print("\t0 - Close the application\n")


def read_choice():
    """
        This function reads the user's main menu choice.

    :raises InvalidInputException: Exception raised if the input is invalid. 
    :return: The user's input.
    """
    choice = input(">> ") 

    if choice not in ['0', '1', '2']:
        raise InvalidInputException

    return choice


def invalid_input_message():
    return "Invalid input!\n"


if __name__ == "__main__":
    error_message = None
    last_winner = None
    settings = Settings()

    config = settings.read_file()

    last_winner = config['last_winner']

    while True:
        try:
            os.system('cls')
            display_title()

            if error_message is not None:
                print(error_message)
                error_message = None

            user_choice = read_choice()

            break

        except InvalidInputException:
            error_message = invalid_input_message()

    if user_choice != '0':
        if user_choice == '1':
            user_interface = GraphicalUI(last_winner)
        else:
            user_interface = ConsoleUI(last_winner)
    
        last_winner = user_interface.start()

    settings.write_file(last_winner)