from utils import get_choice, int_validator, get_user_info
from .models import Client, Contrat, Evenement, Collaborater
import bcrypt


def connect():
    inp = input("Si vous n'avez pas de compte appuyez 1 !")
    if inp == str(1):
        return Collaborater.create()
    nom = input("Votre nom : ")
    password = input("Votre password : ")
    users = get_user_info(nom)
    if not users:
        print("Aucun utilisateurs trouver ! ")
        return connect()
    mdp = users[0].password
    mdp_boolean = bcrypt.checkpw(
        password=password.encode("utf-8"), hashed_password=mdp.encode("utf-8")
    )
    if mdp_boolean is True:
        user_session = get_user_info(nom)
        for i in user_session:
            print(f"Bonjour {i.nom} {i.email} {i.affiliation}")
        return i
    elif mdp_boolean is False:
        print("Erreur, le mot de passe ou le nom est incorecct ! ")
        return connect


def choice_menu_user(value):
    while True:
        choice_menu_client = get_choice("1: créer\n2: update\n3: delete\n")
        if choice_menu_client == 1:
            Collaborater.create()
        elif choice_menu_client == 2:
            Collaborater.update(value)
        elif choice_menu_client == 3:
            id = input("Choissisez le nom du collaborater a delete ! ")
            Collaborater.delete(id)


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


def choice_gestionnaire_menu(value):
    choice = get_choice("1: utilisateur\n2: contrat\n3: delete evenement\n")
    if choice == 1:
        choice_menu_user(value)
    elif choice == 2:
        choices_menu_contrat(value)
    elif choice == 3:
        Evenement.delete(value)
    else:
        pass


def choice_commercial_menu(value):
    choice = get_choice("1: client\n2: contrat\n3: Créer évenement\n")
    if choice == 1:
        choice_menu_client(value)
    elif choice == 2:
        choices_menu_contrat(value)
    elif choice == 3:
        Evenement.update(value)


def choices_command(value):
    while True:
        if not value.nom:
            return connect()
        if value.permission == "gestion":
            choice_gestionnaire_menu(value)
        if value.permission == "commercial":
            choice_commercial_menu(value)
        else:
            pass


def choices_menu_contrat(session, value):
    if value.permission == "commercial" or "gestion":
        message = "create: 1\nmaj: 2\ndel: 3\n"
        choices = get_choice(message)
        if choices == 1:
            Contrat.create()
        elif choices == 2:
            Contrat.update(value)
        elif choices == 3:
            id = int(input("Choisissez le contrat que vous souhaitez supprimez "))
            Contrat.delete(id)
        elif choices == 4:
            Evenement.create(value)
        else:
            return value
    else:
        print("Vous n'avez pas acces a ce menu, déconnexion")
        session.rollback()


def choice_menu_client(value):
    while True:
        choice_menu_client = get_choice("1: create\n2: update\n2 3: delete\n ")
        if choice_menu_client == 1:
            Client.create(value)
        elif choice_menu_client == 2:
            Client.update(value)
        elif choice_menu_client == 3:
            Client.delete(value)
        else:
            break