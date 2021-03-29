import enum

class HTTPMethod(str, enum.Enum):
    GET = 1
    POST = 2
    PATCH = 3
    DELETE = 4