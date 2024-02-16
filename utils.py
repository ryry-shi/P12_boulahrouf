from typing import Any, Callable
import re
import bcrypt
import datetime


def get_choice(message):
    
    while True:
        print(message)
        affiliation = input()
        try:
            affiliation_val = int_validator(affiliation)
            if affiliation_val in {1, 2, 3} :
                return affiliation_val
        except ValueError:
            return None
        affiliation = input("Choix invalide. Veuillez entrer un numéro valide!!! ")


def permission_validation():
    message = "Votre rôle: commercial - 1, support - 2, gestion - 3"
    affiliation_val = get_choice(message)
    if affiliation_val == 1:
        permission = "commercial"
    elif affiliation_val == 2:
        permission = "support"
    elif affiliation_val == 3:
        permission = "gestion"
    return affiliation_val, permission


def str_validator(value):
    if str(value) and len(value) > 6:
        return value
    else:
        return None


def telephone_validator(value):
    while True:
        try:
            if len(value) == 10:
                return value
        except ValueError:
            return None
        value = input("Rentrer un numéro de téléphone correcte")


def password_validator(value):
    while len(value) < 8:
        value = input("Mot de passe non conforme, choissisez un mot de passe supérieur a 8 caractère")
        str_validator(value)
    salt = bcrypt.gensalt()
    hashed_value = bcrypt.hashpw(value.encode('utf-8'), salt)
    return hashed_value


def int_validator(value):
    try:
        return int(value)
    except ValueError:
        return None


def email_validator(value):
    if bool(re.fullmatch(r"^(?!\.)[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", value)):
        return value


def date_validator(value):
    while True:
        value = input("YYYYMMDD ")
        date_value = datetime.datetime.fromisoformat(value)
        if date_value < datetime.datetime.today():
            return date_value
        else:
            value = input("la date de création n'est pas correcte ! YYYYMMDD")


def price_validator():    
    prix = int(input("Quel est le prix ? (un entier)"))
    rest_prix = int(input("Que rest'il a payer ? (un entier)"))
    while True:
        if prix > rest_prix:
            break
        else:
            prix = input("Quel est le prix ? ")
            rest_prix = input("Que rest'il a payer ? ")
    return prix, rest_prix


def validate_input_user(message: str, validator: Callable) -> Any:
    """ récupère entrer utilisateur vérifie entrer utilisateur renvois la valeur """
    while True:
        variable = validator(input(message))
        if variable is not None:
            return variable


def validate(list_fields: list) -> dict:
    """Fonction qui prend en paramètre une liste de champs contenant chacun un nom,
    une description et un validateur et qui retourne un dictionnaire contenant les noms
    des champs associés aux valeurs remplies par l'utilisateur  """ 
    dict_values = {}
    for field in list_fields:
        value = validate_input_user(field["description"], field["validators"])
        dict_values[field["name"]] = value
    return dict_values
