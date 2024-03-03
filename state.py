class State:

    def __init__(self) -> None:
        self.data = {}

    def read(self, key):
        return self.data[key]
    
    def save(self, key, value):
        self.data[key] = value


app_state = State()

def read(key):
    return app_state.read(key)

def save(key, value):
    app_state.save(key, value)
