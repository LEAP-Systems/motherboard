#!/usr/bin/python3

import sys
import serial
import getopt
import logging
import time
from typing import Union


def demo(ser: serial.Serial) -> None:
    try:
        while True:
            for byte in [[x] for x in range(256)]:
                print("Loading -> {}".format(byte))
                ser.write(bytes(byte))
                time.sleep(0.1)
    except KeyboardInterrupt:
        sys.exit()


def main(argv) -> None:
    serial_port: Union[str, None] = None
    try:
        opts, _ = getopt.getopt(argv, "p:", ["port="])
    except getopt.GetoptError:
        logging.exception("./monitor.py -p $SERIAL_PORT")
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-p", "--port"):
            serial_port = arg
    try:
        ser = serial.Serial(
            port=serial_port,
            baudrate=9600,
            timeout=10
        )
    except serial.SerialException as exc:
        logging.exception("Failed to initialize arduino serial monitor\n%s", exc)
        sys.exit(1)
    demo(ser)
    logging.info("Initialized arduino serial monitor on port %s", serial_port)


if __name__ == "__main__":
    logging.basicConfig(format="%(asctime)s %(levelname)s: %(message)s", level=logging.INFO)
    main(sys.argv[1:])
