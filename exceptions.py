class UcaCoinException(Exception):
    msg = ""

    def __init__(self, msg=""):
        self.msg = msg


# ----- Usuarios ------
class UserNotExistException(UcaCoinException):
    pass


class UserIsLoggedException(UcaCoinException):
    pass

# ---------------------
