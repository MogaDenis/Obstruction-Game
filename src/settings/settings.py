from config.definitions import ROOT_DIR
import os


class Settings:
    def __init__(self):
        pass

    def read_file(self):
        """
            This method opens the settings.properties file and reads it, returning a dictionary having as keys the fields and as values
        the corresponding setting.

        :return: Dictionary 
        """
        open_file = open(os.path.join(ROOT_DIR, "settings/settings.properties"), 'r')

        lines = open_file.readlines()
        config = {}

        for line in lines:
            tokens = line.split(' ')

            key = tokens[0]
            key = key.replace(':', '')

            value = tokens[1]

            config[key] = value

        open_file.close()

        return config

    def write_file(self, winner):
        """
            This method opens the settings.properties file and writes to it the winner of the previous game. 

        :param winner: String
        """
        open_file = open(os.path.join(ROOT_DIR, "settings/settings.properties"), 'w')

        if winner is None:
            winner = 'computer'

        open_file.write('last_winner: ' + winner)

        open_file.close()