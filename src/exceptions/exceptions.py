class IncorrectUserPassword(Exception):
    def __init__(self, message="¡Upss!, usuario o contraseña incorrectos"):
        super(IncorrectUserPassword, self).__init__(message)


class UserAlreadyExists(Exception):
    def __init__(self, message="¡Upss!, el usuario ya existe, intenta con otro"):
        super(UserAlreadyExists, self).__init__(message)
