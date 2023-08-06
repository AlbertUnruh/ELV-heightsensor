__all__ = (
    "BUS_CONNECTION",
    "AUTODETECT_IF_NOT_FOUND",
    "AUTODETECT_MATCH_HINT",
    "AUTODETECT_PATTERN",
    "AUTODETECT_COMMAND",
    "SERIAL_KWARGS",
)


import re


BUS_CONNECTION: str = "/dev/ttyUSB0"  # "MISSING"  # "/dev/bus/usb/001/010"

# can only detect usb-bus by now, but only tty works, so this is kinda useless...
AUTODETECT_IF_NOT_FOUND: bool = True
AUTODETECT_MATCH_HINT: bytes = (
    b"Silicon Labs CP210x UART Bridge"  # /!\ change this line /!\
)
AUTODETECT_PATTERN: re.Pattern[bytes] = re.compile(
    rb"^Bus (\d{3}) Device (\d{3}): ID ([\da-f]{4}:[\da-f]{4}) (%b)$"
    % AUTODETECT_MATCH_HINT,
    re.MULTILINE,
)
AUTODETECT_COMMAND: list[str] = [
    "lsusb",  # if you change it make sure the pattern still works!
]

SERIAL_KWARGS: dict[str, ...] = {"baudrate": 115200, "timeout": 0}
