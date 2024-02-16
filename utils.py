from typing import Any, Callable
import re
import bcrypt
import datetime

import sentry_sdk


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


def get_name_email():
    return [
        {
            "name": "nom",
            "description": "Entrer le nom du client ! ",
            "validators": str_validator,
        },
        {
            "name": "email",
            "description": "Entrer l'email du client ! ",
            "validators": email_validator,
        },
    ]


def post_client_info(session, value_session, list_field, creation, maj_contact):
    for i in value_session:
        i.nom = (list_field["nom"],)
        i.email = (list_field["email"],)
        i.telephone = (list_field["telephone"],)
        i.entreprise = (list_field["entreprise"],)
        i.creation = (creation,)
        i.maj_contact = (maj_contact,)
        i.contact = (i.contact,)
        session.add(i)
        session.commit()
    sentry_sdk.capture_message(i)

def get_id_contrat():
    return int(input("Quel est le numéro du contrat ? "))


def get_contrat_signed(rest_prix):
    print(rest_prix, "a")
    if rest_prix == 0:
        status = True
    else:
        status = False
    return status


def create_user_obj():
    list_fields = [
        {"name": "nom", "description": "Entrer votre nom : ", "validators": str_validator},
        {"name": "password", "description": "Entrer votre mot de passe : ", "validators": password_validator},
        {"name": "email", "description": "Entrer votre email : ", "validators": email_validator},
    ]
    user_values = validate(list_fields)
    affiliation, permission = permission_validation()
    return user_values, affiliation, permission


def create_epic_client_objet():
    list_fields = [
        {"name": "nom", "description": "Entrer votre nom :", "validators": str_validator},
        {"name": "entreprise", "description": "Entrer le nom de l'entreprise : ", "validators": str_validator},
        {"name": "telephone", "description": "Entrer votre numéro de télephone : ", "validators": telephone_validator},
        {"name": "email", "description": "Entrer votre email: ", "validators": email_validator},
        {"name": "contact", "description": "Entrer votre contact: ", "validators": str_validator}]
    values_dict = validate(list_fields)
    return values_dict


def create_evenement_objet_update():
    list_fields = [
        {"name": "contrat_id", "description": "numéro du contrat ! ", "validators": str_validator},
        {"name": "client_name", "description": "nom du client ! ", "validators": str_validator},
        {"name": "client_contact", "description": "email du client ! ", "validators" : int_validator},
        {"name": "location", "description": "Description du lieu et précision ! ", "validators" : str_validator},
        {"name": "attendes", "description": "le nombre d'invités ? ", "validators" : int_validator},
        {"name": "NOTES", "description": "Notes de l'évenement ! ", "validators" : str_validator},]
    values_dict = validate(list_fields)
    return values_dict


def create_evenement_objet():
    list_fields = [
        {"name": "location", "description": "La location de l'évenement ? ", "validators": str_validator},
        {"name": "attendes", "description": "le nombre d'invités ? ", "validators" : int_validator},
        {"name": "NOTES", "description": "Description du lieu et précision !", "validators" : str_validator}]
    values_dict = validate(list_fields)
    return values_dict


def create_contrat_objet():
    list_fields = [
        {"name": "information_id", "description": "information client ? ", "validators": int_validator},
        {"name": "contact", "description": "information collaborater du client ? ", "validators": str_validator},
        {"name": "prix", "description": "prix du contrat ?", "validators": int_validator},
        {"name": "rest_prix", "description": "reste a payer du contrat ?", "validators": int_validator},
        {"name": "creation", "description": "creation du contrat ?", "validators": int_validator},
    ]
    values_dict = validate(list_fields)
    return values_dict


def get_name_email_collabo():
    return [
        {
            "name": "nom",
            "description": "le nom du collabo",
            "validators": str_validator,
        },
        {
            "name": "email",
            "description": "email du collabo",
            "validators": email_validator,
        },
    ]

def validate_prix():
    prix = int(input("Quel est le prix ? (un entier)"))
    rest_prix = int(input("Que rest'il a payer ? (un entier)"))
    while True:
        if prix > rest_prix:
            break
        else:
            prix = input("Quel est le prix ? ")
            rest_prix = input("Que rest'il a payer ? ")
    return prix, rest_prix

import datetime


def validate_value_two_date(message, message_two):
    datetime_start_evenement = datetime.datetime.fromisoformat(input(message))
    datetime_end_evenement = datetime.datetime.fromisoformat(input(message_two))
    while True:
        if datetime_start_evenement < datetime_end_evenement:
            break
        else:
            datetime_start_evenement = input("Les dates sont incorrecte! Veuillez entrez des dates correctes!! ")
            datetime_end_evenement = input("La date de fin de l'évènement n'est pas correcte ! ")
    return datetime_start_evenement, datetime_end_evenement


def validate_value_date_contrat():
    while True:
        date = input("la création du contrat ? ")
        date_value = datetime.datetime.fromisoformat(date)
        if date_value < datetime.datetime.today():
            return date_value
        else:
            date = input("la date de création n'est pas correcte ! ")

def val_function_int(value):
    list_number = list(range(1, 100))
    for i in range(1, 100):
        for y in list_number:
            if str(y) == value:
                return int(value)
        else:
            value = input("rentrer un id correcte")


import bcrypt


def validate_value_date_user():
    username = input("Choissisez votre nom ? ")
    while len(username) < 6:
        if username == str and len(username) > 14:
            break
        else:
            print("Votre nom est trop court")
            username = input("")
    password = input("Choissisez votre mot de passe ? ")
    password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return username, password
