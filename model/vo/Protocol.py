import enum

class Protocol(str, enum.Enum):
    MQTT = 1
    COAP = 2