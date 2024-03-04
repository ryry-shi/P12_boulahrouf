from state import read

def create_or_update(object):
    read("session").add(object)
    read("session").commit()

def delete(object):
    read("session").delete(object)
    read("session").commit()
