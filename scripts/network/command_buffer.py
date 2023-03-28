import logging

DELIM_ARGUMENTS_SYMBOL = ";"

class CommandBuffer:
    def __init__(self, command_string):
        self.splitted_command = command_string.split(DELIM_ARGUMENTS_SYMBOL)
        self.current_argument_index = 0

    def read_next_argument(self):
        if len(self.splitted_command) >= self.current_argument_index:
            logging.error("No more arguments left.")
            raise Exception('')

        self.current_argument_index += 1
        return self.splitted_command[self.current_argument_index - 1]

    def get_argument_with_index(self, index):
        return self.splitted_command[index]

    def to_string(self):
        out = ""

        for argument in splitted_command:
            out += argument + ";"

        return out
