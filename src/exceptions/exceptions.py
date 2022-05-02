class IncorrectUserPassword(Exception):
    def __init__(self, message="¡Upss!, usuario o contraseña incorrectos"):
        super(IncorrectUserPassword, self).__init__(message)


class UserAlreadyExists(Exception):
    def __init__(self, message="¡Upss!, el usuario ya existe, intenta con otro"):
        super(UserAlreadyExists, self).__init__(message)


class ComicNotFound(Exception):
    def __init__(self, message="¡Upss!, no tenemos registro de este comic"):
        super(ComicNotFound, self).__init__(message)


class UserComicNotFound(Exception):
    def __init__(self, message="El usuario no tiene comics por mostrar"):
        super(UserComicNotFound, self).__init__(message)
