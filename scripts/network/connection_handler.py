from client.client import Client
import server_properties

import socket
import threading
import logging

def init():
    create_connection_handlers()

def create_connection_handlers():
    # create main socket
    main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    main_socket.settimeout(None)
    main_socket.bind((server_properties.IP, server_properties.PORT))
    main_socket.listen(server_properties.MAX_PLAYER_COUNT)

    # create thread for handle_main_connections
    thread = threading.Thread(target=handle_connections, args=(main_socket,))
    thread.start()

    logging.info("Socket is running on port: " + str(server_properties.PORT))

def handle_connections(main_socket):
    while True:
        socket, ip_and_port = main_socket.accept()

        ip = ip_and_port[0]
        port = ip_and_port[1]

        logging.info(f"User connected from ip: {ip}, port: {port}")

        # create client object
        clien_object = Client(socket, ip, port)

        # start handle_main_packages thread from client
        handle_client_thread = threading.Thread(target=clien_object.client_package_handler.handle_packages, args=())
        handle_client_thread.start()
