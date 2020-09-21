from time import sleep
import logging
from datetime import datetime


logging.basicConfig(level=logging.DEBUG)


if __name__ == '__main__':
    i = 1
    while True:
        logging.debug(f'{i} debug {datetime.now()}')
        logging.info(f'{i} info {datetime.now()}')
        logging.warning(f'{i} warning {datetime.now()}')
        sleep(i)

        i *= 2
