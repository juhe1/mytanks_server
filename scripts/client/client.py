from network.command_buffer import CommandBuffer
import server_properties

import logging
import socket

class Client:
    def __init__(self, socket, ip, port):
        self.client_package_handler = ClientPackageHandler(socket, ip, port)


KEYS = [1,2,3,4,5,6,7,8,9]
DELIM_COMMANDS_SYMBOL = "end~"

class ClientPackageHandler:
    def __init__(self, socket, ip, port):
        self.socket = socket
        self.ip = ip
        self.port = port
        self.last_key = 1

    def user_disconnected(self):
        logging.info(f"User disconnected from ip: {self.ip}, port: {self.port}")
        # TODO: dispatch user disconnect event

    def send_command_buffer(self, command_buffer):
        command_string = command_buffer.to_string()
        logging.debug(f"Sended command: {command_string}")

        try:
            self.socket.sendall(command_string)
        except socket.error as e:
            self.user_disconnected()

    def decrypt(self, string):
        key = (self.last_key + 1) % len(KEYS)
        if key <= 0:
            key = 1

        self.last_key = key
        new_string = ""

        for char in string:
            new_string += chr(ord(char) - (key + 1))

        return new_string[1:]

    def send_aes_data(self):
        aes_string = ""

        with open(server_properties.AES_SWF_PATH, "rb") as f:
            byte = f.read(1)
            while byte != b"":
                aes_string += "," + str(int.from_bytes(byte))
                byte = f.read(1)

        self.send_command_buffer(CommandBuffer("system;" + aes_string[1:]))

    def handle_system_command(self, command_buffer):
        command_name = command_buffer.read_next_argument()

        if command_name == "get_aes_data":
            self.send_aes_data()

        failed = False # TODO: set_failed
        ddos_protection.command_counter.count_command(self.ip, command_buffer, failed)

    def handle_command_buffer(self, command_buffer):
        argument = command_buffer.read_next_argument()

        if command_buffer.read_next_argument() == "system":
            self.handle_system_command(command_buffer)

    def handle_command_strings(self, command_strings):
        for command_string in command_strings:
            command_string = self.decrypt(command_string)

            logging.debug(f"Received command: {command_string}")

            command_buffer = CommandBuffer(command_string)
            self.handle_command_buffer(command_buffer)

    def handle_packages(self):
        while True:
            try:
                data = self.socket.recv(server_properties.RECEIVE_BUFFER_SIZE)
            except socket.error as e:
                self.user_disconnected()
                return

            if data == b"":
                self.user_disconnected()
                return

            data_string = data.decode("utf-8")

            command_strings = data_string.split(DELIM_COMMANDS_SYMBOL)
            self.handle_command_strings(command_strings)
