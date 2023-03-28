from network import ddos_protection
from network import connection_handler
import logging

def main():
    logging.basicConfig(format='[%(asctime)s][%(filename)s:%(lineno)d][%(levelname)s] %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.DEBUG)
    connection_handler.init()

main()
