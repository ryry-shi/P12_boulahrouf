class State:

    def __init__(self) -> None:
        self.data = {}

    def read(self, key):
        return self.data[key] if key in self.data else None
    
    def save(self, key, value):
        self.data[key] = value


app_state = State()


def read(key):
    """ Lis une valeur dans l'état de l'application """
    return app_state.read(key)


def save(key, value):
    """ Sauvegarde une valeur dans l'état de l'application """
    app_state.save(key, value)
