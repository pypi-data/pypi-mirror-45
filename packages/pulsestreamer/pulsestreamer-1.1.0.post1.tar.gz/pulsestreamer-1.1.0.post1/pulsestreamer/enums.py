
from enum import Enum


class Serial(Enum):
    ID = 0
    MAC = 1

class ClockSource(Enum):
    INTERNAL = 0
    EXT_125MHZ = 1
    EXT_10MHZ = 2

class TriggerStart(Enum):
    IMMEDIATE = 0
    SOFTWARE = 1
    HARDWARE_RISING = 2
    HARDWARE_FALLING = 3
    HARDWARE_RISING_AND_FALLING = 4

class TriggerRearm(Enum):
    AUTO = 0
    MANUAL = 1