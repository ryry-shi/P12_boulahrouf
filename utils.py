from typing import Any, Callable, Dict, List
import re
import os
from datetime import datetime


def str_validator(value: str, min_length: int = 6) -> str | None:
    """"
        Valide l'entrée utilisateur pour retourner une chaîne de caractère de moins de 6 de longueur
        Renvoi None sinon
    """
    if not value:
        return None
    if len(value) < min_length:
        raise ValueError()
    return value


def phone_validator(value: str) -> str:
    """"
        Valide l'entrée utilisateur pour retourner un numéro de téléphone
        Renvoi None sinon
    """
    if not value:
        return None
    if not (value.isnumeric() and len(value) == 10):
        raise ValueError()
    return value


def password_validator(value: str) -> bytes:
    """
        Valide l'entrée utilisateur pour retourner le hash du mot de passe d'une longueur au minimum de 8 caractères
        Renvoi None sinon
    """
    return str_validator(value, 8)


def int_validator(value: str) -> int | None:
    """
        Valide l'entrée utilisateur pour retourner un entier
        Renvoi None sinon
    """
    if not value:
        return None
    if not value.isnumeric():
        raise ValueError()
    return int(value)


def email_validator(value: str) -> str | None:
    """
        Valide l'entrée utilisateur pour retourner une adresse email
        Renvoi None sinon
    """
    if not value:
        return None
    if not bool(re.fullmatch(r"^(?!\.)[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", value)):
        raise ValueError()
    return value
    

def date_validator(value: str) -> datetime | None:
    """
        Valide l'entrée utilisateur pour retourner une date
        Renvoi None sinon
    """
    if not value:
        return None
    return datetime.fromisoformat(value)


def future_date_validator(value: str) -> datetime | None:
    """
        Valide l'entrée utilisateur pour retourner une date
        Renvoi None sinon
    """
    if not value:
        return None
    value_date = date_validator(value)
    if value_date < datetime.today():
        raise ValueError()
    return value_date


def past_date_validator(value: str) -> datetime | None:
    """
        Valide l'entrée utilisateur pour retourner une date
        Renvoi None sinon
    """
    if not value:
        return None
    value_date = date_validator(value)
    if value_date > datetime.today():
        raise ValueError()
    return value_date

def two_date_validator(first_value: str, second_value: str) -> datetime:
    """
        Valide les deux entrées utilisateurs pour retourner deux dates dont la seconde est postérieure à la première
    """
    first_date_value = datetime.fromisoformat(first_value)
    second_date_value = datetime.fromisoformat(second_value)
    if first_date_value >= second_date_value:
        raise ValueError("La seconde date doit être postérieure à la première")
    return first_date_value, second_date_value


def positive_int_validator(value: str) -> int | None:
    """
        Valide l'entrée utilisateur pour retourner un prix
        Renvoi None sinon
    """
    if not value:
        return None
    int_value = int_validator(value)
    if int_value < 0:
        raise ValueError()
    return int_value


def user_input(message: str, validator: Callable) -> Any:
    """
        Récupère l'entrée utilisateur validée
    """
    while True:
        try:
            variable = validator(input(f"{message} ? "))
        except ValueError:
            continue
        return variable


def submit_form(title : str, fields: List[Dict[str, str | Callable]]) -> dict:
    """
        Soumet un formulaire et attend qu'on le remplisse
        Renvoi un dictionnaire avec les réponses données
    """ 
    data = {}
    clear_screen()
    print(f".: {title} :.")
    for field in fields:
        data[field["name"]] = user_input(field["description"], field["validator"])
    return data


def ask_user_choice(nb_of_options: int) -> int:
    """
        Demande à l'utilisateur d'entrer un choix parmis des options
    """
    while True:
        try:
            choice = int_validator(input("Choix ? "))
            if choice and choice > 0 and choice <= nb_of_options:
                return choice - 1
        except ValueError:
            pass


def clear_screen():
    os.system("cls")
