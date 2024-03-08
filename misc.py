from state import read


def create_or_update(object):
    """ Crée ou MAJ un objet """
    read("session").add(object)
    read("session").commit()


def delete(object):
    """ Supprime un objet """
    read("session").delete(object)
    read("session").commit()
