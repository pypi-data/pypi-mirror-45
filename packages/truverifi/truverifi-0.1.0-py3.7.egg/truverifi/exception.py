class trueverifiException(Exception):
    pass

class InvalidAPIKeyException(trueverifiException):
    pass

class trueverifiAPIError(trueverifiException):
    pass