class UcaCoinException(Exception):
    msg = ""

    def __init__(self, msg=""):
        self.msg = msg


# ----- Usuarios ------
class BlockchainRegisterException(UcaCoinException):
    pass
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


# ----- Transacciones ------
class BlockchainTransferError(UcaCoinException):
    pass

