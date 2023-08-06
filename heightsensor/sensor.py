__all__ = ("Sensor",)


import serial
import subprocess
from .constants import (
    BUS_CONNECTION,
    AUTODETECT_IF_NOT_FOUND,
    AUTODETECT_PATTERN,
    AUTODETECT_COMMAND,
    SERIAL_KWARGS,
)


class Sensor:
    connection: serial.Serial

    def connect(self) -> serial.Serial:
        try:
            self.connection = serial.Serial(port=BUS_CONNECTION, **SERIAL_KWARGS)
        except serial.SerialException as e:
            match e.errno:
                case 2:
                    if not AUTODETECT_IF_NOT_FOUND:
                        raise
                    out: bytes
                    err: bytes
                    p = subprocess.Popen(
                        AUTODETECT_COMMAND,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                    )
                    out, err = p.communicate()
                    if (result := AUTODETECT_PATTERN.match(out)) is None:
                        raise Exception(
                            f"Failed to detect serial port: {err.decode('utf-8')}"
                        )
                    bus = "/dev/bus/usb/{0}/{1}".format(
                        result.group(1).decode("utf-8"),
                        result.group(2).decode("utf-8"),
                    )
                    info = (
                        result.group(3).decode("utf-8"),
                        result.group(4).decode("utf-8"),
                    )
                    print(
                        "found following serial port: {0} ({1[0]} | {1[1]})".format(
                            bus, info
                        )
                    )
                    self.connection = serial.Serial(port=bus, **SERIAL_KWARGS)
                case _:
                    raise
        return self.connection

    def read(self, size) -> bytes:
        with self.connection:
            return self.connection.read(size)
