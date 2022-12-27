class UcaCoinException(Exception):
    msg = ""

    def __init__(self, msg=""):
        self.msg = msg


# ----- Usuarios ------
class UserNotExistException(UcaCoinException):
    pass


class UserIsLoggedException(UcaCoinException):
    pass


class UserNotLoggedException(UcaCoinException):
    pass


class UsersExistsException(UcaCoinException):
    pass
# ---------------------



# ----- Seguridad ------
class InvalidTokenException(UcaCoinException):
    pass

